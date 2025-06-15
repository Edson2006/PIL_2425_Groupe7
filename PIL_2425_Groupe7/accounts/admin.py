from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, ProfilUtilisateur, Vehicule, OffreCovoiturage, DemandeCovoiturage

class UtilisateurAdmin(UserAdmin):
    """Configuration de l'administration pour le modèle Utilisateur personnalisé"""
    
    # Champs à afficher dans la liste des utilisateurs
    list_display = ('email', 'nom', 'prenom', 'telephone', 'role', 'is_active', 'is_staff', 'date_inscription')
    
    # Champs par lesquels on peut filtrer
    list_filter = ('role', 'is_active', 'is_staff', 'date_inscription')
    
    # Champs dans lesquels on peut rechercher
    search_fields = ('email', 'nom', 'prenom', 'telephone')
    
    # Ordre d'affichage
    ordering = ('email',)
    
    # Configuration des champs dans le formulaire d'édition
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('nom', 'prenom', 'telephone', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_inscription')}),
    )
    
    # Configuration des champs pour la création d'un utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'prenom', 'telephone', 'role', 'password1', 'password2'),
        }),
    )
    
    # Champs en lecture seule
    readonly_fields = ('date_inscription', 'last_login')

# Enregistrement des modèles dans l'administration
admin.site.register(Utilisateur, UtilisateurAdmin)

# Enregistrement des autres modèles (si ils ont du contenu)
@admin.register(ProfilUtilisateur)
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('utilisateur',)
    search_fields = ('utilisateur__email',)

@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('utilisateur',)
    search_fields = ('utilisateur__email',)

@admin.register(OffreCovoiturage)
class OffreCovoiturageAdmin(admin.ModelAdmin):
    list_display = ('conducteur',)
    search_fields = ('conducteur__email',)

@admin.register(DemandeCovoiturage)
class DemandeCovoiturageAdmin(admin.ModelAdmin):
    list_display = ('passager',)
    search_fields = ('passager__email',)

# Personnalisation du titre de l'administration
admin.site.site_header = "Administration Covoiturage"
admin.site.site_title = "Covoiturage Admin"
admin.site.index_title = "Bienvenue dans l'administration"