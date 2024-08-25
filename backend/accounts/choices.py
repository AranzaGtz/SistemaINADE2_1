from django.db import models

class Country(models.TextChoices):
    US = 'Estados Unidos' 
    CA = 'Cánada'
    MX = 'México'
    FR = 'Francia'
    DE = 'Alemania'
    SP = 'España'

class Role(models.TextChoices):
    ADMIN = 'Administrador'
    LABORATORIST = 'Laboratorista'
    CUSTOMER = 'Cliente'