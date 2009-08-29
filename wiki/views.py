# Create your views here.
from dponiwiki.wiki.models import Page
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import markdown

def view_page(request, page_name):
        try:
                page = Page.objects.get(pk=page_name)
        except Page.DoesNotExist:
                return render_to_response("create.html", {"page_name":page_name})

        content = page.content
        return render_to_response("view.html", {"page_name":page_name, "content":content})

def edit_page(request, page_name):
        try:
                page = Page.objects.get(pk=page_name)
                content = page.content
        except Page.DoesNotExist:
                content = ""
        return render_to_response("edit.html", {"page_name":page_name, "content":content})

def save_page(request, page_name):
        content = request.POST["content"]
        try:
                page = Page.objects.get(pk=page_name)
                page.content = content
        except Page.DoesNotExist:
                page = Page(name=page_name, content=content)
        page.save()
        return HttpResponseRedirect("/dponiwiki/" + page_name + "/")

