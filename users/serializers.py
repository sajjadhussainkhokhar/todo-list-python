from django.contrib.auth.models import User
from rest_framework import serializers


class UserSignupSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "password", "date_joined")
        read_only_fields = ("id", "date_joined")

    def create(self, validated_data):
        # Ensure username exists (default User model requires it)
        # remove email from validated_data so it's not passed twice
        email = validated_data.pop("email", None)
        username = validated_data.pop("username", None) or (email.split("@")[0] if email else None)

        password = validated_data.pop("password")

        # remaining validated_data may contain first_name/last_name
        user = User(username=username, email=email, **validated_data)
        user.set_password(password)
        user.save()
        return user
