from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Custom login view for API authentication
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout_view(request):
    """
    Custom logout view for API authentication
    """
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
