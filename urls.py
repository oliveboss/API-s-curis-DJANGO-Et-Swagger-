from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, MecanicienViewSet, VoitureViewSet, RendezvousViewSet, FactureViewSet,stats_view

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'mecaniciens', MecanicienViewSet, basename='mecanicien')
router.register(r'voitures', VoitureViewSet, basename='voiture')
router.register(r'rendezvous', RendezvousViewSet, basename='rendezvous')
router.register(r'factures', FactureViewSet, basename='facture')


# Incluez les URL générées par le routeur

urlpatterns = [
    path('', include(router.urls)),  # Les routes seront accessibles sous /api/
     path('statistiques/', stats_view, name='stats_view'),
]
