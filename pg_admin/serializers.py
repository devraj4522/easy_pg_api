from rest_framework import serializers

from easy_pg_backend.users.models import User


class EasyPgUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "is_active", "groups"]
        extra_kwargs = {
            "username": {"read_only": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
