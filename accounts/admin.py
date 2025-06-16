from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, ProfilUtilisateur, Vehicule, OffreCovoiturage, DemandeCovoiturage, Matching


class UtilisateurAdmin(UserAdmin):
    """Configuration de l'administration pour le modèle Utilisateur personnalisé"""
    list_display = ('email', 'nom', 'prenom', 'telephone', 'role', 'is_active', 'is_staff', 'date_inscription')
    list_filter = ('role', 'is_active', 'is_staff', 'date_inscription')
    search_fields = ('email', 'nom', 'prenom', 'telephone')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('nom', 'prenom', 'telephone', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_inscription')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'prenom', 'telephone', 'role', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('date_inscription', 'last_login')


@admin.register(ProfilUtilisateur)
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'point_depart', 'horaires_depart', 'horaires_arrivee')
    search_fields = ('utilisateur__email',)


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'marque', 'modele', 'nombre_places', 'plaque_immatriculation')
    search_fields = ('utilisateur__email', 'marque', 'modele', 'plaque_immatriculation')


@admin.register(OffreCovoiturage)
class OffreCovoiturageAdmin(admin.ModelAdmin):
    list_display = ('conducteur', 'point_depart', 'point_arrivee', 'heure_depart', 'places_disponibles', 'prix')
    search_fields = ('conducteur__email', 'point_depart', 'point_arrivee')


@admin.register(DemandeCovoiturage)
class DemandeCovoiturageAdmin(admin.ModelAdmin):
    list_display = ('passager', 'point_depart', 'point_arrivee', 'heure_souhaitee', 'flexibilite')
    search_fields = ('passager__email', 'point_depart', 'point_arrivee')


@admin.register(Matching)
class MatchingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_conducteur_email',
        'get_passager_email',
        'get_offre_depart',
        'get_offre_arrivee',
        'get_demande_depart',
        'get_demande_arrivee',
        'get_heure_depart',
        'get_heure_souhaitee',
        'score_match',
        'date_match',
    )
    search_fields = (
        'offre__conducteur__email',
        'demande__passager__email',
        'offre__point_depart',
        'demande__point_depart',
    )
    list_filter = ('date_match',)

    def get_conducteur_email(self, obj):
        return obj.offre.conducteur.email
    get_conducteur_email.short_description = "Conducteur"

    def get_passager_email(self, obj):
        return obj.demande.passager.email
    get_passager_email.short_description = "Passager"

    def get_offre_depart(self, obj):
        return obj.offre.point_depart
    get_offre_depart.short_description = "Offre - Départ"

    def get_offre_arrivee(self, obj):
        return obj.offre.point_arrivee
    get_offre_arrivee.short_description = "Offre - Arrivée"

    def get_demande_depart(self, obj):
        return obj.demande.point_depart
    get_demande_depart.short_description = "Demande - Départ"

    def get_demande_arrivee(self, obj):
        return obj.demande.point_arrivee
    get_demande_arrivee.short_description = "Demande - Arrivée"

    def get_heure_depart(self, obj):
        return obj.offre.heure_depart
    get_heure_depart.short_description = "Heure Départ"

    def get_heure_souhaitee(self, obj):
        return obj.demande.heure_souhaitee
    get_heure_souhaitee.short_description = "Heure Souhaitée"


# Enregistrement du modèle Utilisateur avec sa configuration personnalisée
admin.site.register(Utilisateur, UtilisateurAdmin)

# Personnalisation de l'interface d'administration
admin.site.site_header = "Administration Covoiturage"
admin.site.site_title = "Covoiturage Admin"
admin.site.index_title = "Bienvenue dans l'administration"
