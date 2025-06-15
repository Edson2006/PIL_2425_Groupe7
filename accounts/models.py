from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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
    
    # CORRECTION: Ajout des related_name pour résoudre le conflit
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="utilisateur_set", # Nom unique pour l'accès inverse
        related_query_name="utilisateur",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="utilisateur_set", # Nom unique pour l'accès inverse
        related_query_name="utilisateur",
    )

    objects = UtilisateurManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'telephone']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"

    def get_short_name(self):
        return self.prenom

    def get_role_display(self):
        return dict(self.ROLE_CHOICES).get(self.role, self.role)

    def is_driver(self):
        return self.role == 'conducteur'


class ProfilUtilisateur(models.Model):
    utilisateur = models.OneToOneField('accounts.Utilisateur', on_delete=models.CASCADE, primary_key=True)
    photo_profil = models.ImageField(upload_to='profils/', blank=True, null=True)
    point_depart = models.CharField(max_length=255, blank=True, null=True)
    horaires_depart = models.TimeField(blank=True, null=True)
    horaires_arrivee = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Profil de {self.utilisateur.email}"

class Vehicule(models.Model):
    
    utilisateur = models.OneToOneField(
        'accounts.Utilisateur', 
        on_delete=models.CASCADE,
        primary_key=True  
    )
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    nombre_places = models.PositiveIntegerField()
    plaque_immatriculation = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.marque} {self.modele} de {self.utilisateur.prenom}"

class OffreCovoiturage(models.Model):
    conducteur = models.ForeignKey('accounts.Utilisateur', on_delete=models.CASCADE)
    point_depart = models.CharField(max_length=255)
    point_arrivee = models.CharField(max_length=255)
    heure_depart = models.DateTimeField()
    places_disponibles = models.PositiveIntegerField()
    prix = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    commentaires = models.TextField(blank=True)

    def __str__(self):
        return f"Offre de {self.conducteur.prenom} de {self.point_depart} à {self.point_arrivee}"

class DemandeCovoiturage(models.Model):
    passager = models.ForeignKey('accounts.Utilisateur', on_delete=models.CASCADE)
    point_depart = models.CharField(max_length=255)
    point_arrivee = models.CharField(max_length=255)
    heure_souhaitee = models.DateTimeField()
    flexibilite = models.DurationField(help_text="Marge de flexibilité temporelle", default=timezone.timedelta(minutes=30))

    def __str__(self):
        return f"Demande de {self.passager.prenom} de {self.point_depart} à {self.point_arrivee}"

class Matching(models.Model):
    offre = models.ForeignKey(OffreCovoiturage, on_delete=models.CASCADE)
    demande = models.ForeignKey(DemandeCovoiturage, on_delete=models.CASCADE)
    score_match = models.FloatField(blank=True, null=True)
    date_match = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['offre', 'demande']]

class Conversation(models.Model):
    offre = models.ForeignKey(OffreCovoiturage, on_delete=models.CASCADE, blank=True, null=True)
    demande = models.ForeignKey(DemandeCovoiturage, on_delete=models.CASCADE, blank=True, null=True)
    utilisateur1 = models.ForeignKey('accounts.Utilisateur', related_name='conversations_initiees', on_delete=models.CASCADE)
    utilisateur2 = models.ForeignKey('accounts.Utilisateur', related_name='conversations_recues', on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    derniere_activite = models.DateTimeField(auto_now=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    expediteur = models.ForeignKey('accounts.Utilisateur', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)