from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Steeze, SteezeLikes, SteezeCom
from .serializers import (
    SteezeSerializer, SteezeLikesSerializer, SteezeComSerializer,
)
from .permissions import IsOwnerOrReadOnly  # Custom permission class if needed
from rest_framework.authentication import TokenAuthentication  # Token-based authentication
from datetime import datetime, timedelta

# Views for the Steeze model
class SteezeListCreateView(generics.ListCreateAPIView):
    queryset = Steeze.objects.all()
    serializer_class = SteezeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)

class SteezeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Steeze.objects.all()
    serializer_class = SteezeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.poster != self.request.user:
            raise permissions.PermissionDenied("You don't have permission to edit this object.")

    def perform_destroy(self, instance):
        if instance.poster == self.request.user:
            instance.delete()
        else:
            raise permissions.PermissionDenied("You don't have permission to delete this object.")

# Views for liking a Steeze
class SteezeLikesCreateView(generics.CreateAPIView):
    queryset = SteezeLikes.objects.all()
    serializer_class = SteezeLikesSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        steeze = get_object_or_404(Steeze, pk=self.kwargs['steeze_id'])
        serializer.save(liker=self.request.user, stz=steeze)

class SteezeLikesDestroyView(generics.DestroyAPIView):
    queryset = SteezeLikes.objects.all()
    serializer_class = SteezeLikesSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        steeze = get_object_or_404(Steeze, pk=self.kwargs['steeze_id'])
        if instance.liker == self.request.user and instance.stz == steeze:
            instance.delete()
        else:
            raise permissions.PermissionDenied("You don't have permission to delete this object.")

# Views for commenting on a Steeze
class SteezeComListCreateView(generics.ListCreateAPIView):
    queryset = SteezeCom.objects.all()
    serializer_class = SteezeComSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        steeze = get_object_or_404(Steeze, pk=self.kwargs['steeze_id'])
        serializer.save(commentor=self.request.user, stz=steeze)

class SteezeComRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SteezeCom.objects.all()
    serializer_class = SteezeComSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.commentor != self.request.user:
            raise permissions.PermissionDenied("You don't have permission to edit this object.")

    def perform_destroy(self, instance):
        if instance.commentor == self.request.user:
            instance.delete()
        else:
            raise permissions.PermissionDenied("You don't have permission to delete this object.")

# Function to expire Steezes after 72 hours
def expire_steezes():
    expiration_time = datetime.now() - timedelta(hours=72)
    Steeze.objects.filter(steez_time__lte=expiration_time).delete()
