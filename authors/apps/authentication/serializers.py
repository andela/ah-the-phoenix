from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


from .models import User


def password_validator():
    return serializers.RegexField(
        regex=("^(?=.{8,}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*"),
        max_length=128,
        min_length=8,
        write_only=True,
        required=True,
        error_messages={
            'required': 'please ensure you have inserted a password',
            'min_length': 'password cannot be less than 8 characters',
            'max-length': 'password cannot be greater than 50 characters',
            'invalid': 'please consider a password that has a number, an '
                       'uppercase letter, lowercase letter and'
                       ' a special character',
        }
    )


def email_validator():
    return serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='user with this email already exists.'
            )
        ],
        error_messages={
            'required': 'Ensure the email is inserted',
            'invalid': 'Enter a valid email address.'
        }
    )


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.RegexField(
        regex=("^(?=.{8,}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*"),
        max_length=128,
        min_length=8,
        write_only=True,
        required=True,
        error_messages={
            'required': 'please ensure you have inserted a password',
            'min_length': 'password cannot be less than 8 characters',
            'max-length': 'password cannot be greater than 50 characters',
            'invalid': 'please consider a password that has a number, an '
            'uppercase letter, lowercase letter and a special character',
        }
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='user with this email already exists.'
            )
        ],
        error_messages={
            'required': 'Ensure the email is inserted',
            'invalid': 'Enter a valid email address.'
        }
    )
    username = serializers.RegexField(
        regex=("^[A-Za-z]*$"),
        max_length=128,
        min_length=2,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='user with this username already exists.'
            )
        ],
        error_messages={
            'required': 'please insert your username',
            'min_length': 'username cannot be less than 2 characters',
            'max_length': 'username cannot be greater than 128 characters',
            'invalid': 'username is invalid',
        }
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)


class EmailSerializer(serializers.ModelSerializer):

    """Ensure email is valid and it is inserted"""

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email']


class PasswordResetSerializer(EmailSerializer, serializers.ModelSerializer):

    """Serialize for the password update functionality"""

    password = password_validator()
    confirm_password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=False
    )

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['password', 'confirm_password']


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # As mentioned above, an email is required. Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # As mentioned above, a password is required. Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        if not user.is_verified:
            raise serializers.ValidationError(
                'Verify email before logging in.'
            )
        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag to tell us whether the user has been banned
        # or otherwise deactivated. This will almost never be the case, but
        # it is worth checking for. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    # Passwords must be at least 8 characters, but no more than 128
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so let's just stick with the defaults.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

        # The `read_only_fields` option is an alternative for explicitly
        # specifying the field with `read_only=True` like we did for password
        # above. The reason we want to use `read_only_fields` here is because
        # we don't need to specify anything else about the field. For the
        # password field, we needed to specify the `min_length` and
        # `max_length` properties too, but that isn't the case for the token
        # field.

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        # Passwords should not be handled with `setattr`, unlike other fields.
        # This is because Django provides a function that handles hashing and
        # salting passwords, which is important for security. What that means
        # here is that we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()` is the method mentioned above. It handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        # Finally, after everything has been updated, we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance


class SocialAuthenticationSerializer(serializers.Serializer):
    """Takes in access token, provider, and access_token_secret"""

    client_provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(
        max_length=4096, trim_whitespace=True, required=True)
    access_token_secret = serializers.CharField(
        max_length=4096, trim_whitespace=True, required=False)
