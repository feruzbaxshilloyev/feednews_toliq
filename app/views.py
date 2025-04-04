from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.http import HttpResponseForbidden

from .forms import ContactMessageForm, RegisterForm, ProfileForm
from .models import *
from django.shortcuts import render, redirect
import datetime
from .models import Comment
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import News


def date_view():
    return datetime.datetime.today()


def index(request):
    ctg = Category.objects.all()
    ctg1 = Category.objects.filter(is_active=True)
    news = News.objects.all().order_by('-created_at')
    popular = News.objects.all().order_by('-views')
    sps = Sponsors.objects.all()
    ctx = {
        'ctg': ctg,
        'ctg1': ctg1,
        'news': news,
        'popular': popular,
        'sps': sps,
        'date': date_view(),
    }
    return render(request, 'index.html', ctx)


def about(request):
    return render(request, 'about.html')


def category(request, pk):
    ctg = Category.objects.get(id=pk)
    ctg1 = Category.objects.filter(is_active=True)
    news = News.objects.filter(category__name=ctg.name).order_by('-created_at')
    idd = ctg.id
    ctx = {
        'ctg': ctg,
        'news': news,
        'ctg1': ctg1,
        'date': date_view(),
        'idd': idd,
    }
    return render(request, 'category.html', ctx)


def news_detail(request, pk):
    news = News.objects.get(id=pk)
    newss = News.objects.all().order_by('-created_at')
    news.views += 1
    news.save()
    ctg = Category.objects.all()
    ctg1 = Category.objects.filter(is_active=True)
    news_ctg = News.objects.filter(category=news.category).order_by('-id')[:4]
    sps = Sponsors.objects.all()
    popular = News.objects.all().order_by('-views')
    comments = Comment.objects.filter(news__id=pk).order_by('-created_at')
    ctx = {
        'news': news,
        'ctg': ctg,
        'ctg1': ctg1,
        'news_ctg': news_ctg,
        'date': date_view(),
        'newss': newss,
        'popular': popular,
        'sps': sps,
        'pk': pk,
        'com': comments,
    }
    return render(request, 'single_page.html', ctx)


def contact1(request):
    news = News.objects.all().order_by('-created_at')
    popular = News.objects.all().order_by('-views')
    ctg = Category.objects.all().order_by('-id')
    ctg1 = Category.objects.filter(is_active=True)
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = ContactMessageForm()
    ctx = {
        'ctg': ctg,
        'ctg1': ctg1,
        'news': news,
        'popular': popular,
        'date': date_view(),
        'form': form,
    }

    return render(request, "contact.html", ctx)


def comment(request, pk):
    news = News.objects.get(id=pk)
    coms = Comment.objects.all().order_by('-created_at')
    comments = Comment.objects.filter(news__id=news.id).order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comm = form.save(commit=False)
            comm.author = request.user
            comm.news = news
            comm.save()
            return redirect('comment', pk=pk)
    else:
        form = CommentForm()

    ctx = {
        'form': form,
        'comments': comments,
        'news': news,
        'coms': coms,
        'pk': pk,
    }
    return render(request, 'comment.html', ctx)


@login_required
def like_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.user not in news.liked_users.all() and request.user in news.disliked_users.all():
        news.dislike -= 1
        news.disliked_users.remove(request.user)
        news.save()
        news.like += 1
        news.liked_users.add(request.user)
        news.save()
        return redirect('n_d', pk=pk)

    elif request.user not in news.liked_users.all():
        news.like += 1
        news.liked_users.add(request.user)
        news.save()
        return redirect('n_d', pk=pk)
    else:
        news.like -= 1
        news.liked_users.remove(request.user)
        news.save()
        return redirect('n_d', pk=pk)


@login_required
def dislike_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.user not in news.disliked_users.all() and request.user in news.liked_users.all():
        news.like -= 1
        news.liked_users.remove(request.user)
        news.save()
        news.dislike += 1
        news.disliked_users.add(request.user)
        news.save()
        return redirect('n_d', pk=pk)

    elif request.user not in news.disliked_users.all():
        news.dislike += 1
        news.disliked_users.add(request.user)
        news.save()
        return redirect('n_d', pk=pk)

    else:
        news.dislike -= 1
        news.disliked_users.remove(request.user)
        news.save()
        return redirect('n_d', pk=pk)


def rate_like(request, pk):
    news = get_object_or_404(News, pk=pk)
    newss = News.objects.all().order_by('-created_at')
    news.views += 1
    news.save()
    ctg = Category.objects.all()
    ctg1 = Category.objects.filter(is_active=True)
    news_ctg = News.objects.filter(category=news.category).order_by('-id')[:4]
    sps = Sponsors.objects.all()
    popular = News.objects.all().order_by('-views')
    comments = Comment.objects.filter(news__id=pk).order_by('-created_at')
    ctx = {
        'news': news,
        'ctg': ctg,
        'ctg1': ctg1,
        'news_ctg': news_ctg,
        'date': date_view(),
        'newss': newss,
        'popular': popular,
        'sps': sps,
        'pk': pk,
        'com': comments,
        'lll': like_news(request, pk),
    }
    return render(request, 'single_page.html', ctx)


def rate_dis(request, pk):
    news = get_object_or_404(News, pk=pk)
    newss = News.objects.all().order_by('-created_at')
    news.views += 1
    news.save()
    ctg = Category.objects.all()
    ctg1 = Category.objects.filter(is_active=True)
    news_ctg = News.objects.filter(category=news.category).order_by('-id')[:4]
    sps = Sponsors.objects.all()
    popular = News.objects.all().order_by('-views')
    comments = Comment.objects.filter(news__id=pk).order_by('-created_at')
    ctx = {
        'news': news,
        'ctg': ctg,
        'ctg1': ctg1,
        'news_ctg': news_ctg,
        'date': date_view(),
        'newss': newss,
        'popular': popular,
        'sps': sps,
        'pk': pk,
        'com': comments,
        'ddd': dislike_news(request, pk),
    }

    return render(request, 'single_page.html', ctx)


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Muvaffaqiyatli ro‘yxatdan o‘tdingiz!")
            return redirect('index')
        else:
            messages.error(request, "Iltimos, xatolarni to‘g‘rilang!")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Yaroqsiz login")
            return redirect('login')

    return render(request, "login.html")


# Logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        print(form.errors)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form})


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('n_d', pk=comment.news.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'com_edit.html', {'form': form})


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)

    comment.delete()
    return redirect('n_d', pk=comment.news.id)


@login_required
def user_com(request):
    comments = Comment.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'user_com.html', {'comments': comments})


@login_required
def com_d(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    return redirect('n_d', pk=comment.news.id)
