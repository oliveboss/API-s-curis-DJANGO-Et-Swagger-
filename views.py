from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Client, Mecanicien, Voiture, Rendezvous, Facture
from .serializers import ClientSerializer, MecanicienSerializer, VoitureSerializer, RendezvousSerializer, FactureSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
import requests
from django.http import JsonResponse
from django.shortcuts import render

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]  # Protection par JWT
def create(self, request):
    """
    Créer un nouveau client.
    """
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        # Extraire les données utilisateur
        user_data = serializer.validated_data.pop('user')
        mot_de_passe = serializer.validated_data.pop('mot_de_passe', None)

        # Créer l'utilisateur associé
        user = User.objects.create(
            username=user_data['username'],
            email=user_data['email'],
            password=make_password(mot_de_passe) if mot_de_passe else None
        )

        # Associer l'utilisateur au client
        client = Client.objects.create(user=user, **serializer.validated_data)

        # Repasser par le sérialiseur pour retourner les données au bon format
        response_serializer = ClientSerializer(client)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        """
        Met à jour un client existant.
        """
        client = Client.objects.get(pk=pk)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            # Si un mot de passe est fourni, on le chiffre
            password = serializer.validated_data.get('mot_de_passe', None)
            if password:
                serializer.validated_data['user'].password = make_password(password)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Supprime un client.
        """
        client = Client.objects.get(pk=pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# ViewSet pour les Mécaniciens
class MecanicienViewSet(viewsets.ModelViewSet):
   
    serializer_class = MecanicienSerializer
    permission_classes = [IsAuthenticated]  # Protection par JWT
    def get_queryset(self):
        """
        Un client peut voir la liste des mécaniciens
        """
        if hasattr(self.request.user, 'client'):
            return Mecanicien.objects.all()  # Les clients peuvent voir tous les mécaniciens
        return Mecanicien.objects.none()  # Les mécaniciens ne doivent pas accéder à cette liste    
    def create(self, request):
        """
        Créer un nouveau mécanicien.
        """
        serializer = MecanicienSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get('mot_de_passe', None)
            if password:
                serializer.validated_data['user'].password = make_password(password)
            mecanicien = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Met à jour un mécanicien existant.
        """
        mecanicien = Mecanicien.objects.get(pk=pk)
        serializer = MecanicienSerializer(mecanicien, data=request.data, partial=True)
        if serializer.is_valid():
            password = serializer.validated_data.get('mot_de_passe', None)
            if password:
                serializer.validated_data['user'].password = make_password(password)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Supprime un mécanicien.
        """
        mecanicien = Mecanicien.objects.get(pk=pk)
        mecanicien.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ViewSet pour les Voitures
class VoitureViewSet(viewsets.ModelViewSet):
   
    serializer_class = VoitureSerializer
    permission_classes = [IsAuthenticated]  # Protection par JWT
    def get_queryset(self):
        """
        Retourne les voitures associées au client connecté
        """
        user = self.request.user
        try:
            # Trouver le client lié à l'utilisateur authentifié
            client = user.client
        except Client.DoesNotExist:
            # Si l'utilisateur n'est pas un client, on ne retourne aucune voiture
            return Voiture.objects.none()

        # Retourner uniquement les voitures associées au client
        return Voiture.objects.filter(client=client)
    def create(self, request):
        """
        Créer une nouvelle voiture.
        """
        serializer = VoitureSerializer(data=request.data)
        if serializer.is_valid():
            voiture = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Met à jour une voiture existante.
        """
        voiture = Voiture.objects.get(pk=pk)
        serializer = VoitureSerializer(voiture, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Supprime une voiture.
        """
        voiture = Voiture.objects.get(pk=pk)
        voiture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# ViewSet pour les Rendez-vous
class RendezvousViewSet(viewsets.ModelViewSet):
    
    serializer_class = RendezvousSerializer
    permission_classes = [IsAuthenticated]  # Protection par JWT
    def get_queryset(self):
        """
        Liste des rendez-vous en fonction du rôle de l'utilisateur
        """
        if hasattr(self.request.user, 'client'):
            # Les clients peuvent voir leurs rendez-vous
            return Rendezvous.objects.filter(client=self.request.user.client)
        elif hasattr(self.request.user, 'mecanicien'):
            # Les mécaniciens peuvent voir les rendez-vous auxquels ils sont associés
            return Rendezvous.objects.filter(mecanicien=self.request.user.mecanicien)
        return Rendezvous.objects.none()  # Si l'utilisateur n'est ni client ni mécanicien   
    def create(self, request):
        """
        Créer un nouveau rendez-vous.
        """
        if not hasattr(self.request.user, 'mecanicien'):
            return Response({"detail": "Accès interdit. Vous devez être un mécanicien pour créer une facture."}, status=status.HTTP_403_FORBIDDEN)

        serializer = RendezvousSerializer(data=request.data)
        if serializer.is_valid():
            rendezvous = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Met à jour un rendez-vous existant.
        """
        if not hasattr(self.request.user, 'mecanicien'):
            return Response({"detail": "Accès interdit. Vous devez être un mécanicien pour mettre à jour une facture."}, status=status.HTTP_403_FORBIDDEN)
        rendezvous = Rendezvous.objects.get(pk=pk)
        serializer = RendezvousSerializer(rendezvous, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Supprime un rendez-vous.
        """
        # Vérifie si l'utilisateur est un mécanicien
        if not hasattr(self.request.user, 'mecanicien'):
            return Response({"detail": "Accès interdit. Vous devez être un mécanicien pour supprimer une facture."}, status=status.HTTP_403_FORBIDDEN)

        rendezvous = Rendezvous.objects.get(pk=pk)
        rendezvous.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# ViewSet pour les Factures
class FactureViewSet(viewsets.ModelViewSet):
  
    serializer_class = FactureSerializer
    permission_classes = [IsAuthenticated]  # Protection par JWt
    def get_queryset(self):
        """
        Les clients et mécaniciens ont accès à la liste des factures
        """
        if hasattr(self.request.user, 'client'):
            # Les clients peuvent voir leurs factures
            return Facture.objects.filter(client=self.request.user.client)
        elif hasattr(self.request.user, 'mecanicien'):
            # Les mécaniciens peuvent voir les factures pour leurs rendez-vous
            return Facture.objects.filter(rendezvous__mecanicien=self.request.user.mecanicien)
        return Facture.objects.none()  # Si l'utilisateur n'est ni client ni mécanicien
    def create(self, request):
        """
        Créer une nouvelle facture.
        """
        serializer = FactureSerializer(data=request.data)
        if serializer.is_valid():
            facture = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Met à jour une facture existante.
        """
        facture = Facture.objects.get(pk=pk)
        serializer = FactureSerializer(facture, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Supprime une facture.
        """
        facture = Facture.objects.get(pk=pk)
        facture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


import requests

def get_auth_token():
    url = "http://127.0.0.1:8000/api/token/"
    credentials = {"username": "olive", "password": "2004"}
    response = requests.post(url, data=credentials)
    response.raise_for_status()
    return response.json().get("access")

def fetch_count(url, token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Vérifie que le statut HTTP est 200
        data = response.json()
        return len(data) if isinstance(data, list) else 0
    except Exception as e:
        print(f"Erreur lors de la récupération des données depuis {url}: {e}")
        return 0

def stats_view(request):
    # Obtenez le jeton d'authentification
    token = get_auth_token()

    # Récupérez les données des API protégées avec authentification
    clients_count = fetch_count("http://127.0.0.1:8000/api/clients/", token)
    mecaniciens_count = fetch_count("http://127.0.0.1:8000/api/mecaniciens/", token)
    rendezvous_count = fetch_count("http://127.0.0.1:8000/api/rendezvous/", token)
    vehicules_count = fetch_count("http://127.0.0.1:8000/api/voitures/", token)

    # Passer les données au template
    context = {
        'clients_count': clients_count,
        'mecaniciens_count': mecaniciens_count,
        'rendezvous_count': rendezvous_count,
        'vehicules_count': vehicules_count,
    }
    return render(request, 'stats_page.html', context)
