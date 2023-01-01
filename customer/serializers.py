from rest_framework import serializers

from easy_pg_backend.users.models import User

from .models import Address, CustomersUser, Hostel, HostelType, Review


class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomersUser
        fields = [
            "id",
            "user",
            "name",
            "phone",
            "email",
        ]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "city",
            "state",
            "pin_code",
            "hostel",
            "locality",
        ]


class HostelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelType
        fields = ["type", "price", "hostel"]


class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = [
            "id",
            "name",
            "description",
            "active",
            "images",
            "food_included",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        hotel_types = HostelType.objects.filter(hostel=instance)
        addresses = Address.objects.filter(hostel=instance)
        data["owner"] = CustomerUserSerializer(instance.owner).data
        data["types"] = HostelTypeSerializer(hotel_types, many=True).data
        data["addresses"] = AddressSerializer(addresses, many=True).data
        return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "title", "description", "images"]
