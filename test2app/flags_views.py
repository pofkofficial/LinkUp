from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404  # Import get_object_or_404
from .models import Flags
from .serializers import FlagsSerializer
from rest_framework.authentication import TokenAuthentication
from datetime import timedelta, datetime  # Import timedelta and datetime

class FlagsListCreateView(generics.ListCreateAPIView):
    queryset = Flags.objects.all()
    serializer_class = FlagsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        flag_type = serializer.validated_data['flag_type']
        
        # Check if the user already has a flag of the same type
        user_flag = get_object_or_404(Flags, user=self.request.user, flag_type=flag_type)
        if user_flag:
            raise permissions.PermissionDenied(f"You can only create one {flag_type} flag.")
        
        # Set the created_at field
        created_at = datetime.now()
        serializer.save(user=self.request.user, created_at=created_at)

        # Check if flag_type is flag_1 and delete after 12 hours
        if flag_type == 'flag_1':
            expiration_time = created_at + timedelta(hours=12)
            if expiration_time <= datetime.now():
                serializer.instance.delete()

class FlagsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flags.objects.all()
    serializer_class = FlagsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.user != self.request.user:
            raise permissions.PermissionDenied("You don't have permission to edit this object.")

    def perform_destroy(self, instance):
        if instance.flag_type == 'flag_1' and instance.created_at + timedelta(hours=12) <= datetime.now():
            # Flag_1 can be deleted after 12 hours
            super().perform_destroy(instance)
        elif instance.flag_type == 'flag_2' and instance.created_at + timedelta(hours=48) <= datetime.now():
            # Flag_2 can be deleted automatically after 48 hours
            super().perform_destroy(instance)
        else:
            raise permissions.PermissionDenied("You can't delete this flag yet.")
