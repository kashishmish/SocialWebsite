from django.contrib import admin

# Register your models here.
from .models import Registration,Addpost,Reaction,Comments,Friend_request
admin.site.register(Registration)
admin.site.register(Addpost)
admin.site.register(Reaction)
admin.site.register(Comments)
admin.site.register(Friend_request)