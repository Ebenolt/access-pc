from django.contrib import admin
from . models import Client
from . models import Devis
from . models import Facture
from . models import Connexion
from . models import Message
from . models import Tarif

admin.site.register(Client)
admin.site.register(Devis)
admin.site.register(Facture)
admin.site.register(Connexion)
admin.site.register(Message)
admin.site.register(Tarif)
