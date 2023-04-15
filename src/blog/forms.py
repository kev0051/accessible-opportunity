from django import forms

from blog.models import BlogPost, JobApplication


class CreateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image', 'disability']


class UpdateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image']

	def save(self, commit=True):
		blog_post = self.instance
		blog_post.title = self.cleaned_data['title']
		blog_post.body = self.cleaned_data['body']

		if self.cleaned_data['image']:
			blog_post.image = self.cleaned_data['image']

		if commit:
			blog_post.save()
		return blog_post

class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume', 'cover_letter']

    def save(self, job_post, applicant):
        application = super().save(commit=False)
        application.job_post = job_post
        application.applicant = applicant
        application.save()
        return application