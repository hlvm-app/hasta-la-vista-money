from django.contrib import admin

# Register your models here.
from receipts.models import Receipt

admin.site.register(Receipt)
