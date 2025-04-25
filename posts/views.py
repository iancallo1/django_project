from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment
from .forms import PostForm

def logout_view(request):
    logout(request)
    return redirect('post_list')

class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = 'posts'
    paginate_by = 5  # Show 5 posts per page

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
    success_url = reverse_lazy('post_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('post_list')
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    
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
                author_email=request.user.email,
                content=request.POST['content']
            )
        else:
            # Create comment for anonymous user
            Comment.objects.create(
                post=post,
                author_name=request.POST.get('author_name', 'Anonymous'),
                author_email=request.POST.get('author_email', ''),
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