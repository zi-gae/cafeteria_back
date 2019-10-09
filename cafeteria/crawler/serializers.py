from .models import TuData, RestaurantData
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


class DormitorySerializer(serializers.ModelSerializer):
    tu_password = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = TuData
        fields = [
            'tu_id',
            'tu_password',
            'first_day',
            'second_day',
            'apply_text',
        ]


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantData
        fields = (
            'ddoock',
            'il',
            'rice',
            'noodle',
            'yang',
            'faculty_menu',
        )
