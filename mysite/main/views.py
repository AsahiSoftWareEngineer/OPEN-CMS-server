from ast import arg
from tokenize import group
from urllib import request
from django.shortcuts import render
from django.views.generic import View
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token

import json

from .module.auth import  Account
from .module.management import App, Drive, SDK


# Create your views here.
# レスポンスにCookieを含めるための関数
def SetCookieResponse(params, cookies):
    response = HttpResponse(json.dumps(params))
    for i in cookies:
        response.set_cookie(key=i["key"], value=i["value"], httponly=True, max_age=i["max_age"])
    return response
# Cookieを削除するための関数
def DeleteCookieResponse(params, cookies):
    response = HttpResponse(json.dumps(params))
    for i in cookies:
        response.delete_cookie(i["key"])

# CSRF TOKENの取得 
@csrf_exempt
def get_csrf_token(request):
    return JsonResponse({"token": get_token(request)})

#認証のためのクラス





@method_decorator(csrf_exempt, name="dispatch")
class AccountView(View):
    def post(self, request, *args, **kwargs):
        params = json.loads(request.body)
        if(params["command"] == "set_token"):
            return SetCookieResponse(
                params={"response": 200},
                cookies=[
                    {"key": "access_token", "value": params["access_token"], "max_age": None},
                    {"key": "refresh_token", "value": params["refresh_token"], "max_age": 60*60*24*30}
                ]
            )
            
        elif (params["command"] == "has_account?"):
            refresh_token = request.COOKIES.get("refresh_token")
            if (refresh_token):
                return JsonResponse({"response": True})
            else:
                return JsonResponse({"response": False})
            
        
        elif (params["command"] == "is_accessable?"):
            try:
                user_id = Account.get_id(request.COOKIES.get("access_token"))
                return JsonResponse({"response": True})
            except:
                return JsonResponse({"response": False})
        
        elif (params["command"] == "get_refresh_token"):
            refresh_token = request.COOKIES.get("refresh_token")
            return JsonResponse({"token": refresh_token})


@method_decorator(csrf_exempt, name="dispatch")
class AppView(View):
    def post(self, request, *args, **kwargs):
        user_id = Account.get_id(request.COOKIES.get("access_token"))
        params = json.loads(request.body)
        app = App(user_id=user_id)
        if(params["command"] == "get"):
            return JsonResponse({"apps": app.get_all()})
        
        elif(params["command"] == "create"):
            return JsonResponse({"response": app.edit(params)})

@method_decorator(csrf_exempt, name="dispatch")
class DriveView(View):
    def post(self, request, *args, **kwargs):
        user_id = Account.get_id(request.COOKIES.get("access_token"))
        params = request.POST 
        drive = Drive(user_id=user_id)
        if(params["command"] == "upload"):
            drive.upload(params, request.FILES.get("image"))
            return JsonResponse({"image": drive.get_image_by_id(id=params["id"])})
        elif(params["command"] == "get"):
            return JsonResponse({"images": drive.get_all()})
    
@method_decorator(csrf_exempt, name="dispatch")
class PageView(View):
    def post(self, request, *args, **kwargs):
        user_id = Account.get_id(request.COOKIES.get("access_token"))
        params = json.loads(request.body)
       
        
        if(params["command"] == "create"):
            app = App(user_id=user_id, app_id=params["app_id"])
            response = app.create_page(params=params, app=app.get_apps())
            return JsonResponse({"response": response})
        
        elif(params["command"] == "get"):
            app = App(user_id=user_id, app_id=params["app_id"])
            return JsonResponse({"urls": app.get_pages()})
        
        elif(params["command"] == "get_draft"):
            app = App(user_id=user_id, app_id=None)
            return JsonResponse({
                "info": app.get_page_by_id(page_id=params["page_id"]),
                "contents": app.get_draft_by_id(page_id=params["page_id"])
                })
        
        elif(params["command"] == "save_as_draft"):
            app = App(user_id=user_id, app_id=params["app_id"])
            return JsonResponse({"response": app.save_as_draft(params)})
        
        elif(params["command"] == "published"):
            app = App(user_id=user_id, app_id=params["app_id"])
            app.save_as_draft(params)
            return JsonResponse({"response":  app.publised_page(params)})


#本番データを取得して返すビュー
@method_decorator(csrf_exempt, name="dispatch")
class APIGetView(View):
    def post(self, request, *args, **kwargs):
        params = json.loads(request.body)
        sdk = SDK(app_key=params["key"], url=params["url"])
        return JsonResponse(sdk.get_content_as_json())

@method_decorator(csrf_exempt, name="dispatch")
class APIArrayView(View):
    def post(self, request, *args, **kwargs):
        params = json.loads(request.body)
        sdk = SDK(app_key=params["key"], url=params["url"])
        return JsonResponse({"contents": sdk.get_contents()})
    
        