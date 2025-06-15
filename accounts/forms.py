from django import forms
from .models import ProfilUtilisateur, Vehicule, OffreCovoiturage, DemandeCovoiturage

class ProfilForm(forms.ModelForm):
    class Meta:
        model = ProfilUtilisateur
        fields = ['photo_profil', 'point_depart', 'horaires_depart', 'horaires_arrivee']
        widgets = {
            'horaires_depart': forms.TimeInput(attrs={'type': 'time'}),
            'horaires_arrivee': forms.TimeInput(attrs={'type': 'time'}),
        }

class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ['marque', 'modele', 'nombre_places', 'plaque_immatriculation']

class OffreForm(forms.ModelForm):
    class Meta:
        model = OffreCovoiturage
        fields = ['point_depart', 'point_arrivee', 'heure_depart', 'places_disponibles', 'prix', 'commentaires']
        widgets = {
            'heure_depart': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class DemandeForm(forms.ModelForm):
    class Meta:
        model = DemandeCovoiturage
        fields = ['point_depart', 'point_arrivee', 'heure_souhaitee', 'flexibilite']
        widgets = {
            'heure_souhaitee': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'flexibilite': forms.NumberInput(attrs={'placeholder': 'Minutes'}),
        }