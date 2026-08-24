from django.urls import path

from .views import StudentOnboardingView


urlpatterns = [
    path("student-onboarding/", StudentOnboardingView.as_view(), name="student-onboarding"),
]