from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from todos.models import Todo
from todos.serializers import UserRegistrationSerializer, TodoSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    """
    API View for user registration.
    """

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user registration.
        :param request: The HTTP request object.
        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        :return: HTTP response containing the result of the registration attempt.
        """
        data = request.data

        try:
            if data['password'] != data['password_confirmation']:
                return Response({'detail': 'passwords are not equal!'}, status=status.HTTP_400_BAD_REQUEST)

            new_user = User.objects.create(
                username=data['email'],
                email=data['email'],
                password=make_password(data['password']),
            )

            serializer = UserRegistrationSerializer(new_user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError:
            return Response({'detail': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class TodosAPIView(generics.ListCreateAPIView,
                   generics.DestroyAPIView,
                   generics.UpdateAPIView):
    """
    API View for listing, creating, updating and deleting Todos objects.
    """

    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Get the queryset of Todos objects filtered by the current user.
        :return: The queryset of Todos objects.
        """
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Perform custom actions when creating a new Todos object.
        :param serializer: The serializer instance used for creating the Todos object.
        :return: None
        """
        serializer.save(user=self.request.user)
