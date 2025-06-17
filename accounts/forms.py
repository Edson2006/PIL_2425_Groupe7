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
        fields = ['point_depart', 'point_arrivee', 'heure_depart', 'places_disponibles', 
                 'prix', 'commentaires']
        widgets = {
            'point_depart': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre position actuelle...',
                'id': 'departurePoint'
            }),
            'point_arrivee': forms.TextInput(attrs={
                'class': 'form-input',
                'value': 'Campus Universitaire - Avenue Jean-Paul II, Abomey-Calavi',
                'readonly': True
            }),
            'heure_depart': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-input'
            }),
            
            'prix': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Prix par passager (FCFA)'
            }),
            'places_disponibles': forms.Select(attrs={'class': 'form-select'}),
            'commentaires': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Informations supplémentaires...'
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Définition dynamique des choix
        self.fields['places_disponibles'].choices = [
            (i, f"{i} place{'s' if i > 1 else ''} disponible{'s' if i > 1 else ''}") 
            for i in range(1, 5)
        ]
class DemandeForm(forms.ModelForm):
    class Meta:
        model = DemandeCovoiturage
        fields = ['point_depart', 'point_arrivee', 'heure_souhaitee', 'flexibilite']
        widgets = {
            'heure_souhaitee': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'flexibilite': forms.NumberInput(attrs={'placeholder': 'Minutes'}),
        }
from django.contrib.auth.forms import SetPasswordForm 
class CustomPasswordResetForm(SetPasswordForm): 
    class Meta: fields = ['new_password1', 'new_password2']