from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Cart,CartPosition
from ..serializers import CartSerializer, CartPositionSerializer
from orders.utils import get_cart_by_user
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

@method_decorator(csrf_exempt,name="dispatch")
class CartView(APIView):
    
    def get(self,request,pk=None):
        cart = get_cart_by_user(request.user)["response"]
        if pk:
            cart_item = get_object_or_404(CartPosition,cart=cart)
            serializer = CartSerializer(cart_item)
        else:
            cart_items = CartPosition.objects.filter(cart=cart)
            serializer = CartPositionSerializer(cart_items,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        print("POST BLOCK")
        serializer = CartPositionSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save(cart=get_cart_by_user(request.user)["response"])
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk):
        cart = get_object_or_404(Cart,pk=pk) #add user args
        serializer = CartSerializer(cart,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        cart = get_object_or_404(Cart,pk=pk)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
