from django.urls import path
from . import views
from . import views_v1

urlpatterns = [
    path('', views.bad_endpoint),
    path('v1/', views_v1.hello.as_view()), #GET
    path('v1/client/list/', views_v1.allClientView.as_view()), #GET, DELETE
    path('v1/client/add/', views_v1.clientView.as_view()), #POST
    path('v1/client/<int:client_id>', views_v1.clientView.as_view()), #GET, PATCH, DELETE
    path('v1/devis/list/', views_v1.allDevisView.as_view()), #GET, DELETE
    path('v1/devis/add/', views_v1.devisView.as_view()), #POST
    path('v1/devis/<int:devis_id>', views_v1.devisView.as_view()), #GET, PATCH, DELETE
    path('v1/facture/list', views_v1.allFactureView.as_view()), #GET, DELETE
    path('v1/facture/add/', views_v1.factureView.as_view()), #POST
    path('v1/facture/pay/<int:facture_id>', views_v1.payFactureView.as_view()), #POST
    path('v1/facture/<int:facture_id>', views_v1.factureView.as_view()), #GET, PATCH, DELETE
    path('v1/tarif/list/', views_v1.allTarifsView.as_view()), #GET, DELETE
    path('v1/tarif/add/', views_v1.tarifsView.as_view()), #POST
    path('v1/tarif/<int:tarif_id>', views_v1.tarifsView.as_view()), #GET, PATCH, DELETE
    path('v1/connect/', views_v1.connect.as_view()), #POST
]

