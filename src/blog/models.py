from django.db import models

# Create your models here.
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

# method for upload location

def upload_location(instance, filename, **kwargs):
	file_path = 'blog/{author_id}/{title}-{filename}'.format(
		author_id = str(instance.author.id), title=str(instance.title), filename = filename
		)
	return file_path

# REFERENCE: https://docs.djangoproject.com/en/4.1/topics/db/models/

class BlogPost(models.Model):
	is_active			= models.BooleanField(default=True) # If true, can be discovered. Posters can set this to false after they create it.
	title				= models.CharField(max_length=200, null=False, blank=False)
	body				= models.CharField(max_length=20000, null=False, blank=False)
	image				= models.ImageField(upload_to=upload_location, null=False, blank=False)
	date_published		= models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated		= models.DateTimeField(auto_now=True, verbose_name="date updated")
	author				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	#date_expired		= models.DateTimeField(auto_now_add=True, verbose_name="date expired") # (SET BY POSTER AT CREATION) If past this date, is_active is set to false
	DIS_TYPE			= (
							('V', 'Visual'),
							('A', 'Auditory'),
							('P', 'Physical'),
							('C', 'Cognitive'),
							('O', 'Other')
						  )
	disability			= models.CharField(default='O', max_length=1, choices=DIS_TYPE)
	slug				= models.SlugField(blank=True, unique=True)

	def __str__(self):
		return self.title

@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)

def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)
