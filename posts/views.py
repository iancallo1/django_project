from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment
from .forms import PostForm
from django.utils import timezone

def logout_view(request):
    logout(request)
    return redirect('post_list')

class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = 'posts'
    paginate_by = 5  # Default value
    
    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')
    
    def get_paginate_by(self, queryset):
        # Get the per_page value from the request, default to 5 if not specified
        per_page = self.request.GET.get('per_page', 5)
        try:
            per_page = int(per_page)
            # Ensure per_page is one of the allowed values
            if per_page not in [5, 10, 20, 50]:
                per_page = 5
        except (ValueError, TypeError):
            per_page = 5
        return per_page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the current per_page value to the context
        context['per_page'] = self.get_paginate_by(None)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    
    def get_success_url(self):
        return reverse_lazy('post_list') + '?success=create'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.created_at = timezone.now()
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    
    def get_success_url(self):
        return reverse_lazy('post_list') + '?success=update'
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('post_list') + '?success=delete'
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            # Create comment with user information
            Comment.objects.create(
                post=post,
                author=request.user,
                author_name=request.user.username,
                author_email_hash=hash_email(request.user.email),
                content=request.POST['content']
            )
        else:
            # Create comment for anonymous user
            email = request.POST.get('author_email', '')
            Comment.objects.create(
                post=post,
                author_name=request.POST.get('author_name', 'Anonymous'),
                author_email_hash=hash_email(email) if email else '',
                content=request.POST['content']
            )
        return redirect('post_detail', pk=post_id)
    return redirect('post_detail', pk=post_id)

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'posts/signup.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in after signing up
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response