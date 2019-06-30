from django.shortcuts import render
from .models import Cart,CartItem
from products.models import Product
from wishlists.models import WishlistItem,Wishlist
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from decimal import Decimal
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

# Create your views here.

try:
    gift_rate = settings.DEFAULT_GIFT_WRAP_RATE
except Exception as e:
    print(str(e))
    raise NotImplementedError(str(e))


def cart_details(request):
    if request.is_ajax():
        success = True
        message = ""
        cart_id = request.session.get('cart_id')
        print(cart_id)
        if cart_id is None:
            if request.user.is_authenticated():
                try:
                    cart = Cart.objects.get(user=request.user)
                    for cart_item in cart.cart_items.all():
                        product = cart_item.product
                        if product.stock == 0:
                            cart_item.quantity = 0
                            cart_item.save()
                            success = False
                            message = product.title + "is Out of Stock"
                        elif product.stock < cart_item.quantity:
                            cart_item.quantity = product.stock
                            cart_item.save()
                            success = False
                            message = product.title + "Quantity exceeded stock.Quantity has been changed."
                    cart_total = cart.subtotal
                    count = CartItem.objects.filter(cart=cart).count()
                except:
                    count = 0
                    cart_total = 0.00
            else:
                count = 0
                cart_total = 0.00
        else:
            cart = Cart.objects.get(id=cart_id)
            for cart_item in cart.cart_items.all():
                product = cart_item.product
                if product.stock == 0:
                    cart_item.quantity = 0
                    cart_item.save()
                    success = False
                    message = product.title + "is Out of Stock"
                elif product.stock < cart_item.quantity:
                    cart_item.quantity = product.stock
                    cart_item.save()
                    success = False
                    message = product.title + "Quantity exceeded stock.Quantity has been changed."
            cart_total = cart.subtotal
            count = CartItem.objects.filter(cart=cart).count()

        context = {
            "count": count,
            "cart_total": cart_total,
            "success": success,
            "message": message
        }
        return JsonResponse(context)
    else:
        raise Http404


def add_to_cart(request, slug):
    print(request.POST)
    print(slug)
    request.session.set_expiry(120000)
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        pass
    except:
        pass
    if request.user.is_authenticated():
        cart, created = Cart.objects.get_or_create(user=request.user)
        if created:
            request.session['cart_id'] = cart.id
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist_item = WishlistItem.objects.get(wishlist=wishlist, product=product)
            wishlist_item.delete()
        except:
            pass
    else:
        print("entered")
        the_id = request.session.get('cart_id')
        if the_id is None:
            print("entered except")
            new_cart = Cart()
            print(new_cart)
            new_cart.save()
            request.session['cart_id'] = new_cart.id
            the_id = new_cart.id
        print(the_id)
        cart = Cart.objects.get(id=the_id)

    if request.method == "POST":
        qty = request.POST['qty']
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if product.stock == 0:
            success = False
            message = product.title + " is Out of Stock"
        elif int(qty) > product.stock:
            print("entered")
            success = False
            cart_item.quantity = product.stock
            cart_item.save()
            message = product.title + " Quantity exceeded stock.Quantity has been changed."
        else:
            cart_item.quantity = qty
            cart_item.save()
            success = True
            if created:
                message = cart_item.product.title + " successfully added to cart."
            else:
                message = cart_item.product.title + " already added to cart.You can change the quantity in view cart."
        context = {
            'success': success,
            'message': message
        }
        return JsonResponse(context)
    # error message
    return HttpResponseRedirect(reverse("view_cart"))


def add_custom_product_to_cart(request, slug):
    print(request.POST)
    print(slug)
    request.session.set_expiry(120000)
    cart, created = Cart.objects.get_or_create(user=request.user)
    if created:
        request.session['cart_id'] = cart.id
    product = Product.objects.get(slug=slug)
    if request.method == "POST":
        qty = 1
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = 1
        cart_item.save()
        # return JsonResponse(context)
        return HttpResponseRedirect(reverse("view_cart"))
    # error message
    return HttpResponseRedirect(reverse("view_cart"))


def view_cart(request):
    try:
        the_id = request.session.get('cart_id')
        cart = Cart.objects.get(id=the_id)
        for cart_item in cart.cart_items.all():
            product = cart_item.product
            if product.stock == 0:
                cart_item.quantity = 0
                cart_item.save()
                messages.error(request, product.title + "is Out of Stock")
            elif product.stock < cart_item.quantity:
                cart_item.quantity = product.stock
                cart_item.save()
                messages.error(request, product.title + "Quantity exceeded stock.Quantity has been changed.")
    except:
        if request.user.is_authenticated():
            try:
                cart = Cart.objects.get(user=request.user)
                if cart.coupon:
                    cart.coupon = None
                    cart.coupon_discount = 0
                    cart.update_subtotal()
                    cart.save()
                for cart_item in cart.cart_items.all():
                    product = cart_item.product
                    if product.stock == 0:
                        cart_item.quantity = 0
                        cart_item.save()
                        messages.error(request, product.title + "is Out of Stock")
                    elif product.stock < cart_item.quantity:
                        cart_item.quantity = product.stock
                        cart_item.save()
                        messages.error(request, product.title + "Quantity exceeded stock.Quantity has been changed.")
            except ObjectDoesNotExist:
               cart={}
        else:
            cart = {}
    context = {
        'cart': cart,
        'gift_cost': gift_rate
    }
    return render(request, "carts/view_cart.html", context)


def remove_from_cart(request, id):
    try:
        cart_item = CartItem.objects.get(id=id)
        cart_item.delete()
        return HttpResponseRedirect(reverse("view_cart"))
    except ObjectDoesNotExist:
        raise Http404


def update_cart(request):
    try:
        cart_item = CartItem.objects.get(id=request.GET.get("id"))
        new_quantity = request.GET['quantity']
        if int(new_quantity) == 0:
            cart_item.delete()
            refresh = True
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            refresh = False
        context = {
            'line_total' : cart_item.line_total,
            'subtotal': cart_item.cart.subtotal,
            'final_total': cart_item.cart.get_final_total(),
            'refresh': refresh
        }
        return JsonResponse(context)
    except:
        raise Http404


def add_gift_cart(request):
    try:
        cart = Cart.objects.get(id = request.GET.get("id"))
        if request.GET.get("checked") == "True":
            cart.gift_wrap = True
        else:
            print("entered else")
            cart.gift_wrap = False
        cart.notes = request.GET.get("notes")
        cart.update_subtotal()
        cart.save()
        context = {
            'gift_cost': gift_rate,
            'final_total': cart.get_final_total(),
            'success' : True
        }
        return JsonResponse(context)
    except:
        raise Http404




