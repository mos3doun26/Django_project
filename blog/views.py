from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

def home(request):
    context={
        "posts":Post.objects.all()
    }
    return render(request, "blog/home.html", context)

class PostListview(ListView):
    model = Post
    template_name = "blog/home.html/" #defualt blog/post_list.html, pattern: <app>/<Model>_<view_type>/
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5

class UserPostListview(ListView):
    model = Post
    template_name = "blog/user_posts.html/" #defualt blog/post_list.html, pattern: <app>/<Model>_<view_type>/
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")

class PostDetailview(DetailView):
    model = Post
    # template_name = "blog/post_detail.html"

class PostCreateview(LoginRequiredMixin, CreateView):
    model = Post
    # template_name = "blog/post_create.html" # instead of make asign template_name manualy, createview predict the tamplate nam as <app>/<model>_form.html
    # for that we will create the html file that resposible for creation new post with this name, here: ind dir(blog) file will be post_form.html
    fields=["title", "content"]
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateview(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields=["title", "content"]
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().author == self.request.user
    # write func in another way.
    # def test_func(self):
    #     post = self.get_object()
    #     return True if post.author == self.request.user else False
class PostDeleteview(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # template_name = "blog/post_delete.html"
    success_url = "/"
    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)

    def test_func(self):
        return self.get_object().author == self.request.user

def about(request):
    return render(request, "blog/about.html",{"title":"about"})