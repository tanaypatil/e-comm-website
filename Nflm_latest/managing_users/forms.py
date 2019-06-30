from django import forms
from .models import NFLMUser, UserAddress, ContactUs, Customization
from django.core.exceptions import ValidationError


class SignupForm(forms.ModelForm):
    mobile = forms.RegexField(regex=r'^\+?1?\d{10,10}$',required=True,error_messages = {'required':'Phone number must be entered in the format: "9999999999". It should consist of 10 digits.'}, label= "Mobile", widget=forms.TextInput(attrs = {'placeholder':'A 10 digit Mobile No'}))

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

    def signup(self, request, user):
        wsData,created = NFLMUser.objects.get_or_create(username = user.username)
        wsData.mobile = self.cleaned_data['mobile']
        wsData.save()

    class Meta:
        model = NFLMUser
        fields = ('username', 'email', 'mobile')

COUNTRY_CHOICES = (
    ("India", "India"),
)


class AddressForm(forms.ModelForm):
    company_name = forms.CharField(max_length=30, required=False, label="Company Name")
    name = forms.CharField(max_length=80, label="Full Name")
    address = forms.CharField(max_length=120, error_messages={'required': 'Address line1 is required'}, label="Address Line1")
    address2 = forms.CharField(max_length=120, required=False, label="Address Line2")
    city = forms.CharField(max_length=20, error_messages={'required': 'City Name is required'})
    state = forms.CharField(max_length=30, error_messages={'required': 'State is required'})
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select)
    zipcode = forms.RegexField(regex=r'^[1-9][0-9]{5}$', error_messages={'required': 'PinCode must be entered in the '
                               'format: "555555". It should consist of 6 digits.'})
    phone = forms.RegexField(regex=r'^\+?1?\d{10,10}$', required=True, error_messages={'required':'Phone number must be '
                             'entered in the format: "9999999999". It should consist of 10 digits.'}, label="Mobile",
                             widget=forms.TextInput(attrs={'placeholder': 'A 10 digit Mobile No'}))

    class Meta:
        model = UserAddress
        fields = ('company_name', 'name', 'address', 'address2', 'city', 'state', 'country', 'zipcode', 'phone',)


class ContactUsForm(forms.ModelForm):
    name = forms.CharField(max_length=25, error_messages={'required': 'Full Name is required'}, label="Full Name")
    email =forms.EmailField()
    subject = forms.CharField(max_length=50, error_messages={'required': 'subject is required'})
    message = forms.CharField(widget=forms.Textarea, max_length=150)

    class Meta:
        model = ContactUs
        fields = ('name', 'email', 'subject', 'message')


class CustomizationForm(forms.ModelForm):
    name = forms.CharField(max_length=25, required=False, label="Full Name")
    image = forms.ImageField(error_messages={'required': 'Image is required'})
    description = forms.CharField(max_length=150, widget=forms.Textarea(attrs={'style': 'height:150px'}))

    class Meta:
        model = Customization
        fields = ('name', 'image', 'description')
