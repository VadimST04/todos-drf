from django.contrib.auth.models import User
from rest_framework import serializers

from todos.models import Todo


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    class Meta:
        """
        model (Model): The User model.
        fields (list): The fields to be included in the serialized output.
        """

        model = User
        fields = ['username', 'email', 'password', ]


class TodoSerializer(serializers.ModelSerializer):
    """
    Serializer for Todos objects.
    """

    class Meta:
        """
        model (Model): The Todos model.
        fields (list): The fields to be included in the serialized output.
        """

        model = Todo
        fields = ['id', 'text', ]
