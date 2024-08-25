from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import ( 
    Laboratory, Equipment, SubEquipment
)
from .serializers import ( 
    LaboratoryListSerializer, LaboratoryDetailSerializer,
    EquipmentListSerializer, EquipmentDetailSerializer,
    SubEquipmentListSerializer, SubEquipmentDetailSerializer
)

# Create your views here.
class LaboratoryListView(generics.ListCreateAPIView):
    serializer_class = LaboratoryListSerializer

    def get_queryset(self):
        user = self.request.user
        organization = user.organization
        return Laboratory.objects.filter(organization=organization, is_active=True)        

    def create(self, request, *args, **kwargs):
        try: 
            response = super().create(request, *args, **kwargs)
            return Response(
                {'id': response.data['id'], 'message': 'Laboratory created successfully'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LaboratoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LaboratoryDetailSerializer

    def get_object(self):
        return get_object_or_404(Laboratory, pk=self.kwargs['pk'])
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response(
            {'id': response.data['id'], 'message': 'Laboratory retrieved successfully'},
            status=status.HTTP_200_OK
        )
    
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return Response(
                {'id': response.data['id'], 'message': 'Laboratory updated successfully'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request, *args, **kwargs)
            return Response(
                {'message': 'Laboratory deleted successfully'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EquipmentListView(generics.ListCreateAPIView):
    serializer_class = EquipmentListSerializer

    def get_queryset(self):
        laboratory_id = self.kwargs['laboratory_id']
        return Equipment.objects.filter(laboratory_id=laboratory_id, is_active=True)     

    def create(self, request, *args, **kwargs):
        try: 
            response = super().create(request, *args, **kwargs)
            return Response(
                {'id': response.data['id'], 'message': 'Equipment created successfully'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class EquipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    pass

class SubEquipmentListView(generics.ListCreateAPIView):
    serializer_class = SubEquipmentListSerializer

    def get_queryset(self):
        equipment_id = self.kwargs['equipment_id']
        return SubEquipment.objects.filter(equipment_id=equipment_id, is_active=True)  

    def create(self, request, *args, **kwargs):
        try: 
            response = super().create(request, *args, **kwargs)
            return Response(
                {'id': response.data['id'], 'message': 'SubEquipment created successfully'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SubEquipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    pass