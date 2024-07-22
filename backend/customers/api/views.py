from rest_framework import viewsets
from .serializers import CustomerSerializer
from ..models import Customers

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer