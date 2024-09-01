from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import (
    Organization, Address, Configuration
)
from .serializers import (
    OrganizationListSerializer, OrganizationDetailSerializer,
    AddressListSerializer, AddressDetailSerializer,
)

# Create your views here.

class OrganizationListView(generics.ListCreateAPIView):
    serializer_class = OrganizationListSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Organization.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        try: 
            response = super().create(request, *args, **kwargs)
            return Response(
                {'id': response.data['id'], 'message': 'Organization created successfully'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
    pass

class AddressCreateView(generics.CreateAPIView):
    serializer_class = AddressListSerializer

    def create(self, request, *args, **kwargs):
        try: 
            response = super().create(request, *args, **kwargs)
            return Response(
                {'id': response.data['id'], 'message': 'Address created successfully'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressDetailSerializer

    def get_object(self):
        address_id = self.kwargs.get('pk')
        return get_object_or_404(Address, id=address_id)