from rest_framework import serializers
from . import models


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ('username', 'email', 'date_of_birth')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ('title', 'start_date', 'end_date', 'capacity')
