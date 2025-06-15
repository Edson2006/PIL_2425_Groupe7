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
            'heure_depart': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-input'
            }),
            'point_depart': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre position actuelle...',
                'readonly': 'readonly'
            }),
            'point_arrivee': forms.TextInput(attrs={
                'class': 'form-input',
                'readonly': 'readonly'
            }),
            'places_disponibles': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '1',
                'max': '6'
            }),
            'prix': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0'
            }),
            'commentaires': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': '3',
                'placeholder': 'Informations supplémentaires (point de rencontre, bagages, etc.)'
            }),
            'marque': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'ex: Toyota, Peugeot...'
            }),
            'modele': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'ex: Corolla, 307...'
            })
        }
        labels = {
            'point_depart': 'Point de Départ',
            'point_arrivee': 'Point d\'Arrivée',
            'heure_depart': 'Date et Heure de Départ',
            'places_disponibles': 'Places Disponibles',
            'prix': 'Prix par passager (FCFA)',
            'commentaires': 'Informations Complémentaires',
            'marque_vehicule': 'Marque du Véhicule',
            'modele_vehicule': 'Modèle du Véhicule'
        }

class DemandeForm(forms.ModelForm):
    class Meta:
        model = DemandeCovoiturage
        fields = ['point_depart', 'point_arrivee', 'heure_souhaitee', 'flexibilite']
        widgets = {
            'point_depart': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre position actuelle...',
                'readonly': 'readonly'
            }),
            'point_arrivee': forms.TextInput(attrs={
                'class': 'form-input',
                'value': 'Campus Universitaire - Avenue Jean-Paul II, Abomey-Calavi',
                'readonly': 'readonly'
            }),
            'heure_souhaitee': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-input',
                'required': 'required'
            }),
            'flexibilite': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Minutes de flexibilité',
                'min': '0',
                'max': '120'
            }),
           
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['heure_souhaitee'].label = "Date et Heure de Départ souhaitée"
        self.fields['flexibilite'].label = "Flexibilité horaire (minutes)"