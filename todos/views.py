import email
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ChangePasswordSerializer, TodoSerializer, UserAuthSerializer
from .models import Todo, User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    """End point for loging in. The user must provide password and email. A token pair including refresh token will be returned """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.get_full_name()
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SignupApi(APIView):
    """
    End point for signing up(creating user account)
    """
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = UserAuthSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokenpair = MyTokenObtainPairSerializer.get_token(user)
            data = {
                "refresh": str(tokenpair),
                "access": str(tokenpair.access_token)
            }
            print(tokenpair)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class ChangePassword(APIView):
    """
    endpoint view for changing password
    """
    permission_classes = (IsAuthenticated, )

    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllTodos(APIView):
    """
    List all todos or create new todo. Only authenticated users can see their todos
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        params = request.query_params
        todos = []
        if 'status' not in params:
            todos = Todo.objects.filter(owner=user)
        else:
            todos = Todo.objects.filter(owner=user, status=params['status'])
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user = self.request.user
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetail(APIView):
    """
    Edit a todo object's specific field or delete a todo
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk, format=None):
        user = self.request.user
        todo = Todo.objects.get(owner=user, id=pk)
        if todo is None:
            return Response({"error": "specified item was not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, _, pk, format=None):
        user = self.request.user
        todo = Todo.objects.get(owner=user, id=pk)
        if todo is None:
            return Response({"error": "specified item was not found"}, status=status.HTTP_404_NOT_FOUND)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
