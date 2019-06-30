from django.shortcuts import render
from django.contrib import messages
from .models import Order,OrderItem,PaymentDetails
from managing_users.models import NFLMUser,UserAddress
from managing_users.forms import AddressForm
from carts.models import Cart,CartItem
from django.http import JsonResponse,Http404
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from marketing.models import Coupon,CouponUser,AffiliateProgram,ReferralProgram
from django.http import HttpResponse
from easy_pdf.views import PDFTemplateView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import random
from instamojo import Instamojo
api = Instamojo(api_key='6714471c4518740886a6d1adab96c1aa', auth_token='d57aff95dfedfef868a39b181aece098')

# Create your views here.

try:
    gift_rate = settings.DEFAULT_GIFT_WRAP_RATE
    shipping_rate = settings.DEFAULT_SHIPPING_CHARGE
except:
    pass


def GenerateRandom():
    k = random.randrange(10000, 99999)
    return k


@login_required()
def user_orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders
    }
    return render(request, "myaccount.html", context)


@login_required()
def order_details(request, id):
    order = Order.objects.get(id=id)
    context = {
        'order': order
    }
    return render(request, "orders/order_view.html", context)


def order_login(request, id):
    shipping = False
    try:
        cart = Cart.objects.get(id=id)
        cart_items = CartItem.objects.filter(cart=cart)
        count = 0
        for item in cart_items:
            count = count + item.quantity
        if count < settings.MIN_CART_QUANTITY:
            shipping = True
    except ObjectDoesNotExist:
        raise Http404
    order_id = "NFLM" + str(GenerateRandom()) + str(Order.objects.all().count()).zfill(4)
    if request.user.is_authenticated():
        order, created = Order.objects.get_or_create(user=request.user, status="Started")
        order.order_id = order_id
        order.cart = cart
        if shipping:
            messages.error(request, "Minimum Cart Quantity should be " + str(settings.MIN_CART_QUANTITY) + "to waive of shipping charge")
            order.shipping_charge = shipping_rate
        else:
            order.shipping_charge = 0
        if cart.coupon is not None:
            order.coupon = cart.coupon
            order.coupon_discount = cart.coupon_discount
        order.save()
        context = {
            "cart_id": id,
            "order": order,
            'gift_cost': gift_rate,
        }
        return render(request, "orders/order_started.html", context)
    else:
        context = {
            "cart_id": id
        }
        guest_email = request.POST.get("guest_email")
        if guest_email:
            user_exists = NFLMUser.objects.filter(email =guest_email).count()
            if user_exists != 0:
                messages.error(request, "User with given email already exists.Please try to Login and Proceed.")
                return render(request, "orders/order_login.html", context)
            else:
                order, created = Order.objects.get_or_create(guest_customer=True, guest_email=guest_email)
                order.order_id = order_id
                order.cart = cart
                if shipping:
                    messages.error(request, "Minimum Cart Quantity should be " + str(settings.MIN_CART_QUANTITY) + "to waive of shipping charge")
                    order.shipping_charge = shipping_rate
                else:
                    order.shipping_charge = 0
                order.save()
                context["order"] = order
                return render(request, "orders/order_started.html", context)
        else:
            messages.error(request, "Guest Email is Required or you may login.")
        return render(request, "orders/order_login.html", context)


def payment_details_webhook(request):
    print(request.POST)
    payment_details = PaymentDetails.objects.get(payment_request_id = request.POST["payment_request_id"])
    print("payment_details")
    print(payment_details)
    if payment_details:
        payment_details_new = PaymentDetails(order= payment_details.order,payment_request_id = request.POST["payment_request_id"])
        payment_details_new.save()
        print(payment_details_new)
        payment_details.delete()
    payment_details_new.payment_id = request.POST["payment_id"]
    payment_details_new.status = request.POST["status"]
    payment_details_new.shorturl = request.POST["shorturl"]
    payment_details_new.longurl = request.POST["longurl"]
    payment_details_new.mac = request.POST["mac"]
    payment_details_new.save()
    return HttpResponse("OK")


def payment_redirect_url(request):
    print(request.GET)
    response = api.payment_request_payment_status(request.GET['payment_request_id'], request.GET['payment_id'])
    print("response")
    print(response)
    payment_details = PaymentDetails.objects.get(payment_id=request.GET['payment_id'])
    order = payment_details.order
    print(order)
    # delete cart if payment successful
    if payment_details.status == "Credit":
        if order.status!= "Completed":
            order.date = timezone.now()
            order.status = "Completed"
            order.save()
            for cart_item in order.cart.cart_items.all():
                product = cart_item.product
                product.stock -= cart_item.quantity
                order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
                print(order_item)
                print(created)
                order_item.quantity = cart_item.quantity
                order_item.line_total = cart_item.line_total
                order_item.save()
                product.save()
                cart_item.delete()
            if order.coupon is not None:
                if AffiliateProgram.objects.filter(coupon=order.coupon).count() == 1:
                    affiliate = AffiliateProgram.objects.get(coupon=order.coupon)
                    affiliate.coupon_used_users.add(order.user)
                    affiliate.successful_usage_count += 1
                    affiliate.save()
                elif ReferralProgram.objects.filter(coupon=order.coupon).count() == 1:
                    referral = ReferralProgram.objects.get(coupon=order.coupon)
                    referral.referral_list.add(order.user)
                    referral.referrals_added_count += 1
                    referral.save()
                coupon = Coupon.objects.get(coupon_code=order.coupon.coupon_code)
                coupon.usage_count = coupon.usage_count + 1
                coupon.save()
                coupon_user, created = CouponUser.objects.get_or_create(coupon=coupon, user=order.user)
                coupon_user.coupon_usage_count += 1
                coupon_user.save()
            try:
                del request.session['cart_id']
            except:
                pass
            order.cart.delete()
            text_content = ''
            htmly = get_template('orders/email/order_confirmation.html')
            d = Context({'order': order, 'today': timezone.now(), 'gift_rate': gift_rate})
            if order.user:
                subject, from_email, to = 'Order Confirmation', 'info@nflmnew.co.in', order.user.email
            else:
                subject, from_email, to = 'Order Confirmation', 'info@nflmnew.co.in', order.user.guest_email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    context = {
        "order": order,
        "gift_cost": gift_rate,
        "response": response
    }
    return render(request, "orders/order_finished.html", context)


def payment_initiated(request):
    order = Order.objects.get(id=request.POST["order_id"])
    if request.user.is_authenticated():
        address = UserAddress.objects.get(id=request.POST["address_id"])
        order.shipping_address = address
    else:
        form = AddressForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            print(instance)
            instance.save()
            order.shipping_address = instance
        else:
            context = {
                'form': form,
                "order": order,
                "gift_cost": gift_rate,
            }
            # return render(request, "orders/order_started.html", context)
    order.date = timezone.now()
    order.status = "payment_inititated"
    order.payment_method = request.POST["payment_method"]
    order.sub_total = order.cart.final_total
    order.gift_wrap = order.cart.gift_wrap
    order.notes = order.cart.notes
    order.save()
    stop = False
    for cart_item in order.cart.cart_items.all():
        product = cart_item.product
        if product.stock == 0:
            cart_item.quantity = 0
            cart_item.save()
            stop = True
            messages.error(request, product.title + "is Out of Stock")
        elif product.stock < cart_item.quantity:
            cart_item.quantity = product.stock
            cart_item.save()
            stop = True
            messages.error(request, product.title + "Quantity exceeded stock.Quantity has been changed.")
    order.get_final_amount()
    context = {
        "order": order,
        "gift_cost": gift_rate,
    }
    if stop:
        return render(request, "orders/order_started.html", context)
    else:
        if order.guest_customer:
            email = order.guest_email
        else:
            email = order.user.email
        print(order.get_final_amount())
        print("passed")
        if PaymentDetails.objects.filter(order=order).count() == 1:
            # if order.final_total < 9.00:
               # return HttpResponse("<script>alert('Congratulations. The Product will be delivered to you.');"
                                   # "window.location='https://www.nflm.co.in';</script>")
            return HttpResponseRedirect(order.paymentdetails.longurl)
        else:
            # Create a new Payment Request
            if order.get_final_amount() <= 9.00:
                payment_details, created = PaymentDetails.objects.get_or_create(order=order)
                payment_details.save()
                return HttpResponse("<script>alert('Congratulations. The Product will be delivered to you.');"
                                    "window.location='https://www.nflm.co.in';</script>")
            else:
                response = api.payment_request_create(
                    amount=order.get_final_amount(),
                    purpose="Order ID:" + order.order_id,
                    send_email=True,
                    email=email,
                    redirect_url="https://www.nflm.co.in/order/payment_completed",
                    webhook="https://www.nflm.co.in/order/payment_details",
                )
                payment_details, created = PaymentDetails.objects.get_or_create(order=order,
                                                                                payment_request_id=
                                                                                response['payment_request']['id'])
            print("payment_details")
            print(payment_details)
            payment_details.longurl = response['payment_request']['longurl']
            payment_details.status = response['payment_request']['status']
            payment_details.save()
            return HttpResponseRedirect(response['payment_request']['longurl'])


class InvoicePDFView(PDFTemplateView):
    template_name = "invoices/invoice.html"

    def get_context_data(self, **kwargs):
        context= super(InvoicePDFView, self).get_context_data(pagesize="A4", title="Invoice PDF", **kwargs)
        order_id = self.request.GET.get("order_id")
        context["today"] = timezone.now()
        context["gift_rate"] = gift_rate
        context["order"] = Order.objects.get(order_id=order_id)
        print(order_id)
        return context


def InvoiceGeneration(request):
    context = {
        'title': "Invoice Generation",
    }
    return render(request, "invoices/invoice_generation.html", context)