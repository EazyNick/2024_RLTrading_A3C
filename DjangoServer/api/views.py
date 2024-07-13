import time
import boto3
from boto3.dynamodb.conditions import Key
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer


class SaveItemView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        return Response({"message": "POST 요청으로 해야지 멍충아"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        # DynamoDB 클라이언트 초기화
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        table = dynamodb.Table('Accounts')

        try:
            response = table.put_item(
                Item={
                    'username': username,
                    'email': email,
                    'password': password,
                    'Timestamp': str(int(time.time())),
                }
            )
            return Response({"message": "Data saved to DynamoDB successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class LoginView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        # DynamoDB 클라이언트 초기화
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        table = dynamodb.Table('Accounts')

        try:
            response = table.query(
                KeyConditionExpression=Key('email').eq(email)
            )
            items = response.get('Items', [])
            if not items:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            user = items[0]
            if user['password'] != password:
                return Response({"error": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)