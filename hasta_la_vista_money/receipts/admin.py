from django.contrib import admin
from hasta_la_vista_money.receipts.models import Customer, Product, Receipt

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Receipt)
