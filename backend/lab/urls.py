from django.urls import path
from .views import (
    LaboratoryListView, LaboratoryDetailView,
    EquipmentListView, EquipmentDetailView,
    SubEquipmentListView, SubEquipmentDetailView
)

urlpatterns = [
    path('laboratories/', LaboratoryListView.as_view(), name='laboratory-list'),
    path('laboratories/<str:pk>/', LaboratoryDetailView.as_view(), name='laboratory-detail'),

    path('laboratories/<str:pk>/equipments/', EquipmentListView.as_view(), name='equipment-list'),

    path('equipment/<str:pk>/subequipments/', SubEquipmentListView.as_view(), name='subequipment-list'),
]