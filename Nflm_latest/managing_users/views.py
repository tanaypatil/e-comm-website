import requests
from django.shortcuts import render
from .forms import AddressForm, ContactUsForm, CustomizationForm, Customization
from .models import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from products.models import Product, ProductImage
from itertools import chain
# import urllib2
# import json

# Create your views here.


def home(request):
    title = "NFLM"
    new_list = Product.objects.filter(new_arrival=True)[:3]  # you can change the no of products displaed in
    # Exclusive/New/Sale section (use multiples of 4
    sale_list = Product.objects.filter(sale_price__isnull=False)[:3]
    exclusive_list = Product.objects.filter(exclusive=True)[:3]
    occasional_list = Product.objects.filter(occasional=True)[:3]
    complete_list = list(chain(new_list, sale_list, exclusive_list, occasional_list))
    context = {
        'title': title,
        'new_list': new_list,
        'occasional_list': occasional_list,
        'exclusive_list': exclusive_list,
        'sale_list': sale_list,
        'complete_list': complete_list
    }
    return render(request, "index.html", context)


def sitemap(request):
    return render(request, "sitemap.xml")


def robots(request):
    return render(request, "robots.txt")


def google(request):
    return render(request, "googlef853ae7d9bf10541.html")


def about(request):
    title = "NFLM | About Us"
    context = {
        'title': title,
    }
    return render(request, "others/about.html", context)


def disclaimer(request):
    title = "Disclaimer and Terms of Use of nail art design 2016-nflmnew.co.in"
    context = {
        'title': title,
    }
    return render(request, "others/disclaimer.html", context)


def terms(request):
    title = "Terms of Use of nail art design 2016-nflmnew.co.in"
    context = {
        'title': title,
    }
    return render(request, "others/terms.html", context)


def faq(request):
    title = "FAQ'S of nail art design 2016-nflmnew.co.in"
    context = {
        'title': title,
    }
    return render(request, "others/faq.html", context)


def privacy(request):
    title = "Privacy Policies of nail art design 2016-nflmnew.co.in"
    context = {
        'title': title,
    }
    return render(request, "others/privacy.html", context)


def refunds(request):
    title = "Refunds and Cancellations | nflmnew.co.in"
    context = {
        'title': title,
    }
    return render(request, "others/refunds_and_cancellation.html", context)


def delivery(request):
    title = "Delivery Information | nflmnew.co.in"
    context = {
        'title': title,
    }
    return render(request, "others/delivery.html", context)


@login_required()
def user_addresses(request):
    user_addresses = UserAddress.objects.filter(user=request.user)
    return render(request, "address/user_addresses.html", {"user_addresses": user_addresses})


@login_required()
def add_address(request):
    next = request.GET.get("next")
    print(next)
    if request.method == 'POST':
        form = AddressForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'Address Added Successfully.')
            if next is not None:
                return HttpResponseRedirect(next)
            else:
               return HttpResponseRedirect(reverse("user_addresses"))
        else:
            context = {
                'addressForm': form,
                'next': next
            }
            return render(request, "address/add_address.html", context)
    else:
        form = AddressForm()
        context = {
            'addressForm': form,
            'next': next
        }
        return render(request, "address/add_address.html", context)


@login_required()
def update_address(request, id):
    if request.method == "POST":
        address_form = AddressForm(request.POST, instance=UserAddress.objects.get(id=id))
        address_form.user = request.user
        address_form.save()
        messages.success(request, 'Address Updated Successfully.')
        return HttpResponseRedirect(reverse("user_addresses"))
    else:
        address_form = AddressForm(instance=UserAddress.objects.get(id=id))
        context = {
            'addressForm': address_form,
            'id': id
        }
        return render(request, "address/update_address.html", context)


@login_required()
def delete_address(request, id):
    try:
        user_address = UserAddress.objects.get(id=id)
        user_address.delete()
        return HttpResponseRedirect(reverse("user_addresses"))
    except ObjectDoesNotExist:
        raise Http404


def contact_us(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST or None)
        if form.is_valid():
            instance = form.save()
            print(instance)
            context = {
                'form': form
            }
            messages.success(request, "Your request has been submitted.We will get back to you soon")
            return render(request, "contact.html", context)
        else:
            context = {
                'form': form
            }
            return render(request, "contact.html", context)
    else:
        form = ContactUsForm()
        context = {
            'form': form
        }
        return render(request, "contact.html", context)


@login_required()
def customization(request):
    if request.method == "POST":
        form = CustomizationForm(request.POST or None, request.FILES)
        if form.is_valid():
            count = Customization.objects.filter(user=request.user).count()
            print(count)
            if count >= 4:
                messages.error(request, "Maximum customized submission limit is 4.")
            else:
                instance_new = Customization(user=request.user)
                instance_new.name = form.cleaned_data['name']
                instance_new.image = form.cleaned_data['image']
                instance_new.description = form.cleaned_data['description']
                instance_new.save()
                product_object = Product(title="custom"+str(instance_new.id), custom_made=True, price=150.00,
                                         highlights=None, description=instance_new.description,
                                         slug='custom'+str(instance_new.id), active=False, stock=5,
                                         sku=instance_new.name+str(instance_new.id))
                product_object.save()
                prod_img = ProductImage(product=product_object, image=instance_new.image, alt_text='custom product',
                                        active=False)
                prod_img.save()
                context = {
                    'product': product_object
                }
                return render(request, "customization/custom_rules.html", context)
            # messages.success(request, "Your request has been submitted.We will review it and get back to you soon.")
            # return HttpResponseRedirect(reverse('customization'))
        else:
            context = {
                'form': form
            }
            return render(request, "customization/customization.html", context)
    else:
        form = CustomizationForm()
        context = {
            'form': form
        }
        return render(request, "customization/customization.html", context)


def code_generation(request):
    print(request.GET)
    response = requests.get('http://2factor.in/API/V1/dde69ad1-104a-11e6-9a14-00163ef91450/SMS/' + request.GET.get("mobile") +'/AUTOGEN')
    data = response.json()
    print(data)
    return JsonResponse(data)


def code_check(request):
    print(request.GET)
    response = requests.get('http://2factor.in/API/V1/dde69ad1-104a-11e6-9a14-00163ef91450/SMS/VERIFY/'+ request.GET.get("session") +'/' + request.GET.get("code"))
    data = response.json()
    print(data)
    return JsonResponse(data)


def try_before_buy(request):
    title = "Try Before You Buy | nflmnew.co.in"
    videos = HowToUseVideo.objects.all()
    context = {
        'title': title,
        'videos': videos,
    }
    return render(request, "others/try_before_buy.html", context)

