from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'hello.views.home'),
    url(r'^test_form[/]?$', 'hello.views.test_form'),
    url(r'^awesome[/]?$', 'hello.views.awesome'),
    url(r'^rot13[/]?$', 'hello.views.rot13'),
    url(r'^signup[/]?$', 'hello.views.signup'),
    url(r'^welcome[/]?$', 'hello.views.welcome'),
    url(r'shoppinglist[/]?$', 'hello.views.shoppinglist'),
    url(r'fizzbuzz[/]?$', 'hello.views.fizzbuzz'),
    url(r'asciichan[/]?$', 'hello.views.asciichan'),
    url(r'blog[/]?$', 'hello.blog.blog.blogHome'),
    url(r'blog/[0-9]+[/]?$', 'hello.blog.blog.blogPermaLink'),
    url(r'blog/newpost[/]?$', 'hello.blog.blog.blogNewPost')
)
