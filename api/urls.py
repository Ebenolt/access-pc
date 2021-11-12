from django.urls import path
from . import views
from . import views_v1

urlpatterns = [
    path('', views.bad_endpoint),
    path('v1/', views_v1.hello.as_view()),
    path('v1/users/', views_v1.allUsersView.as_view()),
    path('v1/user/', views_v1.userView.as_view()),
    path('v1/user/<int:user_id>', views_v1.userView.as_view()),
    path('v1/clients/', views_v1.allClientView.as_view()),
    path('v1/client/', views_v1.clientView.as_view()),
    path('v1/client/<int:client_id>', views_v1.clientView.as_view()),
    path('v1/connect', views_v1.connect.as_view()),
]

