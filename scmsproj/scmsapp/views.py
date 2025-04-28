from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import logout
import random
import string
import io
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
from django.shortcuts import render
import os


from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import get_object_or_404




# Create your views here.
def home(request):
    return render(request, 'home.html')


def register(request):
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request, 'Registration successful! You can now log in.')
                return redirect('/login')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})



def user_login(request):
     if request.method == 'POST':
         username = request.POST.get('username')
         password = request.POST.get('password')
         user_captcha = request.POST.get('captcha')  # Get the CAPTCHA input from the form
         # Check if the user exists in the database
         try:
             user = User.objects.get(username=username)
         except User.DoesNotExist:
             user = None
         # If the user doesn't exist, show an error message
         if user is None:
             messages.error(request, "User not found. Please check your username.")
             return redirect('login')  # Redirect to the login page with an error message
       
         # If the CAPTCHA is incorrect, show an error message
         stored_captcha = request.session.get('captcha')
         if user_captcha != stored_captcha:
             messages.error(request, "Invalid CAPTCHA. Please try again.")
             return redirect('login')  # Redirect back to the login page with an error message

         # If the CAPTCHA is correct, proceed with user authentication
         user = authenticate(request, username=username, password=password)
         if user is not None:
             login(request, user)
             return redirect('dashboard')  # Redirect to the dashboard page after successful login
         else:
             messages.error(request, "Invalid password. Please try again.")
    
     return render(request, 'login.html')










@login_required(login_url='login')
def dashboard(request):
                    if request.user.is_authenticated:   
                        # User is logged in, proceed with the dashboard view
                        return render(request, 'dashboard.html')
                    else:
                        # User is not logged in, redirect to the login page
                        return redirect('login')
                    





def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')





def generate_random_string(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def captcha_image(request):
     # Generate a random string
     captcha_text = generate_random_string()
     # Store the CAPTCHA text in the session
     request.session['captcha'] = captcha_text

     # Create an image with dark background
     image = Image.new('RGB', (150, 50), color=(30, 30, 30))  # Dark background (RGB values)
     draw = ImageDraw.Draw(image)
     #font = ImageFont.load_default()
     font = ImageFont.truetype("arial.ttf", 17)  # Load a TTF font (make sure the font file is available)

     # Light color for text to contrast with dark background
     text_color = (255, 255, 255)  # White color for the text

     # Darker gray for lines/noise
     line_color = (50, 50, 50)

     # Add some random lines to make the CAPTCHA harder to read
     for _ in range(5):
         draw.line(
             (random.randint(0, 150), random.randint(0, 50),
              random.randint(0, 150), random.randint(0, 50)),
             fill=line_color)

     # Add the CAPTCHA string to the image
     draw.text((40, 10), captcha_text, fill=text_color, font=font)
     # Save the image to a BytesIO object
     response = HttpResponse(content_type='image/png')
     image.save(response, 'PNG')
     return response








#curd view for customer

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})

def customer_detail(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    return render(request, 'customer_detail.html', {'customer': customer})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customer_form.html', {'form': form})

def customer_update(request, customer_id):
    customer = Customer.objects.get(pk=customer_id  )
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_form.html', {'form': form})

def customer_confirm_delete(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully!')
        return redirect('customer_list')
    return render(request, 'customer_confirm_delete.html', {'customer': customer})






#curd view for supplier

def supplier_list(request):
        suppliers = Supplier.objects.all()
        return render(request, 'supplier_list.html', {'suppliers': suppliers})

def supplier_detail(request, supplier_id):
        supplier = Supplier.objects.get(pk=supplier_id)
        return render(request, 'supplier_detail.html', {'supplier': supplier})

def supplier_create(request):
        if request.method == 'POST':
            form = SupplierForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Supplier created successfully!')
                return redirect('supplier_list')
        else:
            form = SupplierForm()
        return render(request, 'supplier_form.html', {'form': form})

def supplier_update(request, supplier_id):
        supplier = Supplier.objects.get(pk=supplier_id)
        if request.method == 'POST':
            form = SupplierForm(request.POST, instance=supplier)
            if form.is_valid():
                form.save()
                messages.success(request, 'Supplier updated successfully!')
                return redirect('supplier_list')
        else:
            form = SupplierForm(instance=supplier)
        return render(request, 'supplier_form.html', {'form': form})

def supplier_confirm_delete(request, supplier_id):
        supplier = Supplier.objects.get(pk=supplier_id)
        if request.method == 'POST':
            supplier.delete()
            messages.success(request, 'Supplier deleted successfully!')
            return redirect('supplier_list')
        return render(request, 'supplier_confirm_delete.html', {'supplier': supplier})


# views.py
from django.utils import timezone
from datetime import timedelta

def verify_otp_view(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('forgot_password')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            try:
                otp_obj = PasswordResetOTP.objects.filter(
                    user=user, otp=entered_otp
                ).latest('created_at')
                
                if timezone.now() - otp_obj.created_at < timedelta(minutes=10):  # OTP valid for 10 minutes
                    return redirect('reset_password')
                else:
                    form.add_error('otp', 'OTP expired')
            except PasswordResetOTP.DoesNotExist:
                form.add_error('otp', 'Invalid OTP')
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form})


# views.py
def reset_password_view(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('forgot_password')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            del request.session['reset_user_id']
            return redirect('login')
    else:
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})


# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from .models import PasswordResetOTP
# from .forms import ForgotPasswordForm
# import random

# def generate_otp():
#     return str(random.randint(100000, 999999))

# def forgot_password_view(request):
#     if request.method == 'POST':
#         form = ForgotPasswordForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             try:
#                 user = User.objects.get(email=email)
#                 otp = generate_otp()
#                 PasswordResetOTP.objects.create(user=user, otp=otp)
                
#                 send_mail(
#                     subject='Your Password Reset OTP',
#                     message=f'Your OTP for resetting password is: {otp}',
#                     from_email='your@email.com',
#                     recipient_list=[email],
#                     fail_silently=False
#                 )
#                 request.session['reset_user_id'] = user.id
#                 return redirect('verify_otp')
#             except User.DoesNotExist:
#                 form.add_error('email', 'Email not found.')
#     else:
#         form = ForgotPasswordForm()
#     return render(request, 'forgot_password.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import PasswordResetOTP
from .forms import ForgotPasswordForm
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = generate_otp()
                PasswordResetOTP.objects.create(user=user, otp=otp)
                
                send_mail(
                    subject='Your Password Reset OTP',
                    message=f'Your OTP for resetting password is: {otp}',
                    from_email='your@email.com',
                    recipient_list=[email],
                    fail_silently=False
                )
                request.session['reset_user_id'] = user.id
                return redirect('verify_otp')
            except User.DoesNotExist:
                form.add_error('email', 'Email not found.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form': form})


# CRUD views for Material

def material_list(request):
            materials = Material.objects.all()
            return render(request, 'material_list.html', {'materials': materials})

def material_detail(request, material_id):
            material = Material.objects.get(pk=material_id)
            return render(request, 'material_detail.html', {'material': material})

def material_create(request):
            if request.method == 'POST':
                form = MaterialForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Material created successfully!')
                    return redirect('material_list')
            else:
                form = MaterialForm()
            return render(request, 'material_form.html', {'form': form})

def material_update(request, material_id):
            material = Material.objects.get(pk=material_id)
            if request.method == 'POST':
                form = MaterialForm(request.POST, instance=material)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Material updated successfully!')
                    return redirect('material_list')
            else:
                form = MaterialForm(instance=material)
            return render(request, 'material_form.html', {'form': form})

def material_confirm_delete(request, material_id):
            material = Material.objects.get(pk=material_id)
            if request.method == 'POST':
                material.delete()
                messages.success(request, 'Material deleted successfully!')
                return redirect('material_list')
            return render(request, 'material_confirm_delete.html', {'material': material})




# CRUD views for Stock

def stock_list(request):
                stocks = Stock.objects.all()
                return render(request, 'stock_list.html', {'stocks': stocks})

def stock_detail(request, stock_id):
                stock = Stock.objects.get(pk=stock_id)
                return render(request, 'stock_detail.html', {'stock': stock})

def stock_create(request):
                if request.method == 'POST':
                    form = StockForm(request.POST)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Stock created successfully!')
                        return redirect('stock_list')
                else:
                    form = StockForm()
                return render(request, 'stock_form.html', {'form': form})

def stock_update(request, stock_id):
                stock = Stock.objects.get(pk=stock_id)
                if request.method == 'POST':
                    form = StockForm(request.POST, instance=stock)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Stock updated successfully!')
                        return redirect('stock_list')
                else:
                    form = StockForm(instance=stock)
                return render(request, 'stock_form.html', {'form': form})

def stock_confirm_delete(request, stock_id):
                stock = Stock.objects.get(pk=stock_id)
                if request.method == 'POST':
                    stock.delete()
                    messages.success(request, 'Stock deleted successfully!')
                    return redirect('stock_list')
                return render(request, 'stock_confirm_delete.html', {'stock': stock})





# CRUD views for Sales

def sales_list(request):
                    sales = Sales.objects.all()
                    return render(request, 'sales_list.html', {'sales': sales})

def sales_detail(request, sales_id):
                    sale = Sales.objects.get(pk=sales_id)
                    return render(request, 'sales_detail.html', {'sale': sale})

def sales_create(request):
                    if request.method == 'POST':
                        form = SalesForm(request.POST)
                        if form.is_valid():
                           
                            s=Stock.objects.get(material=form.cleaned_data['material'])
                            if s.quantity_available<form.cleaned_data['quantity_sold']:
                                messages.error(request, 'Sale quantity exceeds available stock!')
                                return render(request, 'sales_form.html', {'form': form})
                            else:
                                form.save()
                                s.quantity_available-=form.cleaned_data['quantity_sold']
                                s.save()
                                messages.success(request, 'Sale created successfully!')
                                return redirect('sales_list')
                    else:
                        form = SalesForm()
                    return render(request, 'sales_form.html', {'form': form})



# from django.contrib import messages

# def sales_create(request):
#     if request.method == 'POST':
#         form = SalesForm(request.POST)
#         if form.is_valid():
#             material = form.cleaned_data['material']
#             quantity_sold = form.cleaned_data['quantity_sold']
            
#             try:
#                 stock = Stock.objects.get(material=material)
#             except Stock.DoesNotExist:
#                 messages.error(request, 'Stock for this material does not exist.')
#                 return redirect('sales_create')

#             if quantity_sold > stock.quantity_available:
#                 messages.error(request, 'Sale quantity exceeds available stock!')
#                 return render(request, 'sales_form.html', {'form': form})
            
#             form.save()
#             stock.quantity_available -= quantity_sold
#             stock.save()
#             messages.success(request, 'Sale created successfully!')
#             return redirect('sales_list')
#     else:
#         form = SalesForm()
    
#     return render(request, 'sales_form.html', {'form': form})

def sales_update(request, sales_id):
                    sale = Sales.objects.get(pk=sales_id)
                    if request.method == 'POST':
                        form = SalesForm(request.POST, instance=sale)
                        if form.is_valid():
                            form.save()
                            messages.success(request, 'Sale updated successfully!')
                            return redirect('sales_list')
                    else:
                        form = SalesForm(instance=sale)
                    return render(request, 'sales_form.html', {'form': form})

def sales_confirm_delete(request, sales_id):
                    sale = Sales.objects.get(pk=sales_id)
                    if request.method == 'POST':
                        sale.delete()
                        messages.success(request, 'Sale deleted successfully!')
                        return redirect('sales_list')
                    return render(request, 'sales_confirm_delete.html', {'sale': sale})





# CRUD views for Purchase

def purchase_list(request):
                        purchases = Purchase.objects.all()
                        return render(request, 'purchase_list.html', {'purchases': purchases})

def purchase_detail(request, purchase_id):
                        purchase = Purchase.objects.get(pk=purchase_id)
                        return render(request, 'purchase_detail.html', {'purchase': purchase})

# def purchase_form(request):
#     # Fetch suppliers from the database
#     suppliers = Supplier.objects.all()  # Ensure Supplier model is imported
#     return render(request, 'purchase_form.html', {'suppliers': suppliers})



def purchase_create(request):
                        if request.method == 'POST':
                            form = PurchaseForm(request.POST)
                            if form.is_valid():
                                form.save()
                                e=Expense.objects.create(description="Purchase of "+form.cleaned_data['material'], amount=form.cleaned_data['total_cost'], date=form.cleaned_data['purchase_date'],category="Product Purchase")
                                e.save()
                                
                                messages.success(request, 'Purchase created successfully!')
                                return redirect('purchase_list')
                        else:
                            form = PurchaseForm()
                        return render(request, 'purchase_form.html', {'form': form})

def purchase_update(request, purchase_id):
                        purchase = Purchase.objects.get(pk=purchase_id)
                        if request.method == 'POST':
                            form = PurchaseForm(request.POST, instance=purchase)
                            if form.is_valid():
                                form.save()
                                messages.success(request, 'Purchase updated successfully!')
                                return redirect('purchase_list')
                        else:
                            form = PurchaseForm(instance=purchase)
                        return render(request, 'purchase_form.html', {'form': form})

def purchase_confirm_delete(request, purchase_id):
                        purchase = Purchase.objects.get(pk=purchase_id)
                        if request.method == 'POST':
                            purchase.delete()
                            messages.success(request, 'Purchase deleted successfully!')
                            return redirect('purchase_list')
                        return render(request, 'purchase_confirm_delete.html', {'purchase': purchase})



# CRUD views for Expense

def expense_list(request):
                            expenses = Expense.objects.all()
                            return render(request, 'expense_list.html', {'expenses': expenses})

def expense_detail(request, expense_id):
                            expense = Expense.objects.get(pk=expense_id)
                            return render(request, 'expense_detail.html', {'expense': expense})

def expense_create(request):
                            if request.method == 'POST':
                                form = ExpenseForm(request.POST)
                                if form.is_valid():
                                    form.save()
                                    messages.success(request, 'Expense created successfully!')
                                    return redirect('expense_list')
                            else:
                                form = ExpenseForm()
                            return render(request, 'expense_form.html', {'form': form})

def expense_update(request, expense_id):
                            expense = Expense.objects.get(pk=expense_id)
                            if request.method == 'POST':
                                form = ExpenseForm(request.POST, instance=expense)
                                if form.is_valid():
                                    form.save()
                                    messages.success(request, 'Expense updated successfully!')
                                    return redirect('expense_list')
                            else:
                                form = ExpenseForm(instance=expense)
                            return render(request, 'expense_form.html', {'form': form})

def expense_confirm_delete(request, expense_id):
                            expense = Expense.objects.get(pk=expense_id)
                            if request.method == 'POST':
                                expense.delete()
                                messages.success(request, 'Expense deleted successfully!')
                                return redirect('expense_list')
                            return render(request, 'expense_confirm_delete.html', {'expense': expense})


# CRUD views for Invoice

# def invoice_list(request):
#                                 invoices = Invoice.objects.all()
#                                 return render(request, 'invoice_list.html', {'invoices': invoices})

# def invoice_detail(request, invoice_id):
#                                 invoice = Invoice.objects.get(pk=invoice_id)
#                                 return render(request, 'invoice_detail.html', {'invoice': invoice})

# def invoice_create(request):
#                                 if request.method == 'POST':
#                                     form = InvoiceForm(request.POST)
#                                     if form.is_valid():
#                                         form.save()
#                                         messages.success(request, 'Invoice created successfully!')
#                                         return redirect('invoice_list')
#                                 else:
#                                     form = InvoiceForm()
#                                 return render(request, 'invoice_form.html', {'form': form})

# def invoice_update(request, invoice_id):
#                                 invoice = Invoice.objects.get(pk=invoice_id)
#                                 if request.method == 'POST':
#                                     form = InvoiceForm(request.POST, instance=invoice)
#                                     if form.is_valid():
#                                         form.save()
#                                         messages.success(request, 'Invoice updated successfully!')
#                                         return redirect('invoice_list')
#                                 else:
#                                     form = InvoiceForm(instance=invoice)
#                                 return render(request, 'invoice_form.html', {'form': form})

# def invoice_confirm_delete(request, invoice_id):
#                                 invoice = Invoice.objects.get(pk=invoice_id)
#                                 if request.method == 'POST':
#                                     invoice.delete()
#                                     messages.success(request, 'Invoice deleted successfully!')
#                                     return redirect('invoice_list')
#                                 return render(request, 'invoice_confirm_delete.html', {'invoice': invoice})



# def invoice_list(request):
#     invoices = Invoice.objects.select_related('customer', 'sales').all()
#     invoice_data = []
#     for invoice in invoices:
#         sales = invoice.sales
#         invoice_data.append({
#             'invoice_id': invoice.invoice_id,
#             'customer_id': invoice.customer.customer_id,
#             'customer_name': invoice.customer.name,
#             'sales_id': sales.sales_id,
#             'material': sales.material.name,
#             'quantity': sales.quantity_sold,
#             'price_per_unit': sales.price / sales.quantity_sold if sales.quantity_sold > 0 else 0,
#             'total_price': sales.price,
#             'payment_status': invoice.payment_status,
#         })
#     return render(request, 'invoice_list.html', {'invoices': invoice_data})



# def invoice_detail(request, invoice_id):
#         invoice = Invoice.objects.select_related('customer', 'sales').get(pk=invoice_id)
#         sales = invoice.sales
#         invoice_data = {
#             'invoice_id': invoice.invoice_id,
#             'customer_id': invoice.customer.customer_id,
#             'customer_name': invoice.customer.name,
#             'sales_id': sales.sales_id,
#             'material': sales.material.name,
#             'quantity': sales.quantity_sold,
#             'price_per_unit': sales.price / sales.quantity_sold if sales.quantity_sold > 0 else 0,
#             'total_price': sales.price,
#             'payment_status': invoice.payment_status,
#         }
#         return render(request, 'invoice_detail.html', {'invoice': invoice_data})


# def invoice_create(request):
#         if request.method == 'POST':
#             form = InvoiceForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'Invoice created successfully!')
#                 return redirect('invoice_list')
#         else:
#             form = InvoiceForm()
#         return render(request, 'invoice_form.html', {'form': form})


# def invoice_update(request, invoice_id):
#         invoice = Invoice.objects.get(pk=invoice_id)
#         if request.method == 'POST':
#             form = InvoiceForm(request.POST, instance=invoice)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'Invoice updated successfully!')
#                 return redirect('invoice_list')
#         else:
#             form = InvoiceForm(instance=invoice)
#         return render(request, 'invoice_form.html', {'form': form})


# def invoice_confirm_delete(request, invoice_id):
#         invoice = Invoice.objects.get(pk=invoice_id)
#         if request.method == 'POST':
#             invoice.delete()
#             messages.success(request, 'Invoice deleted successfully!')
#             return redirect('invoice_list')
#         return render(request, 'invoice_confirm_delete.html', {'invoice': invoice})

# CRUD views for InvoiceItem

# def invoice_item_list(request):
#     invoice_items = InvoiceItem.objects.select_related('invoice', 'material').all()
#     return render(request, 'invoice_item_list.html', {'invoice_items': invoice_items})

# def invoice_item_detail(request, invoice_item_id):
#     invoice_item = InvoiceItem.objects.select_related('invoice', 'material').get(pk=invoice_item_id)
#     return render(request, 'invoice_item_detail.html', {'invoice_item': invoice_item})

# def invoice_item_create(request):
#     if request.method == 'POST':
#         form = InvoiceItemForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Invoice Item created successfully!')
#             return redirect('invoice_item_list')
#     else:
#         form = InvoiceItemForm()
#     return render(request, 'invoice_item_form.html', {'form': form})

# def invoice_item_update(request, invoice_item_id):
#     invoice_item = InvoiceItem.objects.get(pk=invoice_item_id)
#     if request.method == 'POST':
#         form = InvoiceItemForm(request.POST, instance=invoice_item)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Invoice Item updated successfully!')
#             return redirect('invoice_item_list')
#     else:
#         form = InvoiceItemForm(instance=invoice_item)
#     return render(request, 'invoice_item_form.html', {'form': form})

# def invoice_item_confirm_delete(request, invoice_item_id):
#     invoice_item = InvoiceItem.objects.get(pk=invoice_item_id)
#     if request.method == 'POST':
#         invoice_item.delete()
#         messages.success(request, 'Invoice Item deleted successfully!')
#         return redirect('invoice_item_list')
#     return render(request, 'invoice_item_confirm_delete.html', {'invoice_item': invoice_item})


# CRUD views for Invoice

def invoice_list(request):
    invoices = Sales.objects.select_related('customer', 'material').all()
    invoice_data = []
    for sale in invoices:
        invoice_data.append({
            'customer_id': sale.customer.customer_id,
            'customer_name': sale.customer.name,
            'sales_id': sale.sales_id,
            'material_name': sale.material.name,
            'quantity': sale.quantity_sold,
            'price_per_unit': sale.price / sale.quantity_sold if sale.quantity_sold > 0 else 0,
            'total_price': sale.price,
        })
    return render(request, 'invoice_list.html', {'invoices': invoice_data})

def invoice_detail(request, sales_id):
    sale = Sales.objects.select_related('customer', 'material').get(pk=sales_id)
    invoice_data = {
        'customer_id': sale.customer.customer_id,
        'customer_name': sale.customer.name,
        'customer_email': sale.customer.email,
        'customer_phone': sale.customer.phone_number,
        'customer_address': sale.customer.address,
        'sales_id': sale.sales_id,
        'material_name': sale.material.name,
        'quantity': sale.quantity_sold,
        'price_per_unit': sale.price / sale.quantity_sold if sale.quantity_sold > 0 else 0,
        'total_price': sale.price,
        'payment_status': sale.payment_status,  # Added payment status from Sales model
        'sales_date': sale.date_of_sale,  # Added sales date from Sales model
    }
    return render(request, 'sales_detail.html', {'invoice': invoice_data})




# from django.shortcuts import render
# from django.utils.timezone import datetime
# from .models import Sales  # and any other models like Expenses, Materials

# def monthly_report(request, year, month):
#     sales = Sales.objects.filter(date_year=year, date_month=month)

#     total_sales = sum(sale.price for sale in sales)
#     total_quantity = sum(sale.quantity_sold for sale in sales)
#     total_transactions = sales.count()

#     context = {
#         'sales': sales,
#         'year': year,
#         'month': month,
#         'total_sales': total_sales,
#         'total_quantity': total_quantity,
#         'total_transactions': total_transactions,
#     }

#     return render(request, 'monthly_report.html', context)



from django.db.models import Sum
from django.shortcuts import render

def overall_report(request):
    # Total Sales and Quantity
    sales_data = Sales.objects.aggregate(
        total_sales_amount=Sum('price'),
        total_quantity_sold=Sum('quantity_sold')
    )

    # Total Expenses
    expense_data = Expense.objects.aggregate(
        total_expenses=Sum('amount')
    )

    # Net Profit
    total_sales = sales_data['total_sales_amount'] or 0
    total_expenses = expense_data['total_expenses'] or 0
    net_profit = total_sales - total_expenses

    # Payment Status Count
    payment_summary = Sales.objects.values('payment_status').annotate(count=Sum('quantity_sold'))

    context = {
        'total_sales_amount': total_sales,
        'total_quantity_sold': sales_data['total_quantity_sold'] or 0,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'payment_summary': payment_summary,
    }
    return render(request, 'overall_report.html', context)