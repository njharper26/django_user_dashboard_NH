from django.shortcuts import render, redirect
from models import *
from django.contrib import messages

def register(request):
    return render(request, 'u_d/register.html')

def process_register(request):
    result = User.objects.registration_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/register')
    else:
        messages.success(request, "You have successfully registered as an Admin!")
        return redirect('/')

def login(request):
    return render(request, 'u_d/login.html')

def process_login(request):
    result = User.objects.login_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    else:
        messages.success(request, "You have successfully logged in!")
        request.session['id'] = result.id
        user_level = result.user_level.level
    return redirect('/dashboard/' + user_level)

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')

def dashboard(request, user_level):
    context = {
        'user': User.objects.get(id = request.session['id']),
        'users': User.objects.all()
    }
    print context['user'].first_name
    print user_level
    print request.session['id']
    if user_level == 'admin':   
        return render(request, 'u_d/admin_dash.html', context)
    else:
        return render(request, 'u_d/normal_dash.html', context)
    
def add(request):
    context = {
        'user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'u_d/add.html', context)

def process_add(request):
    result = User.objects.registration_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/users/new')
    else:
        messages.success(request, "You have successfully added a new User!")
        return redirect('/dashboard/admin')

def edit_info(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'u_d/edit_user.html', context)

def process_edit_info(request, id):
    result = User.objects.edit_user(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/users/edit/info/' + id)
    else:
        messages.success(request, "You have successfully edited the User info")
        return redirect('/dashboard/admin')

def process_remove(request, id):
    user = User.objects.get(id=id)
    user_level = User_Level.objects.get(user_id=id)
    user.delete()
    user_level.delete()
    messages.success(request, "You have sucessfully removed the User")
    return redirect('/dashboard/admin')

def edit_profile(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'u_d/edit_prof.html', context)

def process_edit_profile(request, id):
    result = User.objects.edit_user(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/users/edit/profile/' + id)
    messages.success(request, "You have successfully edited the User info")
    return redirect('/dashboard/admin')

def show(request, id):
    messages = Message.objects.filter(receiver_id=id).order_by('-created_at')
    messages_list = []
    comments_list = []
    if messages:
        for m in messages:
            comments = m.message_comments.all().order_by('-created_at')
            message = {
                'id': m.id,
                'message': m.message,
                'created_at': m.created_at,
                'sender': m.sender.first_name,
                'comments': comments
            }
            messages_list.append(message)

    context = {
        'user': User.objects.get(id=id),
        'messages_list': messages_list,
        'viewer': User.objects.get(id=request.session['id'])
    }
    return render(request, 'u_d/profile.html', context)

def process_message(request, id):
    result = Message.objects.message_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/users/show/profile/' + id)
    else:  
        messages.success(request, "Message sent successfully!")        
        return redirect('/users/show/profile/' + id)

def process_message(request, id):
    result = Message.objects.message_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/users/show/profile/' + id)
    else:  
        messages.success(request, "Message posted successfully!")        
        return redirect('/users/show/profile/' + id)
    
def process_comment(request, id):
        result = Comment.objects.comment_validator(request.POST)
        if type(result) == list:
            for error in result:
                messages.error(request, error)
            return redirect('/users/show/profile/' + id)
        messages.success(request, "Comment posted successfully!")
        print result
        return redirect('/users/show/profile/' + id)