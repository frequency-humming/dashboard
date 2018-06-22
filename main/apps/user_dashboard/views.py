from django.shortcuts import HttpResponse, redirect, render
from django.contrib import messages
from .models import*
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your views here.
def index(request):
    
    return render(request, "user_dashboard/index.html")

def signin(request):

    return render(request, "user_dashboard/signin.html")

def login(request):
    if request.method == "POST":
        try:
            users = User.objects.get(email=request.POST['email'])
        except:
            messages.error(request, 'Invalid email')
            return redirect("/signin")
        if bcrypt.checkpw(request.POST['password'].encode(), users.password.encode()):
            request.session['id'] = users.id
            return redirect("/dashboard/admin")
    else:
        return redirect("/")

def register(request):

    return render(request, "user_dashboard/register.html")

def newuser(request):
    if request.method == "POST":
        error = False
        if len(request.POST['first_name']) < 2:
            messages.error(request, 'First Name must be longer than 2 characters')
            error = True
        if len(request.POST['last_name']) < 2:
            messages.error(request, 'Last Name must be longer than 2 characters')
            error = True
        if any(char.isdigit() for char in request.POST['first_name']):
            messages.error(request, 'First Name cannot contain letters')
            error = True
        if any(char.isdigit() for char in request.POST['last_name']):
            messages.error(request, 'Last Name cannot contain letters')
            error = True
        if len(request.POST['password']) < 8:
            messages.error(request, 'Password must be at least 8 characters')
            error = True
        if not EMAIL_REGEX.match(request.POST['email']):
                messages.error(request, 'Invalid email address')
                error = True
        if request.POST['password'] != request.POST['pwconfirm']:
            messages.error(request, 'Password and Confirmation must match!')
            error = True
        if error:
            return redirect("/register")

        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        this_user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],
        email=request.POST['email'],password=hash1, desc="", level=1)
        request.session['id'] = this_user.id

        return redirect("/dashboard/admin")
    else:
        return redirect("/")
def admin(request):
    
    context = {
        'users': User.objects.all(),
        'active_user': User.objects.get(id=request.session['id'])
    }
    return render(request,"user_dashboard/admin.html", context)

def show(request, id):
    context = {
        'user': User.objects.get(id=id),
        'comments': Comment.objects.filter(user_page__id=id).order_by('-created_at')
    }
    return render(request, "user_dashboard/show.html", context)

def post(request, id):
    Comment.objects.create(content=request.POST['comment'], user_comments=User.objects.get(id=request.session['id']), user_page=User.objects.get(id=id))
    return redirect("/users/show/"+id)

def edit(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, "user_dashboard/edit.html", context)

def edit_user(request,id):
    a = User.objects.get(id=id)
    b = a.level
    if len(request.POST['first_name']) > 1:
        a.first_name = request.POST['first_name']
        a.save()
    if len(request.POST['last_name']) > 1:
        a.last_name = request.POST['last_name']
        a.save()
    if len(request.POST['email']) > 1:
        a.email = request.POST['email']
        a.save()
    if request.POST['level'] == 0:
        a.level = b
        a.save()
    if request.POST['level'] != 0:
        a.level = request.POST['level']
        a.save()
    return redirect("/dashboard/admin")