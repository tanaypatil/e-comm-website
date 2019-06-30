from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# Register your models here.

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = NFLMUser
        fields = ('username', 'email', 'mobile')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = NFLMUser
        fields = ('username', 'email', 'password', 'mobile', 'first_name', 'last_name', 'is_active', )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserResource(resources.ModelResource):
    class Meta:
        model = NFLMUser


class UserAdmin(BaseUserAdmin,ImportExportModelAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    resource_class = UserResource

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'mobile', 'date_joined', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'mobile',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'mobile', 'password1', 'password2')}
        ),
    )
    search_fields = ('username', 'email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(NFLMUser, UserAdmin)


class UserAddressResource(resources.ModelResource):
    class Meta:
        model = UserAddress


class AddressAdmin(ImportExportModelAdmin):
    model = UserAddress
    list_display = ('user', 'address', 'state', 'city', 'updated')
    search_fields = ['user', 'address', 'city']

admin.site.register(UserAddress, AddressAdmin)


class ContactUsAdmin(admin.ModelAdmin):
    model = ContactUs
    list_display = ('name', 'email', 'subject', )
    search_fields = ['name', 'email', 'message']

admin.site.register(ContactUs, ContactUsAdmin)


class CustomizationAdmin(admin.ModelAdmin):
    model = Customization
    list_display = ('user_name', 'user_mobile', 'name', 'timestamp')
    search_fields = ['user__username', 'name', 'user__mobile']
    readonly_fields = ['timestamp']

    def user_mobile(self, obj):
        return obj.user.mobile

    user_mobile.short_description = 'Mobile'
    user_mobile.admin_order_field = 'user__mobile'

    def user_name(self, obj):
        return obj.user.username

    user_name.short_description = 'Name'
    user_name.admin_order_field = 'user__name'

admin.site.register(Customization, CustomizationAdmin)


class HowToUseAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'date_added']
    readonly_fields = ['date_added']
    search_fields = ['title']
    list_filter = ['date_added']


admin.site.register(HowToUseVideo,HowToUseAdmin)

