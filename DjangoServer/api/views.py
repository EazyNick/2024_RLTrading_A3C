import json
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
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token

# 추가 경로 설정
sys.path.append(str(Path(__file__).resolve().parent / 'modules'))
sys.path.append(str(Path(__file__).resolve().parent / 'RLmodels'))

try:
    from modules.Auth import *  # Auth 모듈의 파일들을 임포트
    from modules.services import *  # services 모듈의 파일들을 임포트
    from RLmodels.main import main_run
    from RLmodels.Agent.A3CAgent import A3CAgent  # A3CAgent 클래스 불러오기
    from RLmodels.env.env import StockTradingEnv
    from modules.utils import *
    from modules.config import *
    from ChatGPT import *
except ImportError as e:
    print(f"Import error: {e}")
    raise

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
        table = dynamodb.Table('User_Accounts')

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

    def get(self, request):
        return Response({"message": "POST 요청으로 해야지 멍충아"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        email = request.data.get('Email')
        password = request.data.get('Password')

        if not email or not password:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        # DynamoDB 클라이언트 초기화
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        table = dynamodb.Table('User_Accounts')

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
            
            csrf_token = get_token(request) 
            response = JsonResponse({'message': 'Login successful'})
            response.set_cookie('csrftoken', csrf_token)
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AccountStatusView(View):
    def get(self, request):
        account_id = request.GET.get('account_id')

        if not account_id:
            return JsonResponse({'error': 'No account ID provided'}, status=400)

        try:
            stock_info_list, account_info = DynamoDBManager.load_from_dynamodb(account_id)
            if stock_info_list or account_info:
                return JsonResponse({
                    'stock_info_list': [stock.to_dict() for stock in stock_info_list],
                    'account_info': account_info.to_dict()
                })
            else:
                return JsonResponse({'error': 'No data found for the provided account ID'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

class StockAutoTradingChatbotView(View):
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request):
        return JsonResponse({"message": "POST 요청으로 해야지 멍충아"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        try:
            print("Received POST request")
            excel_path = os.path.join(os.path.dirname(__file__), 'templates', 'excel', 'CS_Document.xlsx')
            if not os.path.exists(excel_path):
                print("Excel file not found")
                return JsonResponse({'error': 'Excel file not found'}, status=404)
            
            excel_content = read_excel(excel_path)
            print("Excel file read successfully")
            data = json.loads(request.body)
            user_input = data.get('message', '')
            if not user_input:
                print("No user input provided")
                return JsonResponse({'error': 'No user input provided'}, status=400)
            
            chatbot_response = chatgpt(user_input, excel_content)
            print("ChatGPT response generated successfully")
            return JsonResponse({'response': chatbot_response})
        except json.JSONDecodeError:
            print("Invalid JSON provided")
            return JsonResponse({'error': 'Invalid JSON provided'}, status=400)
        except Exception as e:
            print(f"An error occurred: {e}")
            return JsonResponse({'error': str(e)}, status=500)
        
class StockDataView(View):
    def get(self, request, *args, **kwargs):
        try:
            kospi_today, kospi_latest, kosdaq_today, kosdaq_latest = get_kospi_kosdaq_data()
            return JsonResponse({
                'status': 'success', 
                'kospi_today': kospi_today, 
                'kospi_latest': kospi_latest,
                'kosdaq_today': kosdaq_today,
                'kosdaq_latest': kosdaq_latest
            }, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
