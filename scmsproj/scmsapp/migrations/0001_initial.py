# Generated by Django 5.1.7 on 2025-04-25 13:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('expense_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('category', models.CharField(choices=[('Fuel', 'Fuel'), ('Maintenance', 'Maintenance'), ('Salary', 'Salary'), ('product purchase', 'Product Purchase'), ('Other', 'Other')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('material_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('supplier_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('material_supplied', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('invoice_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(choices=[('Paid', 'Paid'), ('Pending', 'Pending')], max_length=10)),
                ('invoice_date', models.DateField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scmsapp.customer')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('invoice_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='scmsapp.invoice')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scmsapp.material')),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('sales_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity_sold', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_of_sale', models.DateField()),
                ('payment_status', models.CharField(choices=[('Paid', 'Paid'), ('Pending', 'Pending')], max_length=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scmsapp.customer')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scmsapp.material')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='sales',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scmsapp.sales'),
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('stock_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity_available', models.DecimalField(decimal_places=2, max_digits=10)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scmsapp.material')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('purchase_id', models.AutoField(primary_key=True, serialize=False)),
                ('material', models.CharField(max_length=100)),
                ('quantity_purchased', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchase_date', models.DateField()),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scmsapp.supplier')),
            ],
        ),
    ]
