from django import forms
from .models import Review,ReviewImage

RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )


class ReviewAddForm(forms.Form):
    nickname = forms.CharField(max_length=20, required=True, label="Public Name")
    comment = forms.CharField(max_length = 200, required =True)
    rating = forms.ChoiceField(widget=forms.Select,choices=RATING_CHOICES)
    image1 = forms.ImageField(label='Image1', required=False)
    image2 = forms.ImageField(label='Image2', required=False)
    image3 = forms.ImageField(label='Image3', required=False)

