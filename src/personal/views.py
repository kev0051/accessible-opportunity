from django.shortcuts import render
from account.models import Account
#from personal.models import Question

# Create your views here.

def home_screen_view(request):
	
	context = {}

	accounts = Account.objects.all()
	context['accounts'] = accounts
	#context['some_string'] = "this is some string that I'm passing to the view"
	#context['some_number'] = 6300

	#list_of_values = []
	#list_of_values.append("first entry")
	#list_of_values.append("second entry")
	#list_of_values.append("third entry")
	#list_of_values.append("fourth entry")
	#context['list_of_values'] = list_of_values

	#questions = Question.objects.all()
	#context['questions'] = questions

	user = request.user
	if user.is_authenticated:
		if user.is_poster:
			return render(request, "personal/posterhome.html", context)
		else:
			return render(request, "personal/applicanthome.html", context)
	else:
		return render(request, "personal/home.html", context)
	
