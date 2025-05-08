from django.contrib import admin
from .models import Customer, Connection, ContactMessage

admin.site.register(Customer)
admin.site.register(Connection)
admin.site.register(ContactMessage)