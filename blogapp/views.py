from django.shortcuts import render,redirect
from django.views.generic import ListView,DeleteView,DetailView,CreateView,UpdateView,TemplateView,FormView
from .models import Post,Comment
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy,reverse
from .forms import PostForm,EditForm,CommentForm,AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin # new
)
from rest_framework import generics
from django.contrib import messages 
from .serializers import PostSerializer
from .forms import UserForm,UserProfileInfoForm
from django.views.generic.edit import FormMixin
@login_required(login_url='login')
def LikeView(request,pk):

    post = get_object_or_404(Post,id=request.POST.get('post_id'))
    liked=False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked=True


    return HttpResponseRedirect(reverse('post_detail',args=[str(pk)]))


class BlogListView(ListView):

    model = Post
    template_name = 'home.html'
    ordering = ['-pk']



class BlogDetailView(FormMixin,DetailView): # new
    model = Post
    template_name = 'post_detail.html'
    form_class=CommentForm


    def get_context_data(self,*args,**kwargs):
        context = super(BlogDetailView, self).get_context_data(*args,**kwargs)
        stuff = get_object_or_404(Post,id=self.kwargs['pk'])
        liked=False
        if stuff.likes.filter(id=self.request.user.id).exists():

            liked=True
        total_likes=stuff.like_count()
        context["total_likes"]=total_likes
        context["liked"]=liked
        context["others"]=Post.objects.all()
        return context
    def form_valid(self, form): # new
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    def post(self,request,**kwargs):

        if request.method == 'POST':
            print("herer we go   zde")
            form=CommentForm(request.POST)
            print(form.is_valid)
            
            print("herer we go")
            text = request.POST.get('comment')
            print(text)
            author = self.request.user
            post_id = self.kwargs['pk']
        #     com = form.cleaned_data['text']
        #     author = self.request.user
        #     post_id = self.kwargs['pk']
        #     print(com)
            save=Comment(text=text,author=author,post_id=post_id)
            save.save()
        # ordering = ['-pub_date']
        return HttpResponseRedirect(reverse("post_detail", kwargs={'pk':self.kwargs['pk']}))
    def get_success_url(self, **kwargs):
    # obj = form.instance or self.object
        return reverse("post_detail", kwargs={'pk':self.kwargs['pk']})

class BlogCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name='post_new.html'
    login_url = 'login'


    form_class=PostForm
    def form_valid(self, form): # new
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView): # new
    model = Post
    template_name = 'post_edit.html'
    login_url = 'login'

    form_class=EditForm
    def test_func(self): # new
        obj = self.get_object()
        return obj.author == self.request.user

class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')
class CommentCreateView(LoginRequiredMixin,CreateView):
    model = Comment
    template_name='post_comment.html'
    login_url = 'login'


    form_class=CommentForm

    def form_valid(self, form): # new
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    def get_success_url(self, **kwargs):
    # obj = form.instance or self.object
        return reverse("post_detail", kwargs={'pk':self.kwargs['pk']})
def register(request):
    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True
            return HttpResponseRedirect(reverse('home') )
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'register.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           })

class ListPost(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
class DetailPost(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

def search(request):
    query = request.GET['query']
    
    allpost = Post.objects.all()
    
    searchpost = Post.objects.filter(title__icontains=query)
    print(searchpost)
    params = {'searchpost':searchpost}
    return render(request,'search.html',params)


def user_login(request):
    if request.method == 'POST':
        print("hsdifdfaDSNN jdsf vcxz.........")
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                
                
                
                
                return redirect(reverse('home'))
        else:
            messages.error(request,'username or password not correct')
            print(messages)
            return redirect(reverse('login'))
        
                
    else:
        form = AuthenticationForm()
        context = {'form': form}
    return render(request,'registration/login.html',context)
