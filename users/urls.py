from django.urls import path
from .views import SearchUserView, FriendRequestView, handle_friend_request, FriendListView, PendingFriendRequestsView, login_view, SignupView

urlpatterns = [
    path('search/', SearchUserView.as_view(), name='search_users'),
    path('friend-request/', FriendRequestView.as_view(), name='send_friend_request'),
    path('friend-requests/pending/', PendingFriendRequestsView.as_view(), name='pending_friend_requests'),
    path('friend-requests/<uuid:pk>/<str:action>/', handle_friend_request, name='handle_friend_request'),
    path('friends/', FriendListView.as_view(), name='list_friends'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
]
