from django.contrib import admin
from .models import AppModel, ContentModel, PageModel, PublishedItemModel
admin.site.register(AppModel)
admin.site.register(ContentModel)
admin.site.register(PageModel)
admin.site.register(PublishedItemModel)
# Register your models here.
