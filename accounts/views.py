from .models import  Profile
from .serializers import UserSerializer, ProfileSerializer,UserRegistrationSerializer,UserLoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from django.utils.encoding import force_bytes
from rest_framework import status
from django.contrib import messages
from .permissions import IsStaffOrReadOnly
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import NotFound

class UserViewSet(viewsets.ModelViewSet):
    # queryset = User.objects.all()
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsStaffOrReadOnly] 

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise NotAuthenticated("User is not authenticated.")
        
        queryset = Profile.objects.filter(user=self.request.user)
        
        if not queryset.exists():
            raise NotFound("Profile not found for the user.")
        
        return queryset



class UserRegistrationSerializerViewSet(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            confirm_link = f"https://school-management-five-iota.vercel.app/accounts/active/{uid}/{token}/"
            email_subject = "Confirm Your Email"
            email_body = render_to_string(
                'confirm_email.html', {'confirm_link': confirm_link})

            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")

            email.send()

            return Response('Check your email for confirmation')
        return Response(serializer.errors)


User = get_user_model()


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
    except (TypeError, ValueError, UnicodeDecodeError):
        return redirect('verified_unsuccess')

    user = get_object_or_404(User, pk=uid)

    if default_token_generator.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save()
        return redirect('verified_success')
    else:
        return redirect('verified_unsuccess')


class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username_or_email = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            if "@" in username_or_email:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(username=user_obj.username, password=password)
            else:
                user = user = authenticate(username=username_or_email, password=password)
          
            if user is not None and user.is_active:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'message':'successfully login.\n','token': token.key, 'user_id': user.id, 'is_staff': user.is_staff }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class UserLogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.auth_token:
            request.user.auth_token.delete()
        logout(request)
        messages.success(request, "Successfully logged out.")
        return redirect('login')

# email confirm success message
def successful(request):
    return render(request, 'successful.html')

# email confirm unsuccessful message
def unsuccessful(request):
    return render(request, 'unsuccessful.html')





from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UserDetailSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the logged-in user's profile
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()  # Get the current user
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        # Check if the data is valid
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
