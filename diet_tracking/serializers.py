from rest_framework import serializers

from diet_tracking.models import FoodLog
class FoodLogSerializer(serializers.ModelSerializer):

    class Meta:

        model = FoodLog

        fields = "__all__"

        read_only_fields = ["id","owner","created_at"]

        