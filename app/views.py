from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# GET 

def index(request):
    return render(request, 'index.html')

def success(request):
    context = {
        'all_comments': CommentPost.objects.all()
    }
    return render(request, 'comments.html', context)

def edit_account(request):
    return render(request, 'edit_account.html')

def user_comments(request, user_id):
    # get the user
    context = {
        'user': User.objects.get(id = user_id)
    }
    # render the user's page
    return render(request, 'user_comments.html', context)

def myaccount(request, user_id):
    # get the user
    context = {
        'user': User.objects.get(id = user_id)
    }
    # render the user's edit page
    return render(request, 'edit_account.html', context)

def about(request):
    return render(request, 'about.html')

# POST 

def register(request):
    if request.method == 'POST':
        # validate
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for e in errors:
                messages.error(request, errors[e])
            return redirect('/')
        # ck if user exists
        user_exist_chk = User.objects.filter(email = request.POST['email'])
        if len(user_exist_chk) > 0:
            messages.error(request, 'Email address already in use')
            return redirect('/')
        # create user
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt(4)).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw,
        )
        # establish session data
        request.session['user_id'] = new_user.id
        request.session['first_name'] = new_user.first_name
        request.session['last_name'] = new_user.last_name
        request.session['email'] = new_user.email
    return redirect('/')

def login(request):
    if request.method == 'GET':
        return redirect('/')
    # authenticate email/password
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    # identify user
    user = User.objects.get(email = request.POST['email'])
    # establish session data
    request.session['user_id'] = user.id
    request.session['first_name'] = user.first_name
    request.session['last_name'] = user.last_name
    request.session['email'] = user.email
    return redirect('/success')

def logout(request):
    del request.session['user_id']
    del request.session['first_name']
    del request.session['last_name']
    del request.session['email']
    return redirect('/')

def create_comment(request):
    # validate
    if request.method == 'POST':
        error = CommentPost.objects.comment_validator(request.POST)
        if error:
            for e in error:
                messages.error(request, error[e])
            return redirect('/success')
        # create comment
        CommentPost.objects.create(
            comment = request.POST['comment'],
            poster = User.objects.get(id = request.session['user_id']),
        )
        return redirect('/success')
    return redirect('/')

def back(request):
    return redirect('/success')

def update(request):
    # validate
    if request.method == 'POST':
        # validate
        errors = User.objects.update_validator(request.POST)
        if len(errors) > 0:
            for e in errors:
                messages.error(request, errors[e])
            return redirect(f"/myaccount/{ request.session['user_id'] }")
        # ck if user exists
        user_exist_chk = User.objects.filter(email = request.POST['email'])
        if len(user_exist_chk) > 0:
            messages.error(request, 'Email address already in use')
            return redirect(f"/myaccount/{ request.session['user_id'] }")
        # update user
        updated_user = User.objects.get(id = request.session['user_id'])
        updated_user.first_name = request.POST['first_name']
        updated_user.last_name = request.POST['last_name']
        updated_user.email = request.POST['email']
        updated_user.save()
        # establish session data
        request.session['user_id'] = updated_user.id
        request.session['first_name'] = updated_user.first_name
        request.session['last_name'] = updated_user.last_name
        request.session['email'] = updated_user.email
        return redirect('/success')
    return redirect('/')

def delete_comment(request, comment_id):
    CommentPost.objects.get(id = comment_id).delete()
    return redirect('/success')

def add_like(request, comment_id):
    liked_comment = CommentPost.objects.get(id = comment_id)
    user_liking = User.objects.get(id = request.session['user_id'])
    liked_comment.user_likes.add(user_liking)
    return redirect('/success')