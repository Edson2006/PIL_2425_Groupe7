from django.shortcuts import render, redirect
# CORRECTION: On importe notre nouveau modèle et les fonctions d'authentification
from .models import Utilisateur 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def sign_in_out(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        # --- Logique d'Inscription ---
        if action == 'register':
            email = request.POST.get('email')
            password = request.POST.get('password')
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            telephone = request.POST.get('telephone')
            role = request.POST.get('role')

            # Vérifie si l'email ou le téléphone existe déjà
            if Utilisateur.objects.filter(email=email).exists():
                messages.error(request, 'Un utilisateur avec cette adresse e-mail existe déjà.')
                return redirect('sign_in_out')
            if Utilisateur.objects.filter(telephone=telephone).exists():
                messages.error(request, 'Ce numéro de téléphone est déjà utilisé.')
                return redirect('sign_in_out')

            try:
                # On utilise notre Manager personnalisé pour créer l'utilisateur
                # Le mot de passe sera automatiquement hashé
                Utilisateur.objects.create_user(
                    email=email,
                    password=password,
                    nom=nom,
                    prenom=prenom,
                    telephone=telephone,
                    role=role
                )
                messages.success(request, 'Votre compte a été créé ! Vous pouvez maintenant vous connecter.')
                return redirect('sign_in_out')
            except Exception as e:
                messages.error(request, f"Une erreur est survenue lors de la création du compte : {e}")
                return redirect('sign_in_out')

        # --- Logique de Connexion ---
        elif action == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')

            # 'authenticate' fonctionne maintenant avec notre modèle grâce à USERNAME_FIELD = 'email'
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Connexion réussie ! Bonjour, {user.prenom}.')
                return redirect('home') # Rediriger vers l'accueil après connexion
            else:
                messages.error(request, 'Adresse e-mail ou mot de passe incorrect.')
                return redirect('sign_in_out')

    return render(request, "sign_in_out.html")


def index(request):
    # Exemple de page d'accueil qui affiche un message différent si l'utilisateur est connecté
    return render(request, "index.html")
