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
    print("=== DÉBUT DE LA FONCTION sign_in_out ===")
    print(f"Méthode de requête: {request.method}")
    print(f"Utilisateur authentifié: {request.user.is_authenticated}")
    print(f"URL complète: {request.get_full_path()}")
    print(f"GET parameters: {dict(request.GET)}")
    
    if request.user.is_authenticated:
        print("Utilisateur déjà connecté, redirection vers dashboard")
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
        # Récupérer l'action depuis POST ou GET
        action = request.POST.get('action') or request.GET.get('action')
        print(f"Action POST détectée: {request.POST.get('action')}")
        print(f"Action GET détectée: {request.GET.get('action')}")
        print(f"Action finale utilisée: {action}")
        print(f"Données POST reçues: {dict(request.POST)}")
        
        if action == 'register':
            print("--- TRAITEMENT DE L'INSCRIPTION ---")
            
            # Récupération des données
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()
            nom = request.POST.get('nom', '').strip()
            prenom = request.POST.get('prenom', '').strip()
            telephone = request.POST.get('telephone', '').strip()
            role = request.POST.get('role', '').strip()
            
            print(f"Données récupérées:")
            print(f"  - Email: '{email}'")
            print(f"  - Password: {'*' * len(password)} ({len(password)} caractères)")
            print(f"  - Nom: '{nom}'")
            print(f"  - Prénom: '{prenom}'")
            print(f"  - Téléphone: '{telephone}'")
            print(f"  - Rôle: '{role}'")
            
            # Sauvegarde pour ré-affichage
            form_data = {
                'email': email,
                'nom': nom,
                'prenom': prenom,
                'telephone': telephone,
                'role': role
            }
            
            # Validation
            print("Début de la validation...")
            registration_errors = []
            
            if not email:
                print("Erreur: Email manquant")
                registration_errors.append('L\'email est obligatoire')
            elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                print(f"Erreur: Format email invalide pour '{email}'")
                registration_errors.append('Format d\'email invalide')
            else:
                print("Email valide")
                
            if not password:
                print("Erreur: Mot de passe manquant")
                registration_errors.append('Le mot de passe est obligatoire')
            elif len(password) < 5:
                print(f"Erreur: Mot de passe trop court ({len(password)} caractères)")
                registration_errors.append('Le mot de passe doit contenir au moins 5 caractères')
            else:
                print("Mot de passe valide")
                
            if not nom:
                print("Erreur: Nom manquant")
                registration_errors.append('Le nom est obligatoire')
            else:
                print("Nom valide")
                
            if not prenom:
                print("Erreur: Prénom manquant")
                registration_errors.append('Le prénom est obligatoire')
            else:
                print("Prénom valide")
                
            if not telephone:
                print("Erreur: Téléphone manquant")
                registration_errors.append('Le téléphone est obligatoire')
            elif not re.match(r'^\+?[0-9\s\-\(\)]{8,20}$', telephone):
                print(f"Erreur: Format téléphone invalide pour '{telephone}'")
                registration_errors.append('Format de téléphone invalide')
            else:
                print("Téléphone valide")
                
            if not role:
                print("Erreur: Rôle manquant")
                registration_errors.append('Le rôle est obligatoire')
            elif role not in ['conducteur', 'passager']:
                print(f"Erreur: Rôle invalide '{role}'")
                registration_errors.append('Le rôle doit être "conducteur" ou "passager"')
            else:
                print("Rôle valide")
            
            print(f"Nombre d'erreurs de validation: {len(registration_errors)}")
            if registration_errors:
                print(f"Erreurs: {registration_errors}")
            
            # Vérification des doublons si pas d'erreurs
            if not registration_errors:
                print("Validation réussie, vérification des doublons...")
                try:
                    with transaction.atomic():
                        email_exists = Utilisateur.objects.filter(email=email).exists()
                        telephone_exists = Utilisateur.objects.filter(telephone=telephone).exists()
                        
                        print(f"Email déjà utilisé: {email_exists}")
                        print(f"Téléphone déjà utilisé: {telephone_exists}")
                        
                        if email_exists:
                            print("Erreur: Email déjà utilisé")
                            registration_errors.append('Cette adresse e-mail est déjà utilisée')
                            
                        if telephone_exists:
                            print("Erreur: Téléphone déjà utilisé")
                            registration_errors.append('Ce numéro de téléphone est déjà utilisé')
                            
                        if not registration_errors:
                            print("Pas de doublons, création de l'utilisateur...")
                            # Création de l'utilisateur
                            user = Utilisateur.objects.create_user(
                                email=email,
                                password=password,
                                nom=nom,
                                prenom=prenom,
                                telephone=telephone,
                                role=role
                            )
                            print(f"Utilisateur créé avec l'ID: {user.id}")
                            
                            # Création automatique du profil
                            profil = ProfilUtilisateur.objects.create(utilisateur=user)
                            profil.refresh_from_db()
                            
                            messages.success(request, 'Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.')
                            print("Inscription réussie, redirection...")
                            return redirect('sign_in_out')
                    
                except Exception as e:
                    print(f"ERREUR lors de la création: {str(e)}")
                    print(f"Type d'erreur: {type(e).__name__}")
                    import traceback
                    print(f"Traceback complet: {traceback.format_exc()}")
                    registration_errors.append(f'Une erreur est survenue lors de la création du compte: {str(e)}')

        elif action == 'login':
            print("--- TRAITEMENT DE LA CONNEXION ---")
            
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()
            
            print(f"Tentative de connexion:")
            print(f"  - Email: '{email}'")
            print(f"  - Password: {'*' * len(password)} ({len(password)} caractères)")
            
            if not email or not password:
                print("Erreur: Champs manquants")
                login_error = 'Veuillez remplir tous les champs'
            else:
                print("Tentative d'authentification...")
                user = authenticate(request, email=email, password=password)
                
                print(f"Résultat authenticate: {user}")
                
                if user is not None:
                    print(f"Utilisateur trouvé: {user.email}")
                    print(f"Utilisateur actif: {user.is_active}")
                    
                    if user.is_active:
                        print("Connexion de l'utilisateur...")
                        login(request, user)
                        messages.success(request, f'Bienvenue {user.prenom} !')
                        print("Connexion réussie, redirection vers dashboard")
                        return redirect('dashboard')
                    else:
                        print("Erreur: Compte désactivé")
                        login_error = 'Votre compte est désactivé'
                else:
                    print("Erreur: Authentification échouée")
                    login_error = 'Adresse e-mail ou mot de passe incorrect'
        else:
            print(f"Action inconnue ou manquante: '{action}'")
    
    else:
        print("Requête GET - Affichage du formulaire")
    
    print("Préparation du contexte pour le template")
    context = {
        'form_data': form_data,
        'registration_errors': registration_errors,
        'login_error': login_error,
    }
    print(f"Contexte final: {context}")
    print("=== FIN DE LA FONCTION sign_in_out ===")
    
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
    """Recherche de correspondances entre offres et demandes avec debug"""
    user = request.user
    matches = []

    print(f"Utilisateur connecté : {user} - rôle : {user.role}")

    if user.role == 'passager' or user.role == 'conducteur':
        demandes = DemandeCovoiturage.objects.filter(passager=user)
        print(f"Nombre de demandes du passager : {demandes.count()}")

        for demande in demandes:
            print(f"\n🔍 Demande analysée : {demande}")
            print(f" - Départ : {demande.point_depart}")
            print(f" - Arrivée : {demande.point_arrivee}")
            print(f" - Heure souhaitée : {demande.heure_souhaitee}")
            print(f" - Flexibilité : {demande.flexibilite}")

            # Calcul de la plage horaire
            time_range = (
                demande.heure_souhaitee - demande.flexibilite,
                demande.heure_souhaitee + demande.flexibilite
            )
            print(f" - Plage horaire recherchée : {time_range[0]} → {time_range[1]}")

            offres = OffreCovoiturage.objects.filter(
                point_depart__icontains=demande.point_depart,
                point_arrivee__icontains=demande.point_arrivee,
                heure_depart__range=time_range,
                places_disponibles__gt=0
            ).exclude(conducteur=user)

            print(f"Offres trouvées : {offres.count()}")

            for offre in offres:
                print(f"✅ Offre possible : {offre} à {offre.heure_depart}")
                if not Matching.objects.filter(offre=offre, demande=demande).exists():
                    print("👉 Nouvelle correspondance créée")
                    match = Matching(offre=offre, demande=demande)
                    match.save()
                    matches.append(match)
                else:
                    print("❌ Déjà existant : Matching refusé")

    else:  # Cas conducteur
        offres = OffreCovoiturage.objects.filter(conducteur=user)
        print(f"Nombre d'offres du conducteur : {offres.count()}")

        for offre in offres:
            print(f"\n🔍 Offre analysée : {offre}")
            print(f" - Départ : {offre.point_depart}")
            print(f" - Arrivée : {offre.point_arrivee}")
            print(f" - Heure départ : {offre.heure_depart}")

            time_range = (
                offre.heure_depart - timedelta(minutes=30),
                offre.heure_depart + timedelta(minutes=30)
            )
            print(f" - Plage horaire : {time_range[0]} → {time_range[1]}")

            demandes = DemandeCovoiturage.objects.filter(
                point_depart__icontains=offre.point_depart,
                point_arrivee__icontains=offre.point_arrivee,
                heure_souhaitee__range=time_range
            ).exclude(passager=user)

            print(f"Demandes trouvées : {demandes.count()}")

            for demande in demandes:
                print(f"✅ Demande possible : {demande} à {demande.heure_souhaitee}")
                if not Matching.objects.filter(offre=offre, demande=demande).exists():
                    print("👉 Nouvelle correspondance créée")
                    match = Matching(offre=offre, demande=demande)
                    match.save()
                    matches.append(match)
                else:
                    print("❌ Déjà existant : Matching refusé")

    print(f"\nTotal des correspondances créées : {len(matches)}")
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