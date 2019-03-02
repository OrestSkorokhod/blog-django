from django.shortcuts import render, redirect
# from django.http import HttpResponse
# Create your views here.
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .models import Post, Tag, Comment
from .utils import *
from .forms import TagForm, PostForm, CommentForm

from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from django.db.models import Q



def posts_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query)| Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()


    paginator = Paginator(posts, 3)

    comments = Comment.objects.all()

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    for post in page:
        post.count_of_comments = 0
        for comment in comments:
            if comment.post == post:
                post.count_of_comments += 1

    is_paginated = page.has_other_pages()

    if page.has_previous():
        previous_url = '?page={}'.format(page.previous_page_number())
    else:
        previous_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
    'page_object': page,
    'is_paginated': is_paginated,
    'next_url': next_url,
    'prev_url': previous_url,

    }


    return render(request, 'blog/index.html', context=context)

class CommentCreate(LoginRequiredMixin, View):
    form_model = CommentForm
    template = 'blog/comment_create_form.html'
    raise_exception = True
    model = Comment

    def get(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        bound_form = self.form_model()
        return render(request, self.template, context={'form': bound_form, Post.__name__.lower(): post})

    def post(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        bound_form = self.form_model(request.POST)
        if bound_form.is_valid():
            comment = Comment()
            comment.post = post
            comment.author = auth.get_user(request)
            comment.description = bound_form.cleaned_data['description']
            comment.save()
            return redirect(post.get_absolute_url())
            # bound_form.fields['post'] = post
            # new_obj = bound_form.save()
            # return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, Post.__name__.lower(): post})



class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(PermTest, LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})

class TagDetail(ObjectDetailMixin, View):
        model = Tag
        template = 'blog/tag_detail.html'

class TagCreate(PermTest, LoginRequiredMixin,ObjectCreateMixin, View):
    form_model = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True

class PostUpdate(PermTest, LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True

class TagUpdate(PermTest, LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True


class TagDelete(PermTest, LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True

class PostDelete(PermTest, LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True
