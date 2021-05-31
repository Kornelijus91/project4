from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator
import json

from .models import User, Post, Following, Like, UserInfo


def index(request):
    if request.method == "POST":
        current_user = request.user
        formInput = NewPostForm(request.POST)
        if formInput.is_valid():
            if formInput.cleaned_data["post_content"]:
                post = formInput.cleaned_data["post_content"]
        new_post = Post(
            user = current_user,
            body = post
        )
        new_post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        get_posts = Post.objects.all()
        page_obj = Paginator(get_posts, 10)
        page_number = request.GET.get('page')
        posts = page_obj.get_page(page_number)
        return render(request, "network/index.html", {
            "form": NewPostForm(),
            "posts": posts
        })

def profile(request, username):
    # get_user = User.objects.all().filter(username=username).first()
    # get_user_info = UserInfo.objects.get(user=get_user)
    user = User.objects.get(username=username)
    # print("USER ==> ", user)
    user_info = UserInfo.objects.filter(user=user).first()
    if user_info:
        follows = user_info.following
        followers = user_info.followers
    else:
        follows = 0
        followers = 0
    user_posts = Post.objects.all().filter(user=user)
    #print("USER INFO ==> ", user_info)

    return render(request, "network/profile.html", {
        "username": user,
        "posterid": user.id,
        "following": follows,
        "followers": followers,
        "posts": user_posts
    })

@csrf_exempt
def follow(request):
    if request.method == "POST":
        current_user = request.user
        userid = json.loads(request.body)
        follow_user = User.objects.get(id=userid['userid'])
        isfollowing = Following.objects.all().filter(user=current_user, following=follow_user).first()
        if not isfollowing:
            follow = Following(
                user = current_user,
                following = follow_user
            )
            follow.save()
        else:
            isfollowing.delete()
        follower_count = Following.objects.all().filter(following=follow_user).count()
        update_follower_count = UserInfo.objects.filter(user=follow_user).first()
        if update_follower_count:
            update_follower_count.followers = follower_count
            update_follower_count.save()
            #print(update_follower_count)
        else:
            new_follower_count = UserInfo(
                user=follow_user,
                followers=follower_count
            )
            new_follower_count.save()
        following_count = Following.objects.all().filter(user=current_user).count()
        update_following_count = UserInfo.objects.filter(user=current_user).first()
        if update_following_count:
            update_following_count.following = following_count
            update_following_count.save()
        else:
            new_following_count = UserInfo(
                user=current_user,
                followers=following_count
            )
            new_following_count.save()
        #if isfollowing:
            #return JsonResponse({"buttontext": "Follow"}, status=201)
        #else:
            #return JsonResponse({"buttontext": "Unfollow"}, status=201)
        return HttpResponseRedirect(reverse("profile", args=(follow_user.username,)))

@login_required
def following(request):
    get_following = Following.objects.all().filter(user=request.user)
    following_list = []
    for item in get_following:
        following_list.append(item.following)
    get_posts = Post.objects.all().filter(user__in=following_list)
    return render(request, "network/following.html", {
        "posts": get_posts
    })

@csrf_exempt
def isfollowing(request):
    if request.method == "POST":
        userid = json.loads(request.body)
        follow_user = User.objects.get(id=userid['userid'])
        isfollowing = Following.objects.all().filter(user=request.user, following=follow_user).first()
        if isfollowing:
            return JsonResponse({"buttontext": "Unfollow"}, status=201)
        else:
            return JsonResponse({"buttontext": "Follow"}, status=201)


@csrf_exempt
def updatefollowcount(request):
    if request.method == "POST":
        userid = json.loads(request.body)
        user = User.objects.get(id=userid['userid'])
        follow_user = UserInfo.objects.all().filter(user=user).first()
        return JsonResponse({
            "followers": follow_user.followers,
            "following": follow_user.following
        }, status=201)

@csrf_exempt
def editpost(request):
    if request.method == "POST":
        edit_data = json.loads(request.body)
        post_owner_id = edit_data['userid']
        post_id = edit_data['postid']
        new_post_text = edit_data['posttext']
        if int(post_owner_id) == request.user.id:
            user = User.objects.get(id=request.user.id)
            post = Post.objects.get(id=post_id, user=user)
            post.body = new_post_text
            post.save()
            return JsonResponse({
                "message": "SUCCES!!!!!"
                }, status=201)
    else:
        return JsonResponse(status=401)

@csrf_exempt
def isliked(request):
    if request.method == "POST":
        post_id = json.loads(request.body)["postid"]
        post = Post.objects.get(id=post_id)
        is_liked = Like.objects.all().filter(user=request.user, liked=post).first()
        # print(is_liked)
        if is_liked:
            liked = True
        else:
            liked = False
        return JsonResponse({
            "liked": liked
        }, status=201)
    else:
        return JsonResponse(status=401)

@csrf_exempt
def like(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post = Post.objects.get(id=data["postid"])
        like_count = post.likes
        isliked = Like.objects.all().filter(user=request.user, liked=post).first()
        if not isliked:
            like = Like(
                user=request.user,
                liked=post
            )
            like.save()
            post.likes = like_count + 1
            post.save()
            return JsonResponse({"liked": 1}, status=201)
        else:
            unlike = Like.objects.get(user=request.user, liked=post)
            unlike.delete()
            post.likes = like_count - 1
            post.save()
            return JsonResponse({"liked": 0}, status=201)  
    else:
        return JsonResponse(status=401)

@csrf_exempt
def getlikecount(request):
    if request.method == "POST":
        postid = json.loads(request.body)["postid"]
        post = Post.objects.get(id=postid)
        return JsonResponse({"likecount": post.likes}, status=201)
    else:
        return JsonResponse(status=401)

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

class NewPostForm(forms.Form):
    post_content = forms.CharField(label="New post:", widget=forms.Textarea)