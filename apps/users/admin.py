from django.contrib import admin
from apps.users.models import *

admin.site.register(TestModel)
admin.site.register(Address)
admin.site.register(User)

