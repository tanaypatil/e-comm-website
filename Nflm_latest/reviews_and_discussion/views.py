from django.shortcuts import render
from django.forms import modelformset_factory
from .models import ReviewImage,Review
from .forms import ReviewAddForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse,Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from products.models import Product
from django.http import HttpResponseRedirect
from django.utils import timezone

# Create your views here.

@login_required()
def add_review(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        review = Review.objects.get(user=request.user, product=product)
        old_review = review
    except:
        review = None
        old_review = None
    if request.method == 'POST':
        review_form = ReviewAddForm(request.POST,request.FILES)
        if review_form.is_valid():
            if review:
                review.product = product
                review.user = request.user
                review.rating = request.POST["rating"]
                review.nickname=request.POST["nickname"]
                review.comment=request.POST["comment"]
                review.pub_date = timezone.now()
                review.save()
            else:
                review = Review(product=product,user=request.user,pub_date=timezone.now(),
                                nickname=request.POST["nickname"],
                                rating=request.POST["rating"],
                                comment=request.POST["comment"])
                review.save()
            review_images = ReviewImage.objects.filter(review=old_review)
            print(review_images)
            if review_form.cleaned_data['image1']:
                try:
                    review_image = ReviewImage.objects.get(id=review_images[0].id)
                    review_image.review = review
                    review_image.image = review_form.cleaned_data['image1']
                    review_image.save()
                except:
                    review_image = ReviewImage(review=review,image=review_form.cleaned_data['image1'])
                    review_image.save()
            if review_form.cleaned_data['image2']:
                try:
                    review_image = ReviewImage.objects.get(id=review_images[1].id)
                    review_image.review = review
                    review_image.image = review_form.cleaned_data['image2']
                    review_image.save()
                except:
                    review_image = ReviewImage(review=review,image=review_form.cleaned_data['image2'])
                    review_image.save()
            if review_form.cleaned_data['image3']:
                try:
                    review_image = ReviewImage.objects.get(id=review_images[2].id)
                    review_image.review = review
                    review_image.image = review_form.cleaned_data['image3']
                    review_image.save()
                except:
                    review_image = ReviewImage(review=review,image=review_form.cleaned_data['image3'])
                    review_image.save()
            try:
                for image_id in request.POST["image_id"]:
                    print("entered")
                    review_image = ReviewImage.objects.get(id=image_id)
                    review_image.delete()
            except:
                pass
            messages.success(request,"Review Added Successfully")
            context = {
                'postForm': review_form,
                'product': product,
                'review': Review.objects.get(user=request.user, product=product)
            }
            return render(request, 'reviews/review_add.html',context)
        else:
            context = {
                'postForm': review_form,
                'product': product,
                'review': review
            }
            return render(request, 'reviews/review_add.html',context)
    else:
        review_form = ReviewAddForm()
        context = {
            'postForm': review_form,
            'product': product,
            'review': review
        }
    return render(request, 'reviews/review_add.html',context)


@login_required()
def view_reviews(request):
    reviews = Review.objects.filter(user=request.user)
    context={
        'reviews':reviews
    }
    return render(request,'reviews/view_review.html',context)


@login_required()
def remove_from_reviews(request, id):
    try:
        review = Review.objects.get(id=id)
        review.delete()
        return HttpResponseRedirect(reverse("view_review"))
    except ObjectDoesNotExist:
        raise Http404

