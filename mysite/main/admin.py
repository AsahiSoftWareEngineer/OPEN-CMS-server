from django.contrib import admin
from .models import AppModel, ContentModel, PageModel
admin.site.register(AppModel)
admin.site.register(ContentModel)
admin.site.register(PageModel)
# Register your models here.
