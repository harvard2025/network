from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Post, Follow, Like
import json
from django.http import JsonResponse
from django.views.decorators.cache import cache_page



@cache_page(60 * 15)  # الكاش لمدة 15 دقيقة

def remove_Like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.filter(user=user, post=post)
    like.delete()
    return JsonResponse({'message':'Like add'})


def add_Like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    newLike = Like(user=user, post=post)
    newLike.save()
    return JsonResponse({'message':'Like add'})


def index(request):
    allPosts = Post.objects.all().order_by('id').reverse()

    # Pagination
    paginater = Paginator(allPosts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginater.get_page(page_number)


    allLikes = Like.objects.all()
    

    whoYouLiked = []
    try:
        for like in allLikes :
            if like.user.id == request.user.id:
                whoYouLiked.append(like.post.id)

    except:
        whoYouLiked = []


    
    return render(request, "network/index.html", {
        'allPosts': allPosts,
        'post_of_the_page': posts_of_the_page,
        'whoYouLiked': whoYouLiked,
        

    })

def newPost(request):
    if request.method == 'POST':
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse(index))

def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    allPosts = Post.objects.filter(user=user).order_by('id').reverse()

    follwers = Follow.objects.filter(user_follower=user)
    follwing = Follow.objects.filter(user=user)

    try:
        checkFollow = follwers.filter(user=User.objects.get(pk=request.user.id))
        if len(checkFollow) != 0:
            isFollwing = True
        else:
            isFollwing= False
    except:
        isFollwing = False
    # Pagination
    paginater = Paginator(allPosts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginater.get_page(page_number)

    return render(request, "network/profile.html", {
        'allPosts': allPosts,
        'post_of_the_page': posts_of_the_page,
        'username':user.username,
        'follwing': follwing,
        'follwers': follwers,
        'isFollwing': isFollwing,
        'user_profile':user,

    })
    





def follow(request):
    userFollow = request.POST['userFollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username=userFollow)
    f = Follow(user=currentUser, user_follower=userfollowData)
    f.save()
    user_id = userfollowData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':user_id}))
    
def unfollow(request):
    userFollow = request.POST['userFollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username=userFollow)
    f = Follow.objects.filter(user=currentUser, user_follower=userfollowData)
    f.delete()
    user_id = userfollowData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':user_id}))





def Following(request):
    CurrentUser = User.objects.get(pk=request.user.id)
    followingPeople = Follow.objects.filter(user=CurrentUser)
    allPosts = Post.objects.all().order_by('id').reverse()
    followingPosts = []


    for post in allPosts:
        for person in followingPeople:
            if person.user_follower == post.user:
                followingPosts.append(post)

    paginater = Paginator(followingPosts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginater.get_page(page_number)

    return render(request, "network/following.html", {
        'post_of_the_page': posts_of_the_page,

    })


def edit(request, post_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.content = data['content']
        edit_post.save()
        return JsonResponse({'message':'Change succesful', 'data': data['content']})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

