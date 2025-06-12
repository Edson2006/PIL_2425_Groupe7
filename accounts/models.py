from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, nom, prenom, telephone, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            nom=nom,
            prenom=prenom,
            telephone=telephone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, prenom, telephone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')
        return self.create_user(email, nom, prenom, telephone, password, **extra_fields)

class Utilisateur(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('conducteur', 'Conducteur'),
        ('passager', 'Passager'),
    )
    email = models.EmailField(max_length=100, unique=True, verbose_name="Adresse email")
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='passager')
    date_inscription = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UtilisateurManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'telephone']

    def __str__(self):
        return self.email

# On utilise OneToOneField avec le nom du modèle pour éviter les import circulaires
class ProfilUtilisateur(models.Model):
    utilisateur = models.OneToOneField('accounts.Utilisateur', on_delete=models.CASCADE, primary_key=True)
    photo_profil = models.TextField(blank=True, null=True)
    point_depart = models.TextField(blank=True, null=True)
    horaires_depart = models.TimeField(blank=True, null=True)
    horaires_arrivee = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Profil de {self.utilisateur.email}"

# On utilise ForeignKey avec le nom du modèle
class Vehicule(models.Model):
    utilisateur = models.ForeignKey('accounts.Utilisateur', on_delete=models.CASCADE)
    marque = models.CharField(max_length=100, blank=True, null=True)
    modele = models.CharField(max_length=100, blank=True, null=True)
    nombre_places = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.marque} {self.modele} de {self.utilisateur.prenom}"

class OffreCovoiturage(models.Model):
    conducteur = models.ForeignKey('accounts.Utilisateur', on_delete=models.CASCADE)
    point_depart = models.TextField()
    point_arrivee = models.TextField()
    heure_depart = models.DateTimeField()
    places_disponibles = models.IntegerField()

    def __str__(self):
        return f"Offre de {self.conducteur.prenom} de {self.point_depart} à {self.point_arrivee}"

class DemandeCovoiturage(models.Model):
    passager = models.ForeignKey('accounts.Utilisateur', on_delete=models.CASCADE)
    point_depart = models.TextField()
    point_arrivee = models.TextField()
    heure_souhaitee = models.DateTimeField()

    def __str__(self):
        return f"Demande de {self.passager.prenom} de {self.point_depart} à {self.point_arrivee}"

class Matching(models.Model):
    offre = models.ForeignKey(OffreCovoiturage, on_delete=models.CASCADE)
    demande = models.ForeignKey(DemandeCovoiturage, on_delete=models.CASCADE)
    score_match = models.FloatField(blank=True, null=True)

class Conversation(models.Model):
    utilisateur1 = models.ForeignKey('accounts.Utilisateur', related_name='conversations_utilisateur1', on_delete=models.CASCADE)
    utilisateur2 = models.ForeignKey('accounts.Utilisateur', related_name='conversations_utilisateur2', on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    expediteur = models.ForeignKey('accounts.Utilisateur', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

