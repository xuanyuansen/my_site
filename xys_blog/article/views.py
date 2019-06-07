from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
import markdown
from django.contrib.auth.decorators import login_required


# Create your views here.
def article_list(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        articles = BlogArticle.objects.filter(author_id=user_id)
        # articles = BlogArticle.objects.all()
        context = {'articles': articles}
        return render(request, 'article/list.html', context)
    else:
        articles = BlogArticle.objects.all()
        context = {'articles': articles}
        return render(request, 'article/list.html', context)


# login_required(login_url='/userprofile/login/')
def article_detail(request, article_id):
    article = BlogArticle.objects.get(id=article_id)
    # remark = Remark.objects.filter(aid=id)
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ])

    # remark = Remark.objects.all()
    # articleReply = ArticleReply.objects.all()
    context = {
        'article': article,
        # 'remark': remark,
        # 'articleReply': articleReply,
    }
    return render(request, 'article/detail.html', context)


@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == "POST":
        article_post_form = BlogForm(data=request.POST)
        if article_post_form.is_valid():
            print(request.POST)
            new_article = article_post_form.save(commit=False)
            user_id = request.user.id
            new_article.author = User.objects.get(id=user_id)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = BlogForm()
        context = {'article_post_form': article_post_form}
        return render(request, 'article/create.html', context)


@login_required(login_url='/userprofile/login/')
def article_delete(request, article_id):
    article = BlogArticle.objects.get(id=article_id)
    article.delete()
    return redirect("article:article_list")


@login_required(login_url='/userprofile/login/')
def article_update(request, article_id):
    article = BlogArticle.objects.get(id=article_id)
    if request.method == 'POST':
        article_post_form = BlogForm(data=request.POST)

        if article_post_form .is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()

            return redirect("article:article_detail", id=article_id)
        else:
            return HttpResponse("内容有误，请重新填写")

    else:
        article_post_form = BlogForm()
        context = {'article': article, 'article_post_form': article_post_form}
        return render(request, 'article/update.html', context)


def article_own(request):
    articles = BlogArticle.objects.filter(author_id=request.user.id)
    context = {'articles': articles}
    return render(request, 'article/own.html', context)


def searchtag(request, category):
    tag = category
    articles = BlogArticle.objects.filter(category=category)

    context = {
        'articles':articles,
    }
    return render(request,'article/tag.html',context)
