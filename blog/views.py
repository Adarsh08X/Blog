from urllib import response
from xml.etree.ElementTree import Comment
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)
# Create your views here.

def home(request):

    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model  = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    
    paginate_by = 5


class UserPostListView(ListView):
    model  = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-date_posted']
    def get_queryset(self):
        user =  get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user)
    
    

def get_post(request,pk):
    # post_id = request.id
    logger.info('$$$$$$$$$$$$$$$$$$$')
    post = Post.objects.get(id = pk)
    comments = Comment.objects.get(post = post)
    print(comments)
    context = {
        'post': post,
        'comment': comments
    }
    
    return render(request, 'blog/post_detail.html',context=context)

# class PostDetailView(DetailView):
#     model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model  = Post
    fields = ['title', 'content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model  = Post
    fields = ['title', 'content']

    def form_valid(self,form):
        form.instance.author == self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model  = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html')

def likes(request,pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))