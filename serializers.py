from rest_framework import serializers
from .models import Client, Mecanicien, Voiture, Rendezvous, Facture

class ClientSerializer(serializers.ModelSerializer):
    # Accéder aux attributs de l'utilisateur associé
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
   
    mot_de_passe = serializers.CharField(read_only=True)  # Pour ne pas renvoyer le mot de passe dans les réponses

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'date_naissance', 'mot_de_passe', 'user']  # les autres champs nécessaires


class MecanicienSerializer(serializers.ModelSerializer):
     first_name = serializers.CharField(source='user.first_name')
     last_name = serializers.CharField(source='user.last_name')
     email = serializers.EmailField(source='user.email')
   
     mot_de_passe = serializers.CharField(read_only=True)  # Pour ne pas renvoyer le mot de passe dans les réponses

     class Meta:
        model = Mecanicien
        fields = ['id', 'first_name', 'last_name', 'email', 'date_naissance', 'mot_de_passe', 'specialite','user']
from rest_framework import serializers
from .models import Voiture

class VoitureSerializer(serializers.ModelSerializer):
    # Affichage du prénom et du nom de l'utilisateur (lecture seule)
    client_first_name = serializers.CharField(source='client.user.first_name', read_only=True)
    client_last_name = serializers.CharField(source='client.user.last_name', read_only=True)

    class Meta:
        model = Voiture
        fields = [
            'id', 'client', 'marque', 'modele', 'annee', 
            'immatriculation', 'client_first_name', 'client_last_name'
        ]

class RendezvousSerializer(serializers.ModelSerializer):
    # Affichage du prénom et du nom du client
    client_first_name = serializers.CharField(source='client.user.first_name',read_only=True)
    client_last_name = serializers.CharField(source='client.user.last_name',read_only=True)

    # Affichage du prénom et du nom du mécanicien
    mecanicien_first_name = serializers.CharField(source='mecanicien.user.first_name',read_only=True)
    mecanicien_last_name = serializers.CharField(source='mecanicien.user.last_name',read_only=True)

    class Meta:
        model = Rendezvous
        fields = ['id', 'client', 'mecanicien', 'voiture', 'date', 'symptomes', 'accepte', 
                  'client_first_name', 'client_last_name', 
                  'mecanicien_first_name', 'mecanicien_last_name']

class FactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facture
        fields = ['id', 'rendezvous', 'cout_service', 'benefice']
