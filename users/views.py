import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import User


def extractRequest(credentials):
    credentials = credentials.split('&')
    print(credentials)
    user = credentials[0].replace("username=","")
    hshpass = credentials[1].replace("hshpass=","")
    return user, hshpass


def index(response):
    return HttpResponse("<h1>Hello</h1>")


def docs(response):
    return HttpResponse("<h1>Docs site UwU<h1>")


@csrf_exempt
def post_or_get(request):
    print("GETING HERE FIRST")
    if request.method == 'POST':
        # Compare the sent data with the database data
        print("\n--------------------------------------------------")
        print("Request.body that arrived: ")
        print(type(request.body))
        print(request.body)

        print("\n--------------------------------------------------")
        print("Request decoded: ")
        request = request.body.decode('utf8').replace("'", '"')

        user, hshpass = extractRequest(request) # split request and get user and password to check in db
        USER_OBJ = User.objects.filter(username=user)

        if USER_OBJ.exists():
            for user in USER_OBJ:
                DB_HASHED_PASSWORD = user.check_unity # Instead of contrasena, hashed contrasena
                print("\nData in db: ")
                print(DB_HASHED_PASSWORD)

            if hshpass == DB_HASHED_PASSWORD:
                print("They match. Sending 200 status.")
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=406)
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=502)


def apis(response):
    list_of_dicts = list()
    user_list = User.objects.all().values('username', 'is_active')

    for object in user_list:
        list_of_dicts.append(object)
    final = json.dumps(list_of_dicts)
    return HttpResponse(final, content_type="text/users.json")


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
