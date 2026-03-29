from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


def _token_response(user: User) -> Response:
	refresh = RefreshToken.for_user(user)
	response = Response({'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
	response.set_cookie('access_token', str(refresh.access_token), httponly=True, samesite='Lax')
	response.set_cookie('refresh_token', str(refresh), httponly=True, samesite='Lax')
	return response


class RegisterView(generics.CreateAPIView):
	serializer_class = RegisterSerializer
	permission_classes = [permissions.AllowAny]

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		return _token_response(user)


class LoginView(APIView):
	permission_classes = [permissions.AllowAny]

	def post(self, request):
		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		return _token_response(user)


class LogoutView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		response = Response({'detail': 'Logged out'}, status=status.HTTP_200_OK)
		response.delete_cookie('access_token')
		response.delete_cookie('refresh_token')
		return response


class RefreshTokenView(APIView):
	permission_classes = [permissions.AllowAny]

	def post(self, request):
		token = request.COOKIES.get('refresh_token')
		if not token:
			return Response({'detail': 'Refresh token missing'}, status=status.HTTP_401_UNAUTHORIZED)

		refresh = RefreshToken(token)
		response = Response({'detail': 'Token refreshed'}, status=status.HTTP_200_OK)
		response.set_cookie('access_token', str(refresh.access_token), httponly=True, samesite='Lax')
		return response


class MeView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request):
		return Response(UserSerializer(request.user).data)

	def patch(self, request):
		serializer = UserSerializer(request.user, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)


class PublicFreelancerProfileView(generics.RetrieveAPIView):
	serializer_class = UserSerializer
	permission_classes = [permissions.AllowAny]
	queryset = User.objects.filter(role=User.Role.FREELANCER)
