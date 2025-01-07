

# Register your models here.
from django.contrib import admin
from .models import  Client, Mecanicien, Voiture, Rendezvous, Facture

admin.site.register(Client)
admin.site.register(Mecanicien)
admin.site.register(Voiture)
admin.site.register(Rendezvous)
admin.site.register(Facture)
