from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Profile, Comment, Review
from django import forms
import re


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['img', 'home_address', 'city_town']  # Add home_address and city_town fields here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            profile = self.instance
            self.fields['home_address'].initial = profile.home_address
            self.fields['city_town'].initial = profile.city_town
        except Profile.DoesNotExist:
            pass

    def save(self, commit=True):
        profile = super().save(commit=commit)
        profile.home_address = self.cleaned_data['home_address']
        profile.city_town = self.cleaned_data['city_town']
        profile.save()
        return profile


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }


class BillingAddressForm(forms.Form):
    full_name = forms.CharField(max_length=100, label='Full Name')
    address_line1 = forms.CharField(max_length=255, label='Address Line 1')
    address_line2 = forms.CharField(max_length=255, label='Address Line 2', required=False)
    city_town = forms.CharField(max_length=100, label='City/Town')
    postal_code = forms.CharField(max_length=10, label='Postal Code')
    country = forms.CharField(max_length=100, label='Country')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']  # Fields for the user to provide a rating and comment
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'rating': 'Rating',  # You can customize labels here
            'comment': 'Comment',
        }
        help_texts = {
            'rating': 'Select a rating from 1 to 5.',
            'comment': 'Provide your comments here.',
        }


class CreditCardForm(forms.Form):
    card_number = forms.CharField(
        label='Card Number',
        widget=forms.TextInput(attrs={'placeholder': '*415458745868526'})
    )
    expiry_date = forms.CharField(
        label='Expiry Date',
        widget=forms.TextInput(attrs={'placeholder': '23/11'})
    )
    cvv = forms.CharField(
        label='CVV',
        widget=forms.TextInput(attrs={'placeholder': '123'})
    )

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if not re.match(r'^\*\d{15}$', card_number):
            raise forms.ValidationError('Card number must be in the format *415458745868526')
        return card_number

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data['expiry_date']
        if not re.match(r'^\d{2}/\d{2}$', expiry_date):
            raise forms.ValidationError('Expiry date must be in the format 23/11')
        return expiry_date

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if not re.match(r'^\d{3}$', cvv):
            raise forms.ValidationError('CVV must be 3 digits')
        return cvv
