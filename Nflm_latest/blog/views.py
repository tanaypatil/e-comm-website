from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Blog
from django.db.models import Q

# Create your views here.


class BlogListView(ListView):
    model = Blog
    paginate_by = 4

    def get_context_data(self, *args, **kwargs):
        context = super(BlogListView, self).get_context_data(*args, **kwargs)
        context["query"] = self.request.GET.get("q")
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(BlogListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        qs = qs.order_by('-timestamp')
        if query:
            qs = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__title__icontains=query)
            )
        return qs


class BlogDetailView(DetailView):
    model = Blog

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        print(context)
        return context
