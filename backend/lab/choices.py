from django.db import models

class Priority(models.TextChoices):
    A = '15 business days'
    B = '8 to 10 business days'
    C = '3 to 5 business days'

class FinalDisposition(models.TextChoices):
    RETURN_TO_CLIENT = 'Return to client'
    TOTAL_DESTRUCTION = 'Total destruction'
    WASTE_DISPOSAL = 'Waste disposal'
    SEWER_DISPOSAL = 'Sewer disposal'

class SampleType(models.TextChoices):
    COMPOSITION = 'Composition'
    SPOT = 'Spot'

class StateOfMatter(models.TextChoices):
    LIQUID = 'Liquid'
    SOLID = 'Solid'
    GAS = 'Gas'
    OTHER = 'Other'