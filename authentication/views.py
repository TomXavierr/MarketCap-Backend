from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import UserSerializer


from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()

# Create your views here.


# @api_view(['POST'])
# def login(request):
#     user = get_object_or_404(User, username=request.data['username'])
#     if not user.check_password(request.data['password']):
#         return Response("missing user", status=status.HTTP_404_NOT_FOUND)
#     token, created = Token.objects.get_or_create(user=user)
#     serializer = UserSerializer(user)
#     return Response({'token': token.key, 'user': serializer.data})



class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]




# @api_view(['POST'])
# def signup(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         user = User.objects.get(username=request.data['username'])
#         user.set_password(request.data['password'])
#         user.save()

#         token = Token.objects.create(user=user)
#         return Response({"token": token.key, "user": serializer.data})

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

