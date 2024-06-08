from rest_framework import generics, status, permissions
from .serializers import UserRegSerializer, UserUpdateLogsSerializer
from .models import Userprofile
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User


class UserRegView(generics.CreateAPIView):
    queryset = Userprofile.objects.all()
    serializer_class = UserRegSerializer  # Use your custom serializer
    permission_classes = [AllowAny]  # Allow unauthenticated users to register

class UserUpdateLogsView(generics.UpdateAPIView):
    queryset = Userprofile.objects.all()
    serializer_class = UserUpdateLogsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Assuming phone number is used to fetch the profile, adjust as necessary
        phone = self.request.data.get('phone')
        return Userprofile.objects.get(phone=phone)

class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = Userprofile.objects.all()
    serializer_class = UserRegSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter the queryset to only include the Userprofile associated with the authenticated user
        return Userprofile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically associate the created Userprofile with the authenticated user
        serializer.save(user=self.request.user)

class UserProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Userprofile.objects.all()
    serializer_class = UserRegSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the Userprofile associated with the authenticated user
        return self.request.user.userprofile

# You can create more views for user profile management as needed.
class UserLoginView(ObtainAuthToken):
    """Custom login view to generate authentication token."""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.request.user
        if user.is_authenticated:
            user_profile = user.userprofile
        return response

class FollowUserView(generics.UpdateAPIView):
    queryset = Userprofile.objects.all()
    serializer_class = UserProfileSerializer  # Use your custom user profile serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user_to_follow = self.get_object()
        if self.request.user == user_to_follow :
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        # Implement logic to follow the user
        self.request.user.profile.following.add(user_to_follow)
        return Response(status=status.HTTP_200_OK)

class UnfollowUserView(generics.UpdateAPIView):
    queryset = Userprofile.objects.all()
    serializer_class = UserProfileSerializer  # Use your custom user profile serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user_to_unfollow = self.get_object()

        # Check if the user is already followed
        if user_to_unfollow in request.user.profile.following.all():
            # Unfollow the user
            request.user.profile.following.remove(user_to_unfollow)
            return Response({"detail": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": f"You are not following {user_to_unfollow.username}."}, status=status.HTTP_400_BAD_REQUEST)
        

class ListFollowersView(generics.ListAPIView):
    serializer_class = UserProfileSerializer  # Use your custom user profile serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.profile.followers.all()

class ListFollowingView(generics.ListAPIView):
    serializer_class = UserProfileSerializer  # Use your custom user profile serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.profile.following.all()