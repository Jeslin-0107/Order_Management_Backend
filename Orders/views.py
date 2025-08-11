from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import generics

class CustomerList(APIView):
    def post(self, request):

        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class ProductList(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class OrderCreateView(generics.CreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Return detailed order info
        detail_serializer = OrderDetailSerializer(order)
        return Response(detail_serializer.data)
    
class OrderDetailView(generics.RetrieveAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderDetailSerializer
    # permission_classes = [IsAuthenticated]

class OrderUpdateStatusView(generics.UpdateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        status_value = request.data.get('status')
        
        if status_value and status_value in dict(Order.STATUS_CHOICES):
            order.status = status_value
            order.save()
            serializer = self.get_serializer(order)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Invalid status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Orders.objects.all()
        status_filter = self.request.query_params.get('status', None)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')