from django import http
from django.template import Context, RequestContext, Template
from django.template.loader import get_template
from google.appengine.ext import db
import os

homeDir = '/blog'
newPostDir = '/blog/newpost'

class BlogPost(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    posted = db.DateTimeProperty(auto_now_add = True)

def blogPermaLink(request):
    template = get_template("blog/permalink.html")
    response = http.HttpResponse()

    post = BlogPost.get_by_id(long(os.path.basename(request.path)))

    context = Context({'post': post, 'home': homeDir})

    response.write(template.render(context))
    return response
    
def blogNewPost(request):
    template = get_template("blog/newpost.html")
    response = http.HttpResponse()
    error = ''
    subject = ''
    content = ''

    if request.method == 'POST':
        subject = request.POST.get('subject')
        content = request.POST.get('content')

        if subject and content and subject != "" and content != "":
            post = BlogPost(subject = subject, content = content)
            post.put()
            postID = str(post.key().id())
            return http.HttpResponseRedirect(os.path.join(homeDir, postID))
        else:
            error = 'Need both subject and content to be filled in'

    context = RequestContext(request, {'destination': request.path, 'error': error})
    response.write(template.render(context))
    return response

def blogHome(request):
    template = get_template("blog/blog.html")
    response = http.HttpResponse()

    posts = db.GqlQuery("select * from BlogPost order by posted desc")

    context = RequestContext(request, {'posts': posts})
    response.write(template.render(context))
    return response
