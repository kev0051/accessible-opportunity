from django.urls import path
from blog.views import (
	create_blog_view,
	detail_blog_view,
	edit_blog_view,
    delete_blog_view,
    apply_job_view,
    evaluate_view,
    cover_letter_view,
)

app_name = 'blog'

urlpatterns = [
    path('create/', create_blog_view, name="create"),
    path('<slug>/', detail_blog_view, name="detail"),
    path('<slug>/edit/', edit_blog_view, name="edit"),
    path('<slug>/delete/', delete_blog_view, name="delete"),
    path('apply_job_view/<int:pk>', apply_job_view, name="apply"),
    path('evaluate_view/<int:pk>/', evaluate_view, name="evaluate"),
    path('job_application/<int:job_application_id>/cover_letter/', cover_letter_view, name='read'),
 ]