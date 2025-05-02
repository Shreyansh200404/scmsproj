from django.db import models
from django.contrib.auth.models import User

# 2. Customer Model
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    #gst_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

# 3. Supplier Model
class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    material_supplied = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 4. Material Model
class Material(models.Model):
    material_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# 5. Stock Model
class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity_available = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.material.name} - {self.quantity_available}"




class Sales(models.Model):
    sales_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity_sold = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
   
   # price_per_unit=models.ForeignKey(Material, on_delete=models.CASCADE, related_name='material_price_per_unit')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_sale = models.DateField()
    payment_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Pending', 'Pending')])

    def __str__(self):
        return f"Sale {self.sales_id} - {self.customer.name}"
    
    

# 7. Purchase Model
class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    #material = models.ForeignKey(Material, on_delete=models.CASCADE)
    material=models.CharField(max_length=100)
    quantity_purchased = models.DecimalField(max_digits=10, decimal_places=2)
    #cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()

    def __str__(self):
        return f"Purchase {self.purchase_id} - {self.supplier.name}"



# 8. Expense Model
class Expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=[
        ('Fuel', 'Fuel'),
        ('Maintenance', 'Maintenance'),
        ('Salary', 'Salary'),
        ('product purchase', 'Product Purchase'),
        ('Other', 'Other'),
    ])

    def __str__(self):
        return f"Expense {self.expense_id} - {self.category}"



import uuid

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.otp}"
        