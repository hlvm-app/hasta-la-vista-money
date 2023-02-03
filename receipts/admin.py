from django.contrib import admin
from receipts.models import Customer, Receipt, Product


admin.site.register(Customer)
admin.site.register(Receipt)
admin.site.register(Product)
