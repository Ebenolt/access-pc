from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.sayHello),
    path('bye/', views.sayGoodbye),
]
