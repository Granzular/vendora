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
from rest_framework.decorators import api_view
from django.db import transaction
from django.http import JsonResponse
from analytics.utils import log


@method_decorator(login_required,name="dispatch")
class CartView(APIView):
    
    def get(self,request,pk=None):
        cart = get_cart_by_user(request.user)
        if pk:
            cart_item = get_object_or_404(CartPosition,cart=cart)
            serializer = CartSerializer(cart_item)
        else:
            cart_items = CartPosition.objects.filter(cart=cart)
            serializer = CartPositionSerializer(cart_items,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = CartPositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=get_cart_by_user(request.user))
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            log(f"Orders/views/api(2):POST:  {request.data}")
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


# BULK OPERATIONS BELOW
@login_required
@api_view(['POST'])
@transaction.atomic
def bulk_create_cart(request):
    """
    Create multiple cart items at once.
    Expects a list of objects.
    """
    log(f"Orders/views/api(1):POST: {request.data}")
    if not isinstance(request.data, list):
        return Response({"error": "Expected a list of objects"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CartPositionSerializer(data=request.data, many=True)
    log(f"Orders/views/api.py/bulk-create: Before checking is valid")
    serializer.is_valid(raise_exception=True)
    log("Orders bulk-create: after is valid")
    serializer.save(cart=get_cart_by_user(
request.user))
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@login_required
@api_view(['PUT', 'PATCH'])
@transaction.atomic
def bulk_update_cart(request):
    """
    Update multiple cart items.
    Each object must contain an 'id' field.
    """
    cart = get_cart_by_user(request.user)
    if not isinstance(request.data, list):
        return Response({"error": "Expected a list of objects"}, status=status.HTTP_400_BAD_REQUEST)
 
    updated_items = []
    for item in request.data:
        obj_id = item.get('product')
        if not obj_id:
            continue  # Skip objects without an ID

        try:
            instance = cart.positions.get(product=obj_id)
        except CartPosition.DoesNotExist:
            
            continue
        
        serializer = CartPositionSerializer(instance, data=item, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        updated_items.append(serializer.data)

    return Response(updated_items, status=status.HTTP_200_OK)


@login_required
@api_view(['DELETE'])
@transaction.atomic
def bulk_delete_cart(request):
    """
    Delete multiple cart items by IDs.
    Expects {"ids": [1, 2, 3]}.
    """
    cart = get_cart_by_user(request.user)
    ids = request.data.get("ids", [])
    if not isinstance(ids, list):
        return Response({"error": "ids must be a list"}, status=status.HTTP_400_BAD_REQUEST)

    qs = cart.positions.filter(product__in=ids)
    count = qs.count()
    qs.delete()
    return Response({"deleted": count}, status=status.HTTP_200_OK)

# JUST A REGULAR ENDPOINT, NO TYPICAL API
@login_required
def cart_view(request):
    if request.method == "GET":
        if request.headers.get("X-Requested-With")=="XMLHttpRequest":
            cart = get_cart_by_user(request.user)
            context = {
                    "totalCartPrice" : cart.total_price(),
                    "cartCount" : len(cart.positions.all()),
                    "cartItems" :[],
                    "cart" : []
                    }
            for item in  cart.positions.all():
                context["cartItems"].append({"price":item.product.price,"subTotal":item.total_price(),"product":item.product.id,"quantity":item.quantity})
            for item in cart.positions.all():
                context["cart"].append({"product":item.product.id,"quantity":item.quantity})
            return JsonResponse(context)
