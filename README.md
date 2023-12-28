### Hello! My name is Vadym. I am a Junior Python Developer.
#### This is my simple todos API.

<br />

To design this API, I used <b>Django Rest Framework</b>

By using this API, you can:
+ Register a new user
+ Login by providing your email and password
+ Create new todos
+ Delete todos
+ Update todos
+ List all todos

To login users, I used <a href="https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html">Simple JWT</a>:
```python
...
path('api/user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
...
```
To register new users, I created a custom function based on generics.CreateAPIView:
```python
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

```

To design the CRUD operation, I used generics and only allowed authorized users to do it:
```python
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
```

To serialize all data, I created UserRegistrationSerializer and TodoSerializer:
```python
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
```
