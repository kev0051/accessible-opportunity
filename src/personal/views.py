from django.shortcuts import render
from account.models import Account
from operator import attrgetter
from blog.models import BlogPost
from blog.views import get_blog_queryset
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
#from personal.models import Question

BLOG_POSTS_PER_PAGE = 10

def home_screen_view(request):
	

	context = {}
	# Search
	query = ""
	if request.GET:
		query = request.GET.get('q', '')
		context['query'] = str(query)

	blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)
	accounts = Account.objects.all()
	context['accounts'] = accounts

	# Pagination
	page = request.GET.get('page', 1)
	blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
	try:
		blog_posts = blog_posts_paginator.page(page)
	except PageNotAnInteger:
		blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
	except EmptyPage:
		blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

	context['blog_posts'] = blog_posts
	
	user = request.user
	if user.is_authenticated:
		if user.is_poster:
			return render(request, "personal/posterhome.html", context)
		else:
			return render(request, "personal/applicanthome.html", context)
	else:
		return render(request, "personal/home.html", context)
	
def about_screen_view(request):
    context = {}
    return render(request, "personal/about.html", context)


