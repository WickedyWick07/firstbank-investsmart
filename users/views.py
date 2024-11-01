from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response 
from rest_framework import status 
from django.contrib.auth import authenticate, login 
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, CustomUserSerializer
from django.views.decorators.csrf import csrf_exempt
import logging
from django.http import HttpResponse, JsonResponse
from functools import wraps

logger = logging.getLogger(__name__)

def cors_handler(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.method == 'OPTIONS':
            response = HttpResponse()
            response["Access-Control-Allow-Origin"] = "https://firstbank-investments.vercel.app"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Max-Age"] = "86400"  # 24 hours
            return response
        return view_func(request, *args, **kwargs)
    return wrapped_view

@api_view(['POST', 'OPTIONS'])
@permission_classes([AllowAny])
@cors_handler
def login(request):
    logger.info(f"Login attempt - Method: {request.method}, Headers: {request.headers}")
    
    if request.method == 'POST':
        try:
            serializer = LoginSerializer(data=request.data)
            
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')
                
                user = authenticate(email=email, password=password)
                logger.info(f"Authentication result for {email}: {'Success' if user else 'Failed'}")
                
                if user is not None:
                    refresh = RefreshToken.for_user(user)
                    response_data = {
                        'success': True,
                        'message': 'Login Successful',
                        'access': str(refresh.access_token),
                        'refresh': str(refresh)
                    }
                    response = Response(response_data, status=status.HTTP_200_OK)
                    return response
                else:
                    return Response(
                        {'error': 'Invalid credentials'}, 
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            else:
                logger.error(f"Serializer errors: {serializer.errors}")
                return Response(
                    serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST', 'OPTIONS'])
@permission_classes([AllowAny])
@cors_handler
def register(request):
    logger.info(f"Registration attempt - Method: {request.method}, Headers: {request.headers}")
    
    if request.method == 'POST':
        try:
            serializer = CustomUserSerializer(data=request.data)
            
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                response_data = {
                    'success': True,
                    'message': 'Registration Successful',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
                response = Response(response_data, status=status.HTTP_201_CREATED)
                return response
            else:
                logger.error(f"Serializer errors: {serializer.errors}")
                return Response(
                    serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET', 'OPTIONS'])
@permission_classes([IsAuthenticated])
@cors_handler
def current_user(request):
    logger.info(f"Current user request - User: {request.user.email}")
    try:
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Current user error: {str(e)}")
        return Response(
            {'error': 'Internal server error'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )