import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_api.settings")
django.setup()

from onboarding.serializers import StudentOnboardingSerializer


data = {
    "student_name": "Ankita Jadhav",
    "age": 17,
    "parent_consent": "maybe",
    "special_support_required": "No",
    "previous_school": "ABC Public School",
}

print("Parent consent value:", repr(data["parent_consent"]))
print("Support value:", repr(data["special_support_required"]))

serializer = StudentOnboardingSerializer(data=data)

print("Valid:", serializer.is_valid())
print("Errors:", serializer.errors)

if serializer.is_valid():
    print("Validated data:", serializer.validated_data)