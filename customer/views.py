from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.list import ListView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from easy_pg_backend.users.models import User

from .models import Address, Hostel, HostelType, Review
from .serializers import CustomerUserSerializer, HostelSerializer, ReviewSerializer

# from .models import CustomerUser


class HostelView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    page_size = 1

    def get(self, request):
        id = request.query_params.get("id")
        print(id, "\n\n\n")
        if id:
            try:
                hostel = Hostel.objects.get(id=id)
                serialized_data = HostelSerializer(hostel)

                response_dict = {
                    "custom_status_code": 0,
                    "status_msg": "Hostel Data Fetched successfully.",
                    "data_dict": serialized_data.data,
                }
            except ObjectDoesNotExist:
                response_dict = {
                    "custom_status_code": -1,
                    "status_msg": f"Hostel not found with the id: {id}",
                    "data_dict": {},
                }
        else:
            hostels = Hostel.objects.all()
            serialized_data = HostelSerializer(hostels, many=True)
            response_dict = {
                "custom_status_code": 0,
                "status_msg": "Hostel Data Fetched successfully.",
                "data_dict": serialized_data.data,
            }
        return Response(response_dict)

    def post(self, request):
        name = request.data["name"]
        description = request.data["description"]
        images = request.data["images"]
        food_included = request.data["food_included"]
        types = request.data[
            "types"
        ]  # [{"TRIPLE_SHARING": 5000}, {"DOUBLE_SHARING: 7000}]

        try:
            owner = request.user.customer_user

            hostel = Hostel(
                name=name,
                description=description,
                owner=owner,
                images=images,
                food_included=food_included,
            )
            hostel.save()

            for room_type in types:
                for key, value in room_type.items():  # this runs a single time
                    type_obj = HostelType.objects.filter(
                        type=key, price=value, hostel=hostel
                    )
                    if not len(type_obj):
                        type_obj = HostelType(type=key, price=value, hostel=hostel)
                        type_obj.save()

            serialized_data = HostelSerializer(hostel)
            response_dict = {
                "custom_status_code": 0,
                "status_msg": "Hostel added successfully.",
                "data_dict": serialized_data.data,
            }
        except ObjectDoesNotExist:
            response_dict = {
                "custom_status_code": -1,
                "status_msg": "Owner not found.",
                "data_dict": {},
            }

        return Response(response_dict)


class CommentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    page_size = 1

    def get(self, request):
        id = request.query_params.get("id")

        if id:
            try:
                review = Review.objects.get(id=id)
                serialized_data = ReviewSerializer(review)

                response_dict = {
                    "custom_status_code": 0,
                    "status_msg": "Review Data Fetched successfully.",
                    "data_dict": serialized_data.data,
                }
            except ObjectDoesNotExist:
                response_dict = {
                    "custom_status_code": -1,
                    "status_msg": f"Review data not found with the id: {id}",
                    "data_dict": {},
                }
        else:
            review = Review.objects.all()
            serialized_data = ReviewSerializer(review, many=True)
            response_dict = {
                "custom_status_code": 0,
                "status_msg": "Review Data Fetched successfully.",
                "data_dict": serialized_data.data,
            }
        return Response(response_dict)

    def post(self, request):
        title = request.data["title"]
        description = request.data["description"]
        hostel_id = request.data["hostel_id"]
        images = request.data["images"]

        try:
            hostel = Hostel.objects.get(id=hostel_id)
            review = Review(
                title=title, description=description, hostel=hostel, images=images
            )
            review.save()

            serialized_data = ReviewSerializer(review)
            response_dict = {
                "custom_status_code": 0,
                "status_msg": "Hostel added successfully.",
                "data_dict": serialized_data.data,
            }
        except ObjectDoesNotExist:
            response_dict = {
                "custom_status_code": -1,
                "status_msg": "Owner not found.",
                "data_dict": {},
            }

        return Response(response_dict)


class FilterHostelView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    page_size = 1

    def get(self, request):
        name = request.query_params.get("name", "")
        description = request.query_params.get("description", "")

        # From address
        city = request.query_params.get("city", "")
        pin_code = request.query_params.get("pin_code", "")
        state = request.query_params.get("state", "")
        locality = request.query_params.get("locality", "")

        addresses = Address.objects.filter(
            Q(city__icontains=city)
            & Q(pin_code__icontains=pin_code)
            & Q(state__icontains=state)
            & Q(locality__icontains=locality)
        )

        hotels = Hostel.objects.filter(
            Q(addresses__in=addresses)
            & Q(name__icontains=name, description__icontains=description)
        )

        serialized_data = HostelSerializer(hotels, many=True)
        response_dict = {
            "custom_status_code": 0,
            "status_msg": "Hostel added successfully.",
            "data_dict": serialized_data.data,
        }

        return Response(response_dict)
