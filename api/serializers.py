from rest_framework import serializers
from core.models import PowerOutage

class PowerOutageSerializer(serializers.ModelSerializer):
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = PowerOutage
        fields = ['id', 'area', 'state', 'affected_zone', 'date', 'start_time', 'end_time']

    def get_start_time(self, obj):
        return obj.start_time.strftime("%H:%M")

    def get_end_time(self, obj):
        return obj.end_time.strftime("%H:%M")