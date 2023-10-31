from django.contrib import admin
from .models import AppModel, ContentModel, PageModel, PublishedItemModel, PublishedModel
admin.site.register(AppModel)
admin.site.register(ContentModel)
admin.site.register(PageModel)
admin.site.register(PublishedItemModel)
admin.site.register(PublishedModel)
# Register your models here.
