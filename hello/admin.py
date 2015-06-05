from django import http
from django.template import Context, RequestContext, Template
from django.template.loader import get_template
from google.appengine.ext import db

def removeVulgarPosts(posts):
    for post in posts:
        if 'haha' in post.title or 'fuck' in post.title:
            post.delete()
