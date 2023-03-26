from django.shortcuts import render
from account.models import Account
#from personal.models import Question

# Create your views here.

def home_screen_view(request):
	
	context = {}

	accounts = Account.objects.all()
	context['accounts'] = accounts

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