from rest_framework import serializers

from .dcyn import DCYNValidationError, to_boolean
from .models import StudentOnboarding


class StudentOnboardingSerializer(serializers.ModelSerializer):
    parent_consent = serializers.CharField()
    special_support_required = serializers.CharField()

    class Meta:
        model = StudentOnboarding
        fields = [
            "student_name",
            "age",
            "parent_consent",
            "special_support_required",
            "previous_school",
        ]

    def validate_parent_consent(self, value):
        try:
            to_boolean(value)
        except DCYNValidationError as exc:
            raise serializers.ValidationError(str(exc))

        return value

    def validate_special_support_required(self, value):
        try:
            to_boolean(value)
        except DCYNValidationError as exc:
            raise serializers.ValidationError(str(exc))

        return value