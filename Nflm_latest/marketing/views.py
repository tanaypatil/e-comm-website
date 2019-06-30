from django.shortcuts import render
from .models import Coupon,CouponUser,AffiliateProgram,ReferralProgram,AffiliateBankingDetails,ReferredList
from django.contrib.auth.decorators import login_required
from carts.models import Cart
from orders.models import Order
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from datetime import datetime
from .forms import AffiliateAddForm,AffiliateBankingForm,ReferralForm
from django.core.mail import send_mass_mail,send_mail
import random, re


def GenerateRandom():
    k = random.randrange(10000,99999)
    return k

# Create your views here.

@login_required()
def coupon_check(request):
    code = request.POST["coupon_code"]
    cart = Cart.objects.get(id = request.POST["cart_id"])
    try:
        coupon = Coupon.objects.get(coupon_code=code)
        products_included = coupon.products_included.all()
        print(products_included)
        products_excluded = coupon.products_excluded.all()
        print(products_excluded)
        users_restricted =coupon.users_restricted.all()
        print(users_restricted)
        if cart.coupon:
            cart.coupon=None
            cart.coupon_discount=Decimal(0)
            cart.save()
            cart.update_subtotal()
        if cart.subtotal < coupon.minimum_spend:
            context = {
                "success" : False,
                "message" : "Minimum Cart Value Should be " + str(coupon.minimum_spend),
                'final_total':cart.get_final_total()
            }
            return JsonResponse(context)
        if not coupon.active:
            context = {
                "success" : False,
                "message" : "Coupon is not active",
                'final_total':cart.get_final_total()
            }
            return JsonResponse(context)
        if datetime.now().date() > coupon.expiry_date:
            context = {
                "success" : False,
                "message" : "Coupon has been expired.",
                'final_total':cart.get_final_total()
            }
            return JsonResponse(context)
        if users_restricted.count()>=1:
            if request.user in users_restricted:
                context = {
                    "success" : False,
                    "message" : "You are restricted from using this coupon.",
                    'final_total':cart.get_final_total()
                }
                return JsonResponse(context)
        if coupon.exclude_sale_items:
            for cart_item in cart.cart_items.all():
                if cart_item.product.sale_price:
                    context = {
                        "success" : False,
                        "message" : "Your Cart Includes Sale Items.Please try to remove them or proceed without coupon",
                        'final_total':cart.get_final_total()
                    }
                    return JsonResponse(context)
        if products_included.count()>=1 or products_excluded.count()>=1:
            print("entered")
            for cart_item in cart.cart_items.all():
                print(products_included)
                print(cart_item)
                if cart_item.product not in products_included or cart_item.product in products_excluded:
                    context = {
                        "success" : False,
                        "message" : "Coupon not applicable to " + cart_item.product.title,
                        'final_total':cart.get_final_total()
                    }
                    return JsonResponse(context)
        if coupon.usage_count >= coupon.usage_limit_per_coupon:
            context = {
                "success" : False,
                "message" : "Coupon Usage Limit has been exceeded.",
                'final_total':cart.get_final_total()
            }
            return JsonResponse(context)
        if CouponUser.objects.filter(coupon=coupon,user=request.user).count() >= coupon.usage_limit_per_user:
            context = {
                "success" : False,
                "message" : "You have exceeded Coupon Usage limit.Please try some other coupon.",
                'final_total':cart.get_final_total()
            }
            return JsonResponse(context)
        success = True
        if coupon.absolute_discount:
            if coupon.cart_discount:
                cart.coupon=coupon
                cart.coupon_discount = coupon.coupon_amount
                cart.save()
                cart.update_subtotal()
                message = "Congratulation! Coupon applied successfully"
                discount = coupon.coupon_amount
            context={
                'success':success,
                'message':message,
                'discount':round(discount,2),
                'final_total':round(cart.get_final_total(),2)
            }
            return JsonResponse(context)
        else:
            print(coupon.coupon_amount)
            print(cart.subtotal)
            discount = Decimal(Decimal(coupon.coupon_amount)*Decimal(0.01)*cart.subtotal)
            print(discount)
            if coupon.maximum_spend!=0 and discount > coupon.maximum_spend:
                discount = coupon.maximum_spend
            cart.coupon=coupon
            cart.coupon_discount = discount
            cart.save()
            cart.update_subtotal()
            # Do after Order Completion
            # coupon.usage_count = coupon.usage_count + 1
            # coupon.save()
            message = "Congratulations! Coupon applied successfully"
            context={
                'success':success,
                'message':message,
                'discount':round(discount,2),
                'final_total':round(cart.get_final_total(),2)
            }
            return JsonResponse(context)
    except:
        if cart.coupon:
            cart.coupon=None
            cart.coupon_discount=Decimal(0)
            cart.save()
            cart.update_subtotal()
        context = {
            "success" : False,
            "message" : "Coupon Doesn't Exist.",
            'final_total':round(cart.get_final_total(),0)
        }
        return JsonResponse(context)


@login_required()
def add_affiliate(request):
    if request.method=="POST":
        affiliate_form = AffiliateAddForm(request.POST or None)
        if AffiliateProgram.objects.filter(user=request.user).count()==1:
            messages.error(request,"You are already registered as an affiliate.you can check your details on my account section.")
            context={
                'message':"You are already registered as an affiliate.you can check your details in my account section."
            }
            return render(request,"affiliates/affiliate_redirect.html",context)
        if affiliate_form.is_valid():
            instance = affiliate_form.save(commit=False)
            instance.user=request.user
            coupon_code = "AFFL" + str(GenerateRandom()) + str(AffiliateProgram.objects.all().count()).zfill(4)
            coupon = Coupon(coupon_code=coupon_code)
            coupon.save()
            instance.coupon = coupon
            instance.save()
            context = {
                "coupon_code" : coupon_code
            }
            return render(request,"affiliates/affiliate_redirect.html",context)
        else:
            print("entered else")
            context = {
                'form' : affiliate_form,
            }
            return render(request,"affiliates/new_affiliate.html",context)
    else:
        context={
            'form' : AffiliateAddForm(),
        }
        return render(request,"affiliates/new_affiliate.html",context)


@login_required()
def affiliate_coupon_status(request):
    affiliate = AffiliateProgram.objects.get(user=request.user)
    context={
        "affiliate":affiliate
    }
    return render(request,"affiliates/coupon_status.html",context)


@login_required()
def affiliate_banking_details(request):
    if request.method=="POST":
        affiliate_banking_form = AffiliateBankingForm(request.POST or None)
        if affiliate_banking_form.is_valid():
            affiliate=AffiliateProgram.objects.get(user=request.user)
            instance = affiliate_banking_form.save(commit=False)
            instance.affiliate=affiliate
            instance.save()
            messages.success(request,"Congratulations! Your Banking Details have been saved successfully.")
            context = {
                'form' : affiliate_banking_form
            }
            return render(request,"affiliates/banking_details.html",context)
        else:
            print("entered else")
            context = {
                'form' : affiliate_banking_form,
            }
            return render(request,"affiliates/banking_details.html",context)
    else:
        try:
            banking_details = AffiliateProgram.objects.get(user=request.user).affiliate_banking_details
            context={
                'form' : AffiliateBankingForm(instance=banking_details),
            }
            return render(request,"affiliates/banking_details.html",context)
        except:
            context={
                'form' : AffiliateBankingForm(),
            }
            return render(request,"affiliates/banking_details.html",context)


@login_required()
def affiliate_users(request):
    affiliate = AffiliateProgram.objects.get(user=request.user)
    users = affiliate.coupon_used_users.all()
    orders = Order.objects.filter(user__in=users,coupon=affiliate.coupon)
    context={
        "orders":orders,
    }
    return render(request,"affiliates/affiliate_users.html",context)


@login_required()
def referral_users(request):
    referral = ReferralProgram.objects.get(user=request.user)
    users = referral.referral_list.all()
    orders = Order.objects.filter(user__in=users,coupon=referral.coupon)
    context={
        "orders":orders,
    }
    return render(request,"referral/referral_users.html",context)

@login_required()
def referral_share(request):
    print(request.POST)
    if request.method == "POST":
        mobile_list = request.POST.getlist("number")
        email_list = request.POST.getlist("email")
        name_list = request.POST.getlist("name")
        print(mobile_list)
        print(email_list)
        print(name_list)
        referral = ReferralProgram.objects.get(user=request.user)
        context = {
            'referral_coupon': referral.coupon,
        }
        for counter,mobile in enumerate(mobile_list):
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email_list[counter]):
                messages.error(request,"Email " + email_list[counter] + " is in incorrect format.")
                return render(request, "referral/share.html", context)
            if not re.match(r'^\+?1?\d{10,10}$', mobile):
                messages.error(request, "Mobile " + mobile + " is in incorrect format.")
                return render(request, "referral/share.html", context)
            instance,created = ReferredList.objects.get_or_create(referral = referral,email=email_list[counter])
            instance.name = name_list[counter]
            instance.mobile = mobile
            instance.save()
            print(counter,mobile,email_list[counter])
        send_mail(request.user.username + "referred you to try NFLM Products",
                  "Your Coupon Code is " + referral.coupon.coupon_code + ".Use it at checkout.",
                  "info@nflm.co.in", email_list)
        return render(request, "referral/share.html", context)
    else:
        referral,created = ReferralProgram.objects.get_or_create(user=request.user)
        if not created:
            context = {
                'referral_coupon':referral,
            }
            return render(request,"referral/share.html",context)
        else:
            coupon_code = "REFR" + str(GenerateRandom()) + str(AffiliateProgram.objects.all().count()).zfill(4)
            coupon = Coupon(coupon_code=coupon_code)
            coupon.save()
            referral.coupon=coupon
            referral.save()
            context = {
                'referral_coupon':referral,
            }
            return render(request,"referral/share.html",context)


def referral_login(request):
    title = "Referral Login of nail art design 2016-nflmnew.co.in"
    context = {
        'title': title,
        'next': '/referral/share'
    }
    return render(request, "referral/referral_login.html", context)


def affiliate_login(request):
    title = "Affiliate Login of nail art design 2016-nflmnew.co.in"
    context = {
        'title': title,
        'next': "/affiliate/add/",
    }
    return render(request, "affiliates/affiliate_login.html", context)


def customization_login(request):
    title = "Customization Login of nail art design 2016-nflmnew.co.in"
    context = {
        'title': title,
        'next': '/customization'
    }
    return render(request, "customization/customization_login.html", context)
