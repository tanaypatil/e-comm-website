from django.shortcuts import render
from products.models import Product
from .models import Wishlist,WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse,Http404
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required()
def add_to_wishlist(request, slug):
    wishlist,created = Wishlist.objects.get_or_create(user=request.user)
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        pass
    except:
        pass

    if request.method == "POST":
        wishlist_item,created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
        if created:
            success = wishlist_item.product.title + " successfully added to wishlist."
        else:
            success = wishlist_item.product.title + " already added to wishlist."
        context={
            'success' : success
        }
        return JsonResponse(context)
    #error message
    return HttpResponseRedirect(reverse("view_wishlist"))


@login_required()
def view_wishlist(request):
    wishlist,created = Wishlist.objects.get_or_create(user=request.user)
    context = {
        'wishlist':wishlist
    }
    return render(request, "wishlists/view_wishlist.html", context)


@login_required()
def remove_from_wishlist(request, id):
    try:
        cart_item = WishlistItem.objects.get(id=id)
        cart_item.delete()
        return HttpResponseRedirect(reverse("view_wishlist"))
    except ObjectDoesNotExist:
        raise Http404
