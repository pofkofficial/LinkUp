from django.urls import path
from . import views, UserRegView, user_views, flags_views, event_views, chat_views, steeze_views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('registration/', user_views.UserRegView.as_view(), name='Registration'),
    path('logs_update/', user_views.UserUpdateLogsView.as_view(), name='Update username and password'),

    # Event URLs
    path('events/', event_views.EventsListCreateView.as_view(), name='event-list'),
    path('events/<int:pk>/', event_views.EventsRetrieveUpdateDestroyView.as_view(), name='event-detail'),

    # Flags URLs
    path('flags/', flags_views.FlagsListCreateView.as_view(), name='flags-list'),
    path('flags/<int:pk>/', flags_views.FlagsRetrieveUpdateDestroyView.as_view(), name='flags-detail'),

    # Chat URLs
    path('chats/', chat_views.ChatListCreateView.as_view(), name='chat-list'),
    path('chats/<int:pk>/', chat_views.ChatRetrieveUpdateDestroyView.as_view(), name='chat-detail'),

    # Message URLs
    path('messages/', chat_views.MessageListCreateView.as_view(), name='message-list'),
    path('messages/<int:pk>/', chat_views.MessageRetrieveUpdateDestroyView.as_view(), name='message-detail'),

    # Steeze URLs
    path('steezes/', steeze_views.SteezeListCreateView.as_view(), name='steeze-list'),
    path('steezes/<int:pk>/', steeze_views.SteezeRetrieveUpdateDestroyView.as_view(), name='steeze-detail'),

    # SteezeCom URLs
    path('steezecom/', steeze_views.SteezeComListCreateView.as_view(), name='steezecom-list'),
    path('steezecom/<int:pk>/', steeze_views.SteezeComRetrieveUpdateDestroyView.as_view(), name='steezecom-detail'),

    # SteezeLikes URLs
    path('steezelikes/', steeze_views.SteezeLikesCreateView.as_view(), name='steezelikes-list'),
    path('steezelikes/<int:pk>/', steeze_views.SteezeLikesDestroyView.as_view(), name='steezelikes-detail'),

    # Following and followers views
    path('follow/<int:pk>/', user_views.FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:pk>/', user_views.UnfollowUserView.as_view(), name='unfollow-user'),
    path('followers/', user_views.ListFollowersView.as_view(), name='list-followers'),
    path('following/', user_views.ListFollowingView.as_view(), name='list-following'),

    # User-related views
    path('userprofiles/', user_views.UserProfileListCreateView.as_view(), name='userprofile-list-create'),
    path('userprofile/<int:pk>/', user_views.UserProfileRetrieveUpdateDestroyView.as_view(), name='userprofile-detail'),
    path('login/', user_views.UserLoginView.as_view(), name='user-login'),
]