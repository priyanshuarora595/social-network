from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, FriendRequest, Friendship
from .serializers import UserSerializer, FriendRequestSerializer, FriendshipSerializer
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
import uuid


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import UserSerializer
from django.db.utils import IntegrityError


class SignupView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Ensure email is case-insensitive
            email = request.data.get("email", "").lower()
            request.data["email"] = email

            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"detail": "A user with that email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email", "").lower()
    password = request.data.get("password", "")

    user = authenticate(request, email=email, password=password)
    if user is not None:
        # Generate tokens using Simple JWT
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
    else:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )
        


class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class SearchUserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = UserPagination

    def get_queryset(self):
        keyword = self.request.query_params.get("q", "").lower()
        if "@" in keyword:
            # If the keyword contains '@', assume it's an email search
            return CustomUser.objects.filter(email__iexact=keyword)
        else:
            # Search by name (case-insensitive, partial match)
            return CustomUser.objects.filter(
                Q(username__icontains=keyword)
                | Q(first_name__icontains=keyword)
                | Q(last_name__icontains=keyword)
            )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FriendRequestView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, serializer):
        sender = self.request.user
        receiver_id = self.request.data.get("receiver_id")

        if not receiver_id:
            return Response({"error": "Receiver ID is required."}, status=400)

        # Validate UUID format
        try:
            uuid.UUID(receiver_id)
        except ValueError:
            return Response({"error": "Invalid UUID format."}, status=400)

        # Manually check if the receiver exists
        try:
            receiver = CustomUser.objects.get(id=receiver_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        # Check if sender is trying to send a request to themselves
        if sender == receiver:
            return Response(
                {"error": "You cannot send a friend request to yourself."}, status=400
            )

        # Restrict sending more than 3 requests per minute
        last_minute = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(
            sender=sender, timestamp__gte=last_minute
        )
        if recent_requests.count() >= 3:
            return Response(
                {
                    "error": "You cannot send more than 3 friend requests within a minute."
                },
                status=429,
            )
        # Check if a friend request already exists
        existing_request = FriendRequest.objects.filter(
            sender=sender, receiver=receiver
        )
        if existing_request.exists():
            return Response(
                {"error": "Friend request already sent or exists."}, status=400
            )

        # Save the new friend request with default status
        self.request.data.update({"status": "pending"})
        serializer = self.get_serializer(data=self.request.data)

        if serializer.is_valid():
            serializer.save(sender=sender, receiver=receiver, status="pending")
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def handle_friend_request(request, pk, action):
    
    
    # Manually check if the receiver exists
    try:
        friend_request = FriendRequest.objects.get(id=pk)
    except FriendRequest.DoesNotExist:
        return Response({"error": "Request not found."}, status=404)
    
    # Check if the authenticated user is the receiver of the request
    if request.user != friend_request.receiver:
        return Response({"error": "You are not authorized to handle this friend request."}, status=403)
    
    # Check if the action is valid
    if action not in ["accept", "reject"]:
        return Response({"error": "Invalid action. Must be 'accept' or 'reject'."}, status=400)
    
    if action == "accept":
        Friendship.objects.create(user=request.user, friend=friend_request.sender)
        Friendship.objects.create(user=friend_request.sender, friend=request.user)
        friend_request.delete()
        return Response({"status": "accepted"})
    elif action == "reject":
        friend_request.delete()
        return Response({"status": "rejected"})


class FriendListView(generics.ListAPIView):
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Friendship.objects.filter(user=self.request.user)


class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(
            receiver=self.request.user, status="pending"
        )
