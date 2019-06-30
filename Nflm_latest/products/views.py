from django.shortcuts import render
from .models import Product,StockNotification,Tag
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import JsonResponse,Http404
from django.db.models import Q

# Create your views here.


class ProductListView(ListView):
    model = Product
    paginate_by = 12

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context["query"] = self.request.GET.get("q")
        context["ordering"] = self.request.GET.get("ordering")
        context["filter"] = self.request.GET.get("filter")
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        ordering = self.request.GET.get("ordering")
        filter_query = self.request.GET.get("filter")
        if query:
            qs =self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(highlights__icontains=query) |
                Q(tags__title__icontains=query) |
                Q(sku__iexact=query)
            )
        if ordering:
            qs = qs.order_by(ordering)
        else:
            print("entered")
            qs = qs.order_by('-timestamp')
        if filter_query:
            if filter_query == "excl":
                qs = qs.filter(exclusive=True)
            elif filter_query == "sale":
                qs = qs.filter(sale_price__isnull=False)
            elif filter_query == "occasional":
                qs = qs.filter(occasional=True)
            elif "tag" in filter_query:
                tag = filter_query.split("_")
                print(tag[1])
                qs = qs.filter(tags__title__icontains=tag[1])
            else:
                qs = qs.filter(new_arrival=True)
        return qs


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        print(context)
        return context


class TagListView(ListView):
    model = Tag
    paginate_by = 12


def OutofStockNotification(request):
    if request.method == "POST":
        print(request.POST)
        product_id = request.POST['id']
        email = request.POST['email']
        mobile = request.POST['mobile']
        print(mobile)
        notification, created = StockNotification.objects.get_or_create(product=Product.objects.get(id=product_id), email=email)
        notification.mobile = mobile
        notification.save()
        success = True
        if created:
            message = "Your details have been saved."
        else:
            message = "You are already subscribed."
        context = {
            'success': success,
            'message': message
        }
        return JsonResponse(context)
    else:
        success = False
        message = "Some Error Occured.Please try again later."
        context = {
            'success': success,
            'message': message
        }
        return JsonResponse(context)
