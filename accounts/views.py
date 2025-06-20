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
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .models import DemandeCovoiturage, OffreCovoiturage, Matching
from django.views.decorators.http import require_POST
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
from django.http import JsonResponse
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
    try:
        profil = request.user.profilutilisateur
    except ProfilUtilisateur.DoesNotExist:
        profil = ProfilUtilisateur.objects.create(utilisateur=request.user)

    vehicule = Vehicule.objects.filter(utilisateur=request.user).first()
    
    if request.method == 'POST':
        profil_form = ProfilForm(request.POST, request.FILES, instance=profil)
        vehicule_form = VehiculeForm(request.POST, instance=vehicule) if request.user.role == 'conducteur' else None

        if profil_form.is_valid():
            # Gestion spécifique de la photo
            if 'photo_profil' in request.FILES:
                # Supprime l'ancienne photo si elle existe
                if profil.photo_profil:
                    profil.photo_profil.delete(save=False)
                # Affecte la nouvelle photo
                profil.photo_profil = request.FILES['photo_profil']
            
            # Sauvegarde du profil
            profil_form.save()

            # Sauvegarde du véhicule pour les conducteurs
            if request.user.role == 'conducteur' and vehicule_form and vehicule_form.is_valid():
                vehicule_form.save()

            messages.success(request, 'Profil mis à jour avec succès!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        profil_form = ProfilForm(instance=profil)
        vehicule_form = VehiculeForm(instance=vehicule) if request.user.role == 'conducteur' else None

    context = {
        'profil_form': profil_form,
        'vehicule_form': vehicule_form,
        'profil': profil,
        'user': request.user
    }
    return render(request, 'edit_profile.html', context)
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


def find_matches(request):
    """Recherche simplifiée de correspondances : seulement départ et arrivée"""
    user = request.user
    now = timezone.now()
    matches = []

    if user.role == 'passager':
        demandes = DemandeCovoiturage.objects.filter(passager=user)

        for demande in demandes:
            print(f"[DEBUG] Demande : {demande.point_depart} -> {demande.point_arrivee}")
            
            offres = OffreCovoiturage.objects.filter(
                point_depart__icontains=demande.point_depart,
                point_arrivee__icontains=demande.point_arrivee,
                places_disponibles__gt=0
            ).exclude(conducteur=user)

            print(f"[DEBUG] Offres trouvées pour la demande : {offres.count()}")

            for offre in offres:
                if not Matching.objects.filter(offre=offre, demande=demande).exists():
                    match = Matching.objects.create(offre=offre, demande=demande)
                    matches.append(match)
                    print(f"[DEBUG] Match créé entre Demande {demande.id} et Offre {offre.id}")

    elif user.role == 'conducteur':
        offres = OffreCovoiturage.objects.filter(conducteur=user)

        for offre in offres:
            print(f"[DEBUG] Offre : {offre.point_depart} -> {offre.point_arrivee}")
            
            demandes = DemandeCovoiturage.objects.filter(
                point_depart__icontains=offre.point_depart,
                point_arrivee__icontains=offre.point_arrivee
            ).exclude(passager=user)

            print(f"[DEBUG] Demandes trouvées pour l'offre : {demandes.count()}")

            for demande in demandes:
                if not Matching.objects.filter(offre=offre, demande=demande).exists():
                    match = Matching.objects.create(offre=offre, demande=demande)
                    matches.append(match)
                    print(f"[DEBUG] Match créé entre Offre {offre.id} et Demande {demande.id}")

    # Récupération des correspondances existantes
    user_matches = Matching.objects.filter(
        Q(demande__passager=user) | Q(offre__conducteur=user)
    ).select_related(
        'offre', 'offre__conducteur',
        'demande', 'demande__passager'
    ).order_by('-offre__heure_depart')

    return render(request, 'matches.html', {'matches': user_matches})


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
@login_required
def all_offers(request):
    """Affiche toutes les offres de covoiturage disponibles (toutes, sans filtre)"""
    offres = OffreCovoiturage.objects.select_related('conducteur').all().order_by('-heure_depart')
    now = timezone.now()
    return render(request, 'all_offers.html', {
        'offres': offres,
        'now': now
    })
    
@login_required
def all_requests(request):
    """Affiche toutes les demandes de covoiturage (toutes, sans filtre)"""
    demandes = DemandeCovoiturage.objects.select_related('passager').all().order_by('-heure_souhaitee')
    now = timezone.now()
    return render(request, 'all_requests.html', {
        'demandes': demandes,
        'now': now
    })

def diag(request):
    """
    Cette vue affiche simplement la page statique de présentation 
    du diagramme de flux de données.
    """
    # Django va chercher 'accounts/diag.html' dans les dossiers 'templates'
    return render(request, 'diag.html')

from django.contrib.auth.views import PasswordResetConfirmView 
from django.contrib import messages 
from django.contrib.auth import update_session_auth_hash 
from django.contrib.auth.forms import SetPasswordForm 
from django import forms 
from django.urls import reverse_lazy 

#Changement de mot de passe


# Formulaire personnalisé pour le changement de mot de passe
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={
            'id': 'password',
            'name': 'password',
            'class': 'form-control'
        }),
    )
    new_password2 = forms.CharField(
        label="Confirmation",
        widget=forms.PasswordInput(attrs={
            'id': 'password_confirm',
            'name': 'password_confirm',
            'class': 'form-control'
        }),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password1")
        password_confirm = cleaned_data.get("new_password2")

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("Les mots de passe ne correspondent pas.")
            if len(password) < 8:
                raise forms.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        return cleaned_data

# Vue personnalisée pour la confirmation du mot de passe
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Votre mot de passe a été réinitialisé avec succès !')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Veuillez corriger les erreurs ci-dessous.')
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return self.form_invalid(form)

        return super().post(request, *args, **kwargs)

# Fonction pour envoyer l'email de réinitialisation
def send_password_reset_email(user, reset_url):
    subject = "Réinitialisation de votre mot de passe"
    html_content = render_to_string(
        'registration/password_reset_email.html',
        {
            'user': user,
            'reset_url': reset_url,
            'site_name': "Votre Site"
        }
    )
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        'prudencemouzoun07@gmail.com',
        [user.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

#Delete Accounts

@login_required
@require_POST
def delete_account(request):
    try:
        # Vérification du mot de passe
        password = request.POST.get('password')
        user = request.user
        
        if not user.check_password(password):
            return JsonResponse({
                'success': False,
                'message': 'Mot de passe incorrect.'
            }, status=400)
        
        # Journalisation avant suppression (optionnel)
        logger.info(f"Suppression du compte utilisateur {user.email} (ID: {user.id})")
        
        # Suppression réelle
        user.delete()
        
        # Déconnexion
        logout(request)
        
        return JsonResponse({
            'success': True,
            'message': 'Votre compte a été supprimé avec succès.',
            'redirect_url': reverse('home')  # URL de redirection après suppression
        })
        
    except Exception as e:
        logger.error(f"Erreur suppression compte: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Une erreur est survenue lors de la suppression.'
        }, status=500)
