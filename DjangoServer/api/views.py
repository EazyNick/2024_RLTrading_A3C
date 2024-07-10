import time
import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SaveItemView(APIView):
    def post(self, request):
        stock_name = request.data.get('Stock')
        stck_prpr = request.data.get('현재가')

        if not stock_name or not stck_prpr:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        # DynamoDB 클라이언트 초기화
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        table = dynamodb.Table('RESTAPI')

        try:
            response = table.put_item(
                Item={
                    'Stock': stock_name,
                    'Timestamp': str(int(time.time())),
                    '현재가': str(stck_prpr)
                }
            )
            return Response({"message": "Data saved to DynamoDB successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
