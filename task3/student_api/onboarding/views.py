from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import StudentOnboardingSerializer


class StudentOnboardingView(APIView):
    def post(self, request):
        serializer = StudentOnboardingSerializer(data=request.data)

        if serializer.is_valid():
            return Response(
                {
                    "message": "Student onboarding data is valid.",
                    "data": serializer.validated_data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "message": "Student onboarding data is invalid.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )