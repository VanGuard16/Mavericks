from django.contrib import admin
from .models import Profile
from .models import Event
from .models import Photo
# Register your models here.
admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(Photo)