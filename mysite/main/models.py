from distutils.command.upload import upload
from turtle import update
from django.db import models


class AppModel(models.Model):
    user_id = models.IntegerField()
    app_id = models.TextField()
    api_key = models.TextField()
    name = models.CharField()
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

class PageModel(models.Model):
    app = models.ForeignKey(AppModel, on_delete=models.CASCADE)
    page_id = models.TextField()
    url = models.URLField()
    name = models.CharField(max_length=255)
    is_blog_mode = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    

    
class ContentModel(models.Model):
    page = models.ForeignKey(PageModel, on_delete=models.CASCADE)
    content_id = models.TextField()
    name = models.CharField(max_length=255)
    col_name = models.CharField(max_length=255)
    type = models.IntegerField()
    
    

    

class ShortTextModel(models.Model):
    parent = models.ForeignKey(ContentModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=350)

class LongTextModel(models.Model):
    parent = models.ForeignKey(ContentModel, on_delete=models.CASCADE)
    content = models.TextField()

class RichTextModel(models.Model):
    parent = models.ForeignKey(ContentModel, on_delete=models.CASCADE)
    content = models.TextField()
    
    
class ImageModel(models.Model):
    parent = models.ForeignKey(ContentModel, on_delete=models.CASCADE)
    image_id = models.TextField() 
    alt = models.CharField(max_length=255)

class DriveModel(models.Model):
    user_id = models.IntegerField()
    image_id = models.TextField()
    image = models.ImageField(upload_to="img/")
    



class PublishedModel(models.Model):
    app = models.ForeignKey(AppModel, on_delete=models.CASCADE)
    page_id = models.TextField()
    url = models.URLField()
    published_at = models.DateTimeField(null=True)

class PublishedItemModel(models.Model):
    page = models.ForeignKey(PublishedModel, on_delete=models.CASCADE)
    col_name = models.CharField(max_length=255)
    content_id = models.TextField()
    type = models.IntegerField()

class PublishedShortTextModel(models.Model):
    parent = models.ForeignKey(PublishedItemModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)

class PublishedLongTextModel(models.Model):
    parent = models.ForeignKey(PublishedItemModel, on_delete=models.CASCADE)
    content = models.TextField()
    
class PublishedImageModel(models.Model):
    parent = models.ForeignKey(PublishedItemModel, on_delete=models.CASCADE)
    alt = models.CharField(max_length=255)
    image_id = models.TextField()



class PublishedRichTextModel(models.Model):
    parent = models.ForeignKey(PublishedItemModel, on_delete=models.CASCADE)
    content = models.TextField()