from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_naissance = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Client:  {self.user.first_name} {self.user.last_name}"
# Mecanicien dérive de User
class Mecanicien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialite = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Mécanicien: {self.user.first_name} {self.user.last_name} - Spécialité: {self.specialite}"

# Modèle de Voiture
class Voiture(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="voitures")
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    annee = models.IntegerField()
    immatriculation = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.annee})"

# Modèle de Rendez-vous
class Rendezvous(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    mecanicien = models.ForeignKey(Mecanicien, on_delete=models.CASCADE)
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    date = models.DateTimeField()
    symptomes = models.TextField()
    accepte = models.BooleanField(default=False)

    def __str__(self):
        return f"Rendez-vous {self.id} - {self.client.user.first_name} {self.client.user.last_name}"

# Modèle de Facture
class Facture(models.Model):
    rendezvous = models.ForeignKey(Rendezvous, on_delete=models.CASCADE)
    cout_service = models.DecimalField(max_digits=10, decimal_places=2)
    benefice = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Facture pour Rendez-vous {self.rendezvous.id}"
