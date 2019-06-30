from django import forms
from .models import AffiliateProgram,AffiliateBankingDetails
import re
from django import forms
from django.core.validators import validate_email


class MultiEmailField(forms.Field):
    def to_python(self, value):
        if not value:
            return []
        return value.split(',')

    def validate(self, value):
        super(MultiEmailField, self).validate(value)

        for email in value:
            validate_email(email)


class ReferralForm(forms.Form):
    recipients = MultiEmailField(label="Recipients Emails",help_text="Recipients Emails Seperated by comma", widget=forms.Textarea)

    def clean_recipients(self):
        data = self.cleaned_data['recipients']
        return data


class AffiliateAddForm(forms.ModelForm):
    company_name = forms.CharField(max_length=30, required=False)
    first_name=forms.CharField(max_length=20,label="First Name",error_messages={"required":"First Name is Required"})
    last_name=forms.CharField(max_length=20,label="Last Name",error_messages={"required":"Last Name is Required"})
    website=forms.URLField(required=False)

    class Meta:
        model = AffiliateProgram
        fields = ('first_name','last_name','company_name','website')


class AffiliateBankingForm(forms.ModelForm):
    bank_name=forms.CharField(max_length=30,label="Bank Name",error_messages={"required":"Bank Name is Required"})
    account_no=forms.IntegerField(label="Account No",error_messages={"required":"Account No is Required"})
    name=forms.CharField(label="Beneficiary Name",error_messages={"required":"Name is Required"})
    branch=forms.CharField(label="Bank Branch",error_messages={"required":"Branch is Required"})
    IFSC_code=forms.CharField(label="IFSC Code",error_messages={"required":"IFSC Code is Required"})
    city=forms.CharField(label="City",error_messages={"required":"City is Required"})

    class Meta:
        model = AffiliateBankingDetails
        fields = ('bank_name','account_no','name','branch','IFSC_code','city')


