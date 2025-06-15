from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Utilisateur,
    ProfilUtilisateur,
    Vehicule,
    OffreCovoiturage,
    DemandeCovoiturage,
    Matching,
    Conversation,
    Message
)
from .forms import ProfilForm, VehiculeForm, OffreForm, DemandeForm  
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import logging
from geopy.distance import geodesic
from datetime import timedelta
from django.db.models import Q
from django.utils import timezone

logger = logging.getLogger(__name__)

def index(request):
    """Page d'accueil principale"""
    return render(request, "index.html")

import re
from django.db import transaction, IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Utilisateur, ProfilUtilisateur
import logging

logger = logging.getLogger(__name__)

def sign_in_out(request):
    """Page d'inscription et de connexion"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    # Données pour pré-remplir le formulaire
    form_data = {
        'email': '',
        'nom': '',
        'prenom': '',
        'telephone': '',
        'role': ''
    }
    
    # Messages d'erreur
    registration_errors = []
    login_error = None

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'register':
            # Récupération des données
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()
            nom = request.POST.get('nom', '').strip()
            prenom = request.POST.get('prenom', '').strip()
            telephone = request.POST.get('telephone', '').strip()
            role = request.POST.get('role', '').strip()
            
            # Sauvegarde pour ré-affichage
            form_data = {
                'email': email,
                'nom': nom,
                'prenom': prenom,
                'telephone': telephone,
                'role': role
            }
            
            # Validation
            registration_errors = []
            
            if not email:
                registration_errors.append('L\'email est obligatoire')
            elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                registration_errors.append('Format d\'email invalide')
                
            if not password:
                registration_errors.append('Le mot de passe est obligatoire')
            elif len(password) < 5:  
                registration_errors.append('Le mot de passe doit contenir au moins 5 caractères')
                
            if not nom:
                registration_errors.append('Le nom est obligatoire')
                
            if not prenom:
                registration_errors.append('Le prénom est obligatoire')
                
            if not telephone:
                registration_errors.append('Le téléphone est obligatoire')
            elif not re.match(r'^\+?[0-9\s\-\(\)]{8,20}$', telephone):
                registration_errors.append('Format de téléphone invalide')
                
            if not role:
                registration_errors.append('Le rôle est obligatoire')
            elif role not in ['conducteur', 'passager']:
                registration_errors.append('Le rôle doit être "conducteur" ou "passager"')
            
            # Vérification des doublons si pas d'erreurs
            if not registration_errors:
                try:
                    with transaction.atomic():
                        if Utilisateur.objects.filter(email=email).exists():
                            registration_errors.append('Cette adresse e-mail est déjà utilisée')
                            
                        if Utilisateur.objects.filter(telephone=telephone).exists():
                            registration_errors.append('Ce numéro de téléphone est déjà utilisé')
                            
                        if not registration_errors:
                            # Création de l'utilisateur
                            user = Utilisateur.objects.create_user(
                                email=email,
                                password=password,
                                nom=nom,
                                prenom=prenom,
                                telephone=telephone,
                                role=role
                            )
                            
                            # Création automatique du profil
                            ProfilUtilisateur.objects.create(utilisateur=user)
                            
                            messages.success(request, 'Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.')
                            return redirect('sign_in_out')
                    
                except Exception as e:
                    registration_errors.append(f'Une erreur est survenue lors de la création du compte: {str(e)}')

        elif action == 'login':
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()
            
            if not email or not password:
                login_error = 'Veuillez remplir tous les champs'
            else:
                user = authenticate(request, email=email, password=password)
                
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, f'Bienvenue {user.prenom} !')
                        return redirect('dashboard')
                    else:
                        login_error = 'Votre compte est désactivé'
                else:
                    login_error = 'Adresse e-mail ou mot de passe incorrect'
    
    context = {
        'form_data': form_data,
        'registration_errors': registration_errors,
        'login_error': login_error,
    }
    return render(request, "sign_in_out.html", context)
@login_required
def dashboard(request):
    """Tableau de bord après connexion"""
    user = request.user
    now = timezone.now()
    
    # Récupérer les données selon le rôle
    if user.role == 'passager':
        # Offres disponibles (exclure celles de l'utilisateur et celles passées)
        offres_disponibles = OffreCovoiturage.objects.filter(
            heure_depart__gt=now,
            places_disponibles__gt=0
        ).exclude(conducteur=user).order_by('heure_depart')[:10]
        
        # Demandes de l'utilisateur
        publications = DemandeCovoiturage.objects.filter(passager=user).order_by('-heure_souhaitee')[:5]
        demandes_disponibles = None
    else:  # conducteur
        # Demandes disponibles (exclure celles de l'utilisateur et celles passées)
        demandes_disponibles = DemandeCovoiturage.objects.filter(
            heure_souhaitee__gt=now
        ).exclude(passager=user).order_by('heure_souhaitee')[:10]
        
        # Offres de l'utilisateur
        publications = OffreCovoiturage.objects.filter(conducteur=user).order_by('-heure_depart')[:5]
        offres_disponibles = None

    # Conversations récentes
    conversations = Conversation.objects.filter(
        Q(utilisateur1=user) | Q(utilisateur2=user)
    ).order_by('-derniere_activite')[:5]

    # Récupérer la photo de profil si elle existe
    try:
        photo_profil = user.profilutilisateur.photo_profil.url
    except (ProfilUtilisateur.DoesNotExist, ValueError):
        photo_profil = None

    context = {
        'user': user,
        'conversations': conversations,
        'publications': publications,
        'photo_profil': photo_profil
    }

    if user.role == 'passager':
        context['offres_disponibles'] = offres_disponibles
    else:
        context['demandes_disponibles'] = demandes_disponibles

    return render(request, "dashboard.html", context)
def switch_role(request, role):
    """Changer de rôle dans la session"""
    if role in ['conducteur', 'passager']:
        request.session['active_role'] = role
    return redirect('dashboard')

def sign_out(request):
    """Déconnexion de l'utilisateur"""
    user_name = request.user.prenom if request.user.is_authenticated else ""
    logout(request)
    if user_name:
        messages.success(request, f"Au revoir {user_name} ! Vous avez été déconnecté avec succès.")
    else:
        messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('home')  # Redirection vers la page d'accueil après déconnexion

def debug_users(request):
    """Vue de débogage pour voir tous les utilisateurs"""
    users = Utilisateur.objects.all()
    print("=== TOUS LES UTILISATEURS ===")
    for user in users:
        print(f"ID: {user.id}, Email: {user.email}, Nom: {user.nom}, Prénom: {user.prenom}, Rôle: {user.role}, Actif: {user.is_active}")
    print("=============================")
    
    return render(request, 'debug_users.html', {'users': users})

@login_required
def edit_profile(request):
    """Modification du profil utilisateur"""
    try:
        profil = request.user.profilutilisateur
    except ProfilUtilisateur.DoesNotExist:
        profil = ProfilUtilisateur(utilisateur=request.user)

    vehicule = Vehicule.objects.filter(utilisateur=request.user).first()
    if not vehicule:
        vehicule = Vehicule(utilisateur=request.user)

    if request.method == 'POST':
        profil_form = ProfilForm(request.POST, request.FILES, instance=profil)
        vehicule_form = VehiculeForm(request.POST, instance=vehicule)
        
        if profil_form.is_valid() and vehicule_form.is_valid():
            profil_form.save()
            
            # Sauvegarder seulement si l'utilisateur est conducteur
            if request.user.role == 'conducteur':
                vehicule_form.save()
                
            messages.success(request, 'Profil mis à jour avec succès!')
            return redirect('dashboard')
    else:
        profil_form = ProfilForm(instance=profil)
        vehicule_form = VehiculeForm(instance=vehicule)
    
    return render(request, 'edit_profile.html', {
        'profil_form': profil_form,
        'vehicule_form': vehicule_form,
        'photo_profil': profil.photo_profil.url if profil.photo_profil else None
    })
@login_required
def create_offer(request):
    """Création d'une offre de covoiturage"""
    if request.method == 'POST':
        form = OffreForm(request.POST)
        if form.is_valid():
            offre = form.save(commit=False)
            offre.conducteur = request.user
            offre.save()
            messages.success(request, 'Offre publiée avec succès!')
            return redirect('my_offers')
    else:
        form = OffreForm()
    return render(request, 'create_offer.html', {'form': form})

@login_required
def create_request(request):
    """Création d'une demande de covoiturage"""
    if request.method == 'POST':
        form = DemandeForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.passager = request.user
            demande.save()
            messages.success(request, 'Demande publiée avec succès!')
            return redirect('my_requests')
    else:
        form = DemandeForm()
    return render(request, 'create_request.html', {'form': form})

@login_required
def my_offers(request):
    """Liste des offres de covoiturage de l'utilisateur"""
    offres = OffreCovoiturage.objects.filter(conducteur=request.user)
    now = timezone.now()
    return render(request, 'my_offers.html', {
        'offres': offres,
        'now': now
    })

@login_required
def my_requests(request):
    """Liste des demandes de covoiturage de l'utilisateur"""
    demandes = DemandeCovoiturage.objects.filter(passager=request.user)
    now = timezone.now()
    return render(request, 'my_requests.html', {
        'demandes': demandes,
        'now': now
    })

@login_required
def find_matches(request):
    """Recherche de correspondances entre offres et demandes"""
    user = request.user
    matches = []
    
    if user.role == 'passager':
        demandes = DemandeCovoiturage.objects.filter(passager=user)
        for demande in demandes:
            # Recherche avec flexibilité temporelle
            time_range = (
                demande.heure_souhaitee - demande.flexibilite,
                demande.heure_souhaitee + demande.flexibilite
            )
            
            offres = OffreCovoiturage.objects.filter(
                point_depart__icontains=demande.point_depart,
                point_arrivee__icontains=demande.point_arrivee,
                heure_depart__range=time_range,
                places_disponibles__gt=0
            ).exclude(conducteur=user)
            
            for offre in offres:
                if not Matching.objects.filter(offre=offre, demande=demande).exists():
                    match = Matching(offre=offre, demande=demande)
                    match.save()
                    matches.append(match)
    
    else:
        offres = OffreCovoiturage.objects.filter(conducteur=user)
        for offre in offres:
            # Recherche avec flexibilité temporelle
            time_range = (
                offre.heure_depart - timedelta(minutes=30),
                offre.heure_depart + timedelta(minutes=30)
            )
            
            demandes = DemandeCovoiturage.objects.filter(
                point_depart__icontains=offre.point_depart,
                point_arrivee__icontains=offre.point_arrivee,
                heure_souhaitee__range=time_range
            ).exclude(passager=user)
            
            for demande in demandes:
                if not Matching.objects.filter(offre=offre, demande=demande).exists():
                    match = Matching(offre=offre, demande=demande)
                    match.save()
                    matches.append(match)
    
    return render(request, 'matches.html', {'matches': matches})

@login_required
def conversations_list(request):
    """Liste des conversations de l'utilisateur"""
    user_conversations = Conversation.objects.filter(
        Q(utilisateur1=request.user) | Q(utilisateur2=request.user)
    ).order_by('-derniere_activite')
    return render(request, 'conversation.html', {'conversations': user_conversations})

@login_required
def conversation_detail(request, conversation_id):
    """Détail d'une conversation spécifique"""
    conversation = get_object_or_404(
        Conversation, 
        Q(id=conversation_id),
        Q(utilisateur1=request.user) | Q(utilisateur2=request.user)
    )
    
    messages_list = Message.objects.filter(conversation=conversation).order_by('date_envoi')
    
    # Marquer les messages comme lus
    Message.objects.filter(conversation=conversation, lu=False).exclude(expediteur=request.user).update(lu=True)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                conversation=conversation,
                expediteur=request.user,
                contenu=content
            )
            conversation.derniere_activite = timezone.now()
            conversation.save()
            return redirect('conversation_detail', conversation_id=conversation_id)
    
    return render(request, 'conversation.html', {
        'conversation': conversation,
        'messages': messages_list,
        'other_user': conversation.utilisateur2 if conversation.utilisateur1 == request.user else conversation.utilisateur1
    })

@login_required
def start_conversation(request, user_id):
    """Démarrer une nouvelle conversation avec un autre utilisateur"""
    other_user = get_object_or_404(Utilisateur, id=user_id)
    
    # Vérifier si une conversation existe déjà
    conversation = Conversation.objects.filter(
        Q(utilisateur1=request.user, utilisateur2=other_user) |
        Q(utilisateur1=other_user, utilisateur2=request.user)
    ).first()
    
    if not conversation:
        conversation = Conversation.objects.create(
            utilisateur1=request.user,
            utilisateur2=other_user
        )
    
    return redirect('conversation_detail', conversation_id=conversation.id)

@login_required
def edit_offer(request, pk):
    offre = get_object_or_404(OffreCovoiturage, id=pk, conducteur=request.user)
    if request.method == 'POST':
        form = OffreForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            messages.success(request, 'Offre mise à jour avec succès!')
            return redirect('dashboard')
    else:
        form = OffreForm(instance=offre)
    return render(request, 'edit_offer.html', {'form': form})

@login_required
def edit_request(request, pk):
    demande = get_object_or_404(DemandeCovoiturage, id=pk, passager=request.user)
    if request.method == 'POST':
        form = DemandeForm(request.POST, instance=demande)
        if form.is_valid():
            form.save()
            messages.success(request, 'Demande mise à jour avec succès!')
            return redirect('dashboard')
    else:
        form = DemandeForm(instance=demande)
    return render(request, 'edit_request.html', {'form': form})
@login_required
def delete_offer(request, pk):
    offre = get_object_or_404(OffreCovoiturage, id=pk, conducteur=request.user)
    
    if request.method == 'POST':
        offre.delete()
        messages.success(request, 'Offre supprimée avec succès!')
        return redirect('my_offers')
    
    return render(request, 'confirm_delete_offer.html', {'offre': offre})


@login_required
def delete_request(request, pk):
    demande = get_object_or_404(DemandeCovoiturage, id=pk, passager=request.user)
    now = timezone.now()
    
    if request.method == 'POST':
        demande.delete()
        messages.success(request, 'Demande supprimée avec succès!')
        return redirect('my_requests')
    
    return render(request, 'confirm_delete_request.html', {
        'demande': demande,
        'now': now
    })