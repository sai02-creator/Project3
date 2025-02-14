from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})


def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        # Save to session
        cart.add(product=product, quantity=product_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__()

        # Return response
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ("Product Added To Cart..."))
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        # Retrieve the product (just in case we need it for something)
        product = get_object_or_404(Product, id=product_id)

        # Delete the product from the cart
        cart.delete(product=product_id)

        # Send back the response
        messages.success(request, "Item Deleted From Shopping Cart...")
        return JsonResponse({'status': 'success', 'product_id': product_id})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def cart_update(request):
    if request.method == 'POST':
        # Log the POST data
        print("POST data received:", request.POST)
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        print(f"Received product_id: {product_id}")
        print(f"Received product_qty: {product_qty}")

        # Check for missing values
        if not product_id or not product_qty:
            return JsonResponse({'error': 'Missing product_id or product_qty'}, status=400)

        try:
            product_id = int(product_id)
            product_qty = int(product_qty)
        except ValueError:
            return JsonResponse({'error': 'Invalid product_id or product_qty'}, status=400)

        cart = Cart(request)
        cart.update(product=product_id, quantity=product_qty)
        return JsonResponse({'qty': product_qty})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
