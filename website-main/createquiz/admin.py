from django.contrib import admin
from .models import contacts, createlink,feedback,join

# Register your models here.
admin.site.register(createlink)
admin.site.register(feedback)
admin.site.register(contacts)
admin.site.register(join)
