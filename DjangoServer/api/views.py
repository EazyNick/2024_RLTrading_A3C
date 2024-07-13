import time
import boto3
from boto3.dynamodb.conditions import Key
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from django.views import View
import subprocess
import sys
import os


class SaveItemView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        return Response({"message": "POST 요청으로 해야지 멍충아"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        email = request.data.get('Email')
        password = request.data.get('Password')
        username = request.data.get('username')

        if not username or not email or not password:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        # DynamoDB 클라이언트 초기화
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        table = dynamodb.Table('Accounts')

        try:
            response = table.put_item(
                Item={
                    'Email': email,
                    'Password': password,
                    'username': username,
                    'Timestamp': str(int(time.time())),
                }
            )
            return Response({"message": "Data saved to DynamoDB successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class LoginView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        email = request.data.get('Email')
        password = request.data.get('Password')

        if not email or not password:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        # DynamoDB 클라이언트 초기화
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        table = dynamodb.Table('Accounts')

        try:
            response = table.query(
                KeyConditionExpression=Key('Email').eq(email)
            )
            items = response.get('Items', [])
            if not items:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            user = items[0]
            if user['Password'] != password:
                return Response({"error": "Incorrect Password"}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AccountStatusView(View):
    def get(self, request):
        try:
            # get_prices.py 파일의 절대 경로를 지정합니다.
            script_path = os.path.join(os.path.dirname(__file__), 'modules/services/get_prices.py')

            # subprocess를 사용하여 스크립트를 실행하고 출력을 캡처합니다.
            result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)

            # 스크립트 실행 결과를 JSON 형식으로 반환합니다.
            return JsonResponse({
                'output': result.stdout,
                'error': result.stderr
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)