import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_api.settings")
django.setup()

from onboarding.serializers import StudentOnboardingSerializer


data = {
    "student_name": "Rahul Sharma",
    "age": 15,
    "parent_consent": "No",
    "special_support_required": "No",
    "previous_school": "ABC Public School",
}

serializer = StudentOnboardingSerializer(data=data)

print("Valid:", serializer.is_valid())
print("Errors:", serializer.errors)

if serializer.is_valid():
    print("Validated data:", serializer.validated_data)