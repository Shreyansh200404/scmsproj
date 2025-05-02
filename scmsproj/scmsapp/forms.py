from django import forms
from django.contrib.auth.models import User
from .models import *



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

class CustomerForm(forms.ModelForm):
            class Meta:
                model = Customer
                #fields = ['name', 'phone_number', 'address', 'gst_number', 'email']
                fields = '__all__'


class SupplierForm(forms.ModelForm):
     class Meta:
         model = Supplier
         fields = '__all__'


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'




class SalesForm(forms.ModelForm):
    class Meta:
        model= Sales
        fields=['customer','material','quantity_sold','date_of_sale','payment_status']
        widgets={
            'date_of_sale': forms.DateInput(attrs={'type': 'date'}),
        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'
        widgets={
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'




class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

# forms.py
class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)

# forms.py
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('new_password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError('Passwords do not match.')


