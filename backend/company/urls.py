from django.urls import path, include
from .views import (
    OrganizationListView, OrganizationDetailView,
    AddressCreateView, AddressDetailView
)

urlpatterns = [
    path('organizations/', OrganizationListView.as_view(), name='organization-list'),
    path('organizations/<str:pk>/', OrganizationDetailView.as_view(), name='organization-detail'),
    
    path('addresses/', AddressCreateView.as_view(), name='address-create'),
    path('addresses/<str:pk>/', AddressDetailView.as_view(), name='address-detail'),
]
