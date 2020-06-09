from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.models import User
# Create your views here.

#dummy data
#loist of dictonary
# posts = [

# {
# 	'author': 'User_1',
# 	'title' : 'Blog Post 1',
# 	'content' : 'First Post Content',
# 	'date_posted': 'June 3, 2020'
# },

# {
# 	'author': 'User_2',
# 	'title' : 'Blog Post 2',
# 	'content' : 'Second Post Content',
# 	'date_posted': 'June 3, 2020'
# }

# ]

#funciton for home page
#this is a function based view
def home(request):             
	#dict
	context ={
	'posts' : Post.objects.all()
	}
	# return HttpResponse('<h1>Blog Home</h1>')
	return render(request, 'blog/home.html',context)

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'   #overwrite the pre-define (<app>/<model>_<viewtype>.html)naming of template in ListView
	context_object_name = 'posts'	   #overwrite the pre-defined context
	ordering = ['-date_posted']	 		#for newer post on top
	paginate_by = 3						#for pagination 2 post per page


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'   #overwrite the pre-define (<app>/<model>_<viewtype>.html)naming of template in ListView
	context_object_name = 'posts'	   #overwrite the pre-defined context
	paginate_by = 2						#for pagination 2 post per page

	def get_queryset(self):
		user = get_object_or_404(User, username = self.kwargs.get('username'))
		return Post.objects.filter(author = user).order_by('-date_posted')


class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):     #LoginRequiredMixin for log in before creating anything
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user    #update author to the current logged in user
		return super().form_valid(form)				#return form_valid method which was gonna run anyway
	


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):     #
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user    #
		return super().form_valid(form)	

	def test_func(self):            #check for user updating his post only
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False	


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post	
	success_url = '/'
	def test_func(self):            #check for user updating his post only
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


#function for about page

def about(request):
	# return HttpResponse('<h1> Blog About</h1>')
	return render(request, 'blog/about.html',{'title': 'About Page'})