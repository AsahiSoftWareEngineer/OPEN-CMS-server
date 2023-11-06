from asyncio import constants
from datetime import datetime
import os
from ..models import AppModel, PageModel, ContentModel, ShortTextModel, LongTextModel, RichTextModel, DriveModel, ImageModel, PublishedModel, PublishedImageModel, PublishedLongTextModel, PublishedShortTextModel, PublishedItemModel,  PublishedRichTextModel
from django.core.mail import send_mail
from mysite import settings

class App:
    def __init__(self, app_id=None, user_id=None):
        self.app_id = app_id
        self.user_id = user_id
    
    #全てのアプリケーションを取得するメソッド
    def get_all(self):
        apps = []
        app = AppModel.objects.filter(user_id=self.user_id)
        for i in app:
            apps.append({
                "id": i.app_id,
                "api_key": i.api_key,
                "name": i.name,
                "created_at": i.created_at,
                "updated_at": i.updated_at
            })
        return apps
    
    def get_apps(self):
        if(AppModel.objects.filter(app_id=self.app_id).exists()):
            return AppModel.objects.get(app_id=self.app_id)
        else:
            return 404
    
    #アプリケーションを作成/編集するメソッド
    def edit(self, params):
        app = AppModel.objects.update_or_create(
            app_id=params["id"],
            defaults={
                "user_id": self.user_id,
                "name": params["name"],
                "api_key": params["api_key"],
                "created_at": params["created_at"],
                "updated_at": params["updated_at"],
            }
        )
        return True
    
    #URL一覧を取得するメソッド
    def get_pages(self):
        pages = []
        page = PageModel.objects.filter(app__app_id=self.app_id)
        for i in page:
            pages.append({
                "id": i.page_id,
                "url": i.url,
                "name": i.name,
                "created_at": i.created_at,
                "updated_at": i.updated_at,
                "is_blog": i.is_blog_mode,
            })
        return pages
    
    
    #ページを作成するメソッド
    def create_page(self, params, app):
        items = params["items"]
        pages = PageModel.objects.update_or_create(
            page_id=params["id"],
            defaults={
                "app": app,
                "url": params["url"],
                "name": params["name"],
                "created_at": params["created_at"],
                "updated_at": params["updated_at"],
                "is_blog_mode":params["is_blog_mode"]
            }
        )
        for i in items:
            page = pages[0]
            item = ContentModel.objects.update_or_create(
                content_id=i["id"],
                defaults={
                    "page": page,
                    "name": i["name"],
                    "col_name": i["col_name"],
                    "type": i["type"]["value"],
                }
            )[0]
            if(i["type"]["value"] == 0):
                ShortTextModel.objects.update_or_create(
                    parent__content_id=i["id"], 
                    defaults={
                        "parent": item,
                        "content": "",
                    }
                )
            elif(i["type"]["value"] == 1):
                LongTextModel.objects.update_or_create(
                    parent__content_id=i["id"],
                    defaults={
                        "parent": item,
                        "content": "",
                    }
                )
            elif(i["type"]["value"] == 2):
                ImageModel.objects.update_or_create(
                    parent__content_id=i["id"],
                    defaults={
                        "parent": item,
                        "alt": "",
                        "image_id": ""
                    }
                )
            elif(i["type"]["value"] == 3):
                LongTextModel.objects.update_or_create(
                    parent__content_id=i["id"],
                    defaults={
                        "parent": item,
                        "content": "",
                    }
                )
        return True
    
    #下書き保存するメソッド
    
    def save_as_draft(self, params):
        
        page = PageModel.objects.update_or_create(
            page_id=params["id"],
            is_blog_mode=False,
            defaults={
                "page_id": params["id"],
                "app":self.get_apps(),
                "url": params["url"],
                "name": params["name"],
            })[0]
        items = params["items"]
        for i in items:
            item = ContentModel.objects.update_or_create(
                content_id=i["id"],
                defaults={
                    "page": page,
                    "name": i["name"],
                    "col_name": i["col_name"],
                    "type": i["type"],
                }
            )[0]
            if(i["type"] == 0):
                ShortTextModel.objects.update_or_create(
                    parent__content_id=i["id"], 
                    defaults={
                        "parent": item,
                        "content": i["content"],
                    }
                )
            elif(i["type"] == 1):
                LongTextModel.objects.update_or_create(
                    parent__content_id=i["id"],
                    defaults={
                        "parent": item,
                        "content": i["content"],
                    }
                )
            elif(i["type"]== 2):
                ImageModel.objects.update_or_create(
                    parent__content_id=i["id"],
                    defaults={
                        "parent": item,
                        "alt": i["alt"],
                        "image_id": i["image_id"],
                    }
                )
            elif(i["type"] == 3):
                RichTextModel.objects.update_or_create(
                    parent__content_id=i["id"],
                    defaults={
                        "parent": item,
                        "content": i["content"],
                    }
                )
            pass
        return True
    
    #テキストを取得するメソッド
    def get_short_text_by_id(self, id):
        if(ShortTextModel.objects.filter(parent__content_id=id).exists()):
            return ShortTextModel.objects.get(parent__content_id=id).content
    
    def get_long_text_by_id(self, id):
        if(LongTextModel.objects.filter(parent__content_id=id).exists()):
            return LongTextModel.objects.get(parent__content_id=id).content
    
    def get_rich_text_by_id(self, id):
        if(RichTextModel.objects.filter(parent__content_id=id).exists()):
            return RichTextModel.objects.get(parent__content_id=id).content
    
    def get_image_by_id(self, id):
        if(ImageModel.objects.filter(parent__content_id=id).exists()):
            image = ImageModel.objects.get(parent__content_id=id)
            return {
                "image_id": image.image_id,
                "alt": image.alt
                }
    def get_page_by_id(self, page_id):
        if(PageModel.objects.filter(page_id=page_id).exists()):
            page = PageModel.objects.get(page_id=page_id)
            return {
                "name":page.name,
                "id":page.page_id,
                "app_id": page.app.app_id,
                "url": page.url,
                "is_blog": page.is_blog_mode,
            }
        else:
            return {
                "message": "Page not found"
            }
            
    
    #下書きを取得するメソッド
    def get_draft_by_id(self, page_id):
        contents = []
        content = ContentModel.objects.filter(page__page_id=page_id)
        for i in content:
            if(i.type == 0):
                contents.append({
                    "id": i.content_id,
                    "type": i.type,
                    "name": i.name,
                    "col_name": i.col_name,
                    "content": self.get_short_text_by_id(id=i.content_id)
                })
            elif(i.type == 1):
                contents.append({
                    "id": i.content_id,
                    "type": i.type,
                    "name": i.name,
                    "col_name": i.col_name,
                    "content": self.get_long_text_by_id(id=i.content_id)
                })
            elif(i.type == 2):
                image = self.get_image_by_id(id=i.content_id)
                drive = Drive(self.user_id)
                contents.append({
                    "id": i.content_id,
                    "alt": image["alt"],
                    "name": i.name,
                    "col_name": i.col_name,
                    "type": i.type,
                    "image_id": image["image_id"],
                    "url": drive.get_image_by_id(id=image["image_id"])["url"]
                })
            elif(i.type == 3):
                contents.append({
                    "id": i.content_id,
                    "type": i.type,
                    "name": i.name,
                    "col_name": i.col_name,
                    "content": self.get_rich_text_by_id(id=i.content_id)
                })
        return contents
    
    #コンテンツを公開するメソッド
    def publised_page(self, params):
        parent = PageModel.objects.get(page_id=params["id"])
        page = PublishedModel.objects.update_or_create(
            page_id=params["id"],
            defaults={
                "app": parent.app,
                "url": parent.url,
                "published_at": datetime.now()
            }
        )[0]
        items = params["items"]
        
        for i in items:
            item = PublishedItemModel.objects.update_or_create(
                content_id=i["id"],
                defaults={
                    "page": page,
                    "col_name": i["col_name"],
                    "type": i["type"],
                }
            )[0]
            if(i["type"] == 0):
                PublishedShortTextModel.objects.update_or_create(
                    parent__content_id=i["id"], 
                    defaults={
                        "parent": item,
                        "content": i["content"],
                    }
                )
            elif(i["type"] == 1):
                PublishedLongTextModel.objects.update_or_create(
                    parent__content_id=i["id"],
                    defaults={
                        "parent": item,
                        "content": i["content"],
                    }
                )
            elif(i["type"]== 2):
                PublishedImageModel.objects.update_or_create(
                    parent__content_id=i["id"],
                    defaults={
                        "parent": item,
                        "alt": i["alt"],
                        "image_id": i["image_id"],
                    }
                )
            elif(i["type"] == 3):
                PublishedRichTextModel.objects.update_or_create(
                    parent__content_id=i["id"],
                    defaults={
                        "parent": item,
                        "content": i["content"],
                    }
                )
            pass
        return True
        

            
class Drive:
    def __init__(self, user_id=None):
        self.user_id = user_id
    
    #画像のアップロードを処置するクラス
    def upload(self, params, image):
        drive = DriveModel.objects.create(
            user_id=self.user_id,
            image_id=params["id"],
            image = image
        )
    # idで画像を取得するメソッド
    def get_image_by_id(self, id):
        if(DriveModel.objects.filter(image_id=id).exists()):
            image = DriveModel.objects.get(image_id=id)
            return {
                "url": str(image.image),
                "id": image.image_id,
            }
        else :
            return {
                "url": "",
                "id": ""
            }
            
            
    #全ての画像を取得するメソッド
    def get_all(self):
        images = []
        drive = DriveModel.objects.filter(user_id=self.user_id)
        for i in drive:
            images.append({
                "id": i.image_id,
                "url": str(i.image)
            })
        return images
    
 
class SDK:
    def __init__(self, app_key, url):
        self.key = app_key
        self.url = url
    
    #テキストを取得するメソッド
    def get_short_text_by_id(self, id):
        if(PublishedShortTextModel.objects.filter(parent__content_id=id).exists()):
            return PublishedShortTextModel.objects.get(parent__content_id=id).content
    
    def get_long_text_by_id(self, id):
        if(PublishedLongTextModel.objects.filter(parent__content_id=id).exists()):
            return PublishedLongTextModel.objects.get(parent__content_id=id).content
    def get_rich_text_by_id(self, id):
        if(PublishedRichTextModel.objects.filter(parent__content_id=id).exists()):
            return PublishedRichTextModel.objects.get(parent__content_id=id).content
    
    def get_image_by_id(self, id):
        if(PublishedImageModel.objects.filter(parent__content_id=id).exists()):
            image = PublishedImageModel.objects.get(parent__content_id=id)
            return {
                "image_id": image.image_id,
                "alt": image.alt
                }
    
    def get_content_as_json(self):
        contents = {}
        
    
        
        app = AppModel.objects.get(api_key=self.key) if AppModel.objects.filter(api_key=self.key).exists() else None
        page = PublishedModel.objects.get(app__app_id=app.app_id, url=self.url) if PublishedModel.objects.filter(app__app_id=app.app_id, url=self.url).exists() else None
        
        if(app is None or page is None):
            return {}
   
        content = PublishedItemModel.objects.filter(page=page)
        contents["url"] = self.url.split("/")
        contents["published_at"] = page.published_at.strftime("%Y-%m-%d")
        for i in content:
            if(i.type == 0):
                contents[i.col_name] = self.get_short_text_by_id(id=i.content_id)
            elif(i.type == 1):
                contents[i.col_name] = self.get_long_text_by_id(id=i.content_id)
            elif(i.type == 2):
                image = self.get_image_by_id(id=i.content_id)
                drive = Drive(app.user_id)
                contents[i.col_name] = {
                    "image_id": image["image_id"],
                    "url": drive.get_image_by_id(id=image["image_id"])["url"],
                    "alt": image["alt"],
                }
            elif(i.type == 3):
                contents[i.col_name] = self.get_rich_text_by_id(id=i.content_id)
        return contents
    
    def get_contents(self):
        app = object()
        if(AppModel.objects.filter(api_key=self.key).exists()):
            app = AppModel.objects.get(api_key=self.key)
            pages = PublishedModel.objects.filter(app__app_id=app.app_id)
            contents = []
            for i in pages:
                if(self.url in i.url):
                    sdk = SDK(app_key=self.key, url=i.url)
                    contents.append(sdk.get_content_as_json())
            contents.reverse()
            return contents

        else:
            return []
    
    
        

class Mail:
    def __init__(self, email):
        self.email = email
        self.response_path =  os.path.abspath("main/module/mail/response.txt")
        self.notification_path = os.path.abspath("main/module/mail/notification.txt")
    
    def receive(self, name, message, subject, company):
        f = open(self.response_path, 'r')
        response_mail = f.read()
        f.close()
        
        f = open(self.notification_path, "r")
        notification_mail = f.read()
        f.close()
        
      
        try:
            response_subject = "お問い合わせを受け付けました"
            from_mail = getattr(settings, "DEFAULT_FROM_EMAIL", None)
            recipirent_list = [self.email]
            send_mail(response_subject, response_mail, from_mail, recipirent_list) 
            

            notification_subject = "新規お問い合わせ通知"
            notification_message = notification_mail.replace(r"{{email}}", self.email).replace(r"{{name}}", name).replace(r"{{message}}", message).replace(r"{{subject}}", subject).replace(r"{{company}}", company)
            send_mail(notification_subject, notification_message, from_mail, [from_mail])
            return True
        except:
            return False
           
            
        
        
    