from django import http
from django.template import Context, RequestContext, Template
from django.template.loader import get_template
from google.appengine.ext import db
import cgi
import re
import blog

class AsciiArt(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


form = Template("""
<form method="post" action={{destination}}>{% csrf_token %}
    <input type="text" name="super_move" value="Type in Gyarados's coolest move.">
    <input type="submit" value="HYPER JAMMER">
</form>
""")

def plaintext(message):
    return '<plaintext>' + message + '</plaintext>'

def asciichan(request):
    response = http.HttpResponse()
    template = get_template('asciichan.html')
    errors = []

    title = ""
    art = ""
    if (request.method == 'POST'):
        title = request.POST['title_submission']
        art = request.POST['art_submission']
        if title and art and title != "" and art != "":
            submission = AsciiArt(title = title, 
                                art = art)
            submission.put()
            return http.HttpResponseRedirect(request.path)
        else:
            errors.append("Need both title and art fields to be filled in.")

    posts = db.GqlQuery("select * from AsciiArt order by created desc")    

    context = RequestContext(request, {'destination': request.path, 'errors': errors,
                                        'title': title, 'art': art,
                                       'posts': posts})
    response.write(template.render(context))
    return response

def fizzbuzz(request):
    response = http.HttpResponse()
    template = get_template('fizzbuzz.html')
    context = Context({'range': xrange(1, 100+1)})
    
    response.write(template.render(context))
    return response

def shoppinglist(request):
    response = http.HttpResponse()
    template = get_template('shoppinglist.html')

    if not request.method == 'GET':
        response.write('Should be using "GET" method')
        return response
    
    items = request.GET.getlist('food')

    context = Context({'destination': request.path,
                      'items': items})
    response.write(template.render(context))
    return response

def signup(request):
    response = http.HttpResponse()
    signup_form = """
    <form action={{path}} method="POST">{% csrf_token %}
        Username <input type="text" name="username" value={{username}}>
        <div style="color:red"> {{username_error}}</div>
        Password <input type="password" name="password" value={{password}}>
        <div style="color:red"> {{password_error}}</div>
        Re-type Password <input type="password" name="verify">
        <div style="color:red"> {{verify_error}}</div>
        E-mail(optional) <input type="text" name="email" value={{email}}>
        <div style="color:red"> {{email_error}}</div>
        <input type="submit" value="Sign me up!">
    </form>
    """
    
    username = ""
    password = ""
    email = ""
    verify = ""

    username_error = ""
    password_error = ""
    verify_error = ""
    email_error = ""

    signup_form = Template(signup_form)
    if request.method == 'POST':
        if 'username' in request.POST:
            username = request.POST['username']
        if 'password' in request.POST:
            password = request.POST['password']
        if 'verify' in request.POST:
            verify = request.POST['verify']
        if 'email' in request.POST:
            email = request.POST['email']

    user_re = re.compile("^[a-zA-Z0-9_-]{3,20}$")
    password_re = re.compile("^.{3,20}$")
    email_re = re.compile("^[\S]+@[\S]+\.[\S]+$") 

    error = False
    if not user_re.match(username) and len(username) > 0:
        username_error = "That is not a valid username."
        error = True
    if not password_re.match(password) and len(password) > 0:
        password_error ="That is not a valid password."
        error = True
    if not password == verify:
        verify_error = "Passwords don't match."
        error = True
    if not email_re.match(email) and len(email) > 0:
        email_error = "That is not a valid email"
        error = True
    if len(username) == 0 or len(password) == 0:
        error = True

    signup_context = RequestContext(request, {'path': request.path, 
                        'username': username, 'password': '', 'email': email,
                        'username_error':username_error, 'password_error':password_error,
                        'verify_error': verify_error, 'email_error': email_error})

    response.write(signup_form.render(signup_context))

    if not error:
        return http.HttpResponseRedirect('/welcome?username=%s'%username)
    else:
        return response

def welcome(request):
    if request.method == 'GET' and'username' in request.GET:
        return http.HttpResponse('Welcome aboarrrrrd, matey %s!'%request.GET['username'])
    else:
        return http.HttpResponse('Please sign up at the sign up page')

def rot13(request):
    response = http.HttpResponse()
    t = 'Please type something in the form<br>'
    rot_message = ""
    if 'text' in request.POST:    
        message = request.POST['text']
        for c in message:
            if ord(c) >= ord('A') and ord(c) <= ord('Z'):
                if ord(c) + 13 <= ord('Z'):
                    rot_message += chr(ord(c)+13)
                else:
                    rot_message += chr(ord(c)-13)
            elif ord(c) >= ord('a') and ord(c) <= ord('z'):
                if ord(c) + 13 <= ord('z'):
                    rot_message += chr(ord(c)+13)
                else:
                    rot_message += chr(ord(c)-13)
            else:
                rot_message += c

    t += """
    <form action="{{path}}" method="POST">{% csrf_token %}
    <textarea name="text" rows="10" cols="100">{{message}}</textarea>
    <input type="submit">
    </form>"""

    t = Template(t)
    #esc_message = cgi.escape(rot_message, quote = True)
    c = RequestContext(request, {"path": request.path, "message": rot_message})

    response.write(t.render(c))
    return response
            
def awesome(request):
    t = Template("{{super_move}}? You ain't no Pokemon!")
    c = Context({"super_move": request.GET['super_move'].capitalize()})
    response = http.HttpResponse(t.render(c))
    return response

def home(request):
    c = RequestContext(request, {"destination": request.path})
    t = get_template("home.html")
    
    response = http.HttpResponse()
    response.write(t.render(c))

    viewNum = request.COOKIES.get('views', '0')
    if (viewNum.isdigit()):
        viewNum = int(viewNum) + 1
    response.set_cookie('views', str(viewNum))
    print "Views = ", viewNum
    
    if request.method=='POST' and request.POST['super_move'].lower() == 'hyper beam':
        response = http.HttpResponseRedirect('/awesome?super_move=%s'%request.POST['super_move'])
    return response

def test_form(request):
    response = http.HttpResponse()
    c = RequestContext(request, {})
    if request.method == 'POST':
        response.write("c00l")
        response.write("<br>")
        response.write(plaintext(str(request)))
    else:
        response.write("cool")
    '''
    response = http.HttpResponse()
    #response['Content-Type'] = 'text/plain'
    response.write('This is a test form!')
    if response['Content-Type'] != 'text/html':
        response.write('\n')
    else:
        response.write('<br>')

    if (request.method == 'GET'):
        response.write(request.GET['q'])
    elif request.method == 'POST':
        response.write(request.POST['q'])
    #response.write(str(request))'''
    return response
