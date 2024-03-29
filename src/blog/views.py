from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

from blog.models import BlogPost, JobApplication
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm, ApplyJobForm
from account.models import Account

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.urls import reverse

def create_blog_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		form = CreateBlogPostForm()
		return redirect("home")

	context['form'] = form

	return render(request, "blog/create_blog.html", context)


def detail_blog_view(request, slug):

	context = {}

	blog_post = get_object_or_404(BlogPost, slug=slug)
	context['blog_post'] = blog_post

	return render(request, 'blog/detail_blog.html', context)



def edit_blog_view(request, slug):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	blog_post = get_object_or_404(BlogPost, slug=slug)

	if blog_post.author != user:
		return HttpResponse('You are not the author of that post.')

	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog_post = obj
			return redirect("home")

	form = UpdateBlogPostForm(
			initial = {
					"title": blog_post.title,
					"body": blog_post.body,
					"image": blog_post.image,
			}
		)

	context['form'] = form
	return render(request, 'blog/edit_blog.html', context)

def get_blog_queryset(query=None):
	queryset = []
	queries = query.split(" ") # python install 2019 = [python, install, 2019]
	for q in queries:
		posts = BlogPost.objects.filter(
				Q(title__icontains=q) | 
				Q(body__icontains=q)
			).distinct()

		for post in posts:
			queryset.append(post)

	return list(set(queryset))	

def delete_blog_view(request, slug):
    # Get the blog post object
    blog_post = get_object_or_404(BlogPost, slug=slug)

    # Check if the user is the author of the blog post
    if request.user == blog_post.author:
        # Delete the blog post
        blog_post.delete()
        # Redirect to the blog post list page
        return redirect("home")
    else:
        # Redirect to the blog post detail page
        return redirect('detail_blog_view', slug=slug)

@login_required
@never_cache
def apply_job_view(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        form = ApplyJobForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(job_post=post, applicant=request.user)
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('blog:detail', slug=post.slug)
    else:
        form = ApplyJobForm()

    return render(request, 'blog/apply_job.html', {'form': form, 'post': post})

def evaluate_view(request, pk):
    job_post = get_object_or_404(BlogPost, pk=pk)
    job_applications = JobApplication.objects.filter(job_post=job_post)
    context = {
        'job_post': job_post,
        'job_applications': job_applications,
        'date_applied': [app.date_applied for app in job_applications],
    }
    return render(request, 'blog/view_job_applications.html', context)

def cover_letter_view(request, job_application_id):
    job_application = get_object_or_404(JobApplication, pk=job_application_id)
    context = {
        'job_application': job_application,
    }
    return render(request, 'blog/view_cover_letters.html', context)