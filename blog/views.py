from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from blog.models import Blog,Comment,Category,Profile
from django.contrib.auth.models import User
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from blog.forms import BlogForm,UserForm,CommentForm
from django.http import HttpResponseRedirect


# Create your views here.


class UserProfile(DetailView):
    context_object_name = 'blog_user'
    model =User
    template_name = 'blog/user_profile.html'
    def get_absolute_url(self,pk):
        bhatia = User.objects.get(id=self.kwargs['pk'])
        return reverse('blog:user_profile',bhatia)
    def get_context_data(self,*args,**kwargs):
        context = super(UserProfile,self).get_context_data(*args,**kwargs)
        jay = User.objects.get(id=self.kwargs['pk'])
        jayu = User.objects.all()
        new = Blog.objects.filter(author_id=self.kwargs['pk'])
        context['jay']=jay
        context['jayu']=jayu
        context['new']=new
        return context

class UserListView(ListView):
    model = User
    template_name='blog/user_list.html'






def LikeView(request,pk):
    blog = get_object_or_404(Blog,id=request.POST.get('blog_id'))
    liked = False
    if blog.likes_jay.filter(username=request.user.username).exists():

        blog.likes_jay.remove(request.user)
        liked = False
    else:
        blog.likes_jay.add(request.user)
        liked = True


    return HttpResponseRedirect(reverse('blog:detail',args=[str(pk)]))

class CategoryListView(ListView):
    model = Category
    template_name='blog/category_list.html'
    def get_context_data(self,*args,**kwargs):
        context = super(CategoryListView,self).get_context_data(*args,**kwargs)
        tmkoc = User.objects.all()
        context['insert2']=tmkoc
        return context


def CategoryView(request,cats):
    c=Category.objects.get(name=cats)

    cats_list = Blog.objects.filter(category=c)
    dict = Category.objects.all()
    tmkoc = User.objects.all()

    return render(request,'blog/categories.html',{'cats':cats,'cats_list':cats_list,'insert':dict,'insert2':tmkoc})

def index(request):
    dict = Category.objects.all()
    tmkoc = User.objects.all()
    hii = {'insert2':tmkoc}
    hello={'insert':dict}

    return render(request,'blog/index.html',{'insert2':tmkoc,'insert':dict})


class BlogListView(ListView):
    context_object_name = 'blog_list'
    model = Blog
    def get_queryset(self):
        return Blog.objects.filter(published_date__lte=timezone.now()).order_by('-created_date')
    def get_context_data(self,*args,**kwargs):
        context = super(BlogListView,self).get_context_data(*args,**kwargs)
        dict = Category.objects.all()
        tmkoc = User.objects.all()
        context['insert']=dict
        context['insert2']=tmkoc

        return context


class BlogCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    form_class=BlogForm
    model = Blog
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)


class CategoryCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = Category
    success_url = reverse_lazy('index')
    fields = '__all__'


class BlogDetailView(DetailView):
    context_object_name='blog'
    model = Blog
    def get_context_data(self,*args,**kwargs):
        context = super(BlogDetailView,self).get_context_data(*args,**kwargs)
        dict = Category.objects.all()
        tmkoc = User.objects.all()


        stuff = get_object_or_404(Blog,id=self.kwargs['pk'])
        liked = False
        if stuff.likes_jay.filter(username = self.request.user.username).exists():
            liked = True

        total = stuff.countlikes()
        context['total']=total
        context['liked']=liked
        context['insert']=dict
        context['insert2']=tmkoc

        return context

class BlogUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = Blog
    redirect_field_name='blog/blog_detail.html'
    fields = ('title','text')

class CommentCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = Comment
    form_class = CommentForm

    def form_valid(self,form):

        form.instance.blog_id=self.kwargs['pk']
        return super().form_valid(form)



class BlogDeleteView(LoginRequiredMixin,DeleteView):
    login_url = '/login/'
    model =Blog
    success_url = reverse_lazy('blog:list')

class DraftListView(LoginRequiredMixin,ListView):
    context_object_name='draft_list'
    login_url = '/login/'
    model = Blog
    template_name = 'blog/blog_draft_list.html'
    def get_queryset(self):
        return Blog.objects.filter(published_date__isnull=True).order_by('-created_date')
    def get_context_data(self,*args,**kwargs):
        context = super(DraftListView,self).get_context_data(*args,**kwargs)
        dict = Category.objects.all()
        tmkoc = User.objects.all()
        context['insert']=dict
        context['insert2']=tmkoc

        return context



class UserCreateView(CreateView):
    form_class = UserForm

    template_name = 'blog/registration.html'
    success_url = reverse_lazy('login')




class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    template_name = 'blog/registration.html'
    login_url = '/login/'
    fields = ('first_name','last_name','email')

    success_url = reverse_lazy('index')




@login_required
def post_publish(request,pk):
    post = get_object_or_404(Blog,pk=pk)
    post.publish()
    return redirect('blog:detail',pk=pk)

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('blog:detail',pk=comment.blog.pk)

@login_required
def comment_remove(request,pk):
    comment= get_object_or_404(Comment,pk=pk)
    post_pk = comment.blog.pk
    comment.delete()
    return redirect('blog:detail',pk=post_pk)
