from django.db import models

class Country(models.TextChoices):
    US = 'Estados Unidos' 
    CA = 'Cánada'
    MX = 'México'
    FR = 'Francia'
    DE = 'Alemania'
    SP = 'España'

class Role(models.TextChoices):
    ADMIN = 'Admin'
    LABORATORIST = 'Laboratorist'
    CUSTOMER = 'Customer'

class Gender(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'
    UNKNOWN = 'Unknown'

class Priority(models.IntegerChoices):
    LOW = 0, 'Low'
    MEDIUM = 1, 'Medium'
    HIGH = 2, 'High'