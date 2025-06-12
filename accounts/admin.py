from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Utilisateur, ProfilUtilisateur, Vehicule, 
    OffreCovoiturage, DemandeCovoiturage, Matching
)

# On personnalise l'affichage dans l'admin pour notre modèle Utilisateur
class UtilisateurAdmin(UserAdmin):
    model = Utilisateur
    list_display = ('email', 'nom', 'prenom', 'role', 'is_staff')
    search_fields = ('email', 'nom', 'prenom')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')
    ordering = ('email',)
    # Les fieldsets contrôlent la mise en page dans le formulaire d'édition
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations Personnelles', {'fields': ('nom', 'prenom', 'telephone', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_inscription')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'prenom', 'telephone', 'role', 'password'),
        }),
    )

admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(ProfilUtilisateur)
admin.site.register(Vehicule)
admin.site.register(OffreCovoiturage)
admin.site.register(DemandeCovoiturage)
admin.site.register(Matching)
