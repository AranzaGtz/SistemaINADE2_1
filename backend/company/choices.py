from django.db import models

class Currency(models.TextChoices):
    MXN = 'MXN', 'MXN - Peso mexicano'
    USD = 'USD', 'USD - Dólar estadounidense'

class VAT(models.IntegerChoices):
    EIGHT_PERCENT = 8
    SIXTEEN_PERCENT = 16