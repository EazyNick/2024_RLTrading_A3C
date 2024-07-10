from rest_framework import viewsets
from rest_framework.response import Response
from api.models import Item
from api.serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
