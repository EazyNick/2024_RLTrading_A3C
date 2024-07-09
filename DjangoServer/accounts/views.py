from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer

class RegisterView(APIView):
    def post(self, request):
        print("RegisterView POST request received")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            print("Serializer is valid")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Serializer is invalid")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

