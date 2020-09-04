from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
import json

from .models import User, Post, Follower


def index(request):
    if request.method != "GET":
        return HttpResponseBadRequest()

    posts = Post.objects.all()[::-1]
    paginator = Paginator(posts, per_page=10)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)

    return render(request,"network/index.html",{
        'paginator':paginator,
        'page_obj':page_obj,
    })

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

@csrf_exempt
@login_required
def post(request):
    if request.method != "POST":
        return render(request, "network/index.html", {"error1": "POST request required."})
    content = request.POST["postc"]
    if content == "":
        return render(request, "network/index.html", {"error": "POST request required."})
    pos = Post(
        userp = request.user,
        content = content,
    )
    pos.save()
    print(pos)

    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def like_post(request):
    data = json.loads(request.body)
    post_id = data["post_id"]
    post = Post.objects.get(id=post_id)
    #print(post.userl)
    is_liked = False
    if post.is_ulike(request.user):
        post.userl.remove(request.user)
        is_liked = False
    else:
        post.userl.add(request.user)
        is_liked = True

    return JsonResponse({"is_liked": is_liked , "no_likes":post.userl.all().count()}, status=201)

def profile(request, userq):
    usera = User.objects.get(id = userq)
    posts = Post.objects.filter(userp = userq).all()[::-1]
    print(userq)
    username = usera.username
    try:
        follow1 = Follower.objects.filter(following = usera).all()
    except:
        follow1= []
    try:
        follow2 = Follower.objects.get(user = usera).following.all()
    except:
        f = Follower.objects.create(user = usera)
        follow2= f.following.all()
    #print(list(follow1)[0].user)
    print(follow2)
    print(request.user)
    m = False
    for i in list(follow1):
        if i.user == request.user :
            m = True
            break
    return render(request,"network/profile.html",{
        "posts":posts,"usera":usera,"follow1":follow1,"follow2":follow2,"m":m
    })

@csrf_exempt
@login_required
def follow(request):
    data = json.loads(request.body)
    stat = data["stat"]
    usid = data["usid"]
    usera = User.objects.get(id = usid)
    is_follow=True
    foll = Follower.objects.filter(user=request.user)
    m= False
    if len(foll)>0:
        m = True
    if stat:
        if m:
            Follower.objects.get(user=request.user).following.add(usera)
        else:
            fo = Follower.objects.create(user = request.user)
            fo.following.add(usera)
    else:
        fo = Follower.objects.get(user=request.user)
        fo.following.remove(usera)
        is_follow = False
    try:
        Follower.objects.get(user=usera)
    except:
        Follower.objects.create(user=usera)

    fg = Follower.objects.get(user=usera).following.all().count()
    fr = Follower.objects.filter(following__username = usera).all().count()
    print(usera)
    print(Follower.objects.filter(following = usera).all())
    print(User.objects.filter(follow__user = usera).all())
    return JsonResponse({"is_follow": is_follow,"fg":fg,"fr":fr},status=201)

def following(request):
    users = Follower.objects.get(user = request.user).following.all()
    print(users)
    l1 = Post.objects.none()
    for i in users:
        l2 = Post.objects.filter(userp = i).all()
        l1 = l1 | l2
    print(l1)
    posts = l1.order_by("-timestamp").all()
    paginator = Paginator(posts, per_page=10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request,"network/following.html",{
        "page_obj":page_obj,"paginator":paginator
    })
@csrf_exempt
@login_required
def edit(request):
    data = json.loads(request.body)
    post_id = data["post_id"]
    content = data["content"]
    print(content)
    post = Post.objects.get(id = post_id)
    post.content = content
    post.save()
    return JsonResponse({"true":True},status=201)
