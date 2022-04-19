from contextvars import Context
from itertools import count
import json
from multiprocessing import context
import string
from tkinter import NONE
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import Historial, User
from random import randrange
#Librerias para web
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
import sqlite3
from .models import Historial
#from .forms import CambiarPassword
from django.contrib.auth.views import LogoutView 
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Count, Max, Min, Avg
import hashlib as hb
from json import dumps, loads
# from django.contrib.auth.hashers import check_password, is_password_usable
#Condigo de Unity
def create_endpoint(user):
    username = user.username
    status = user.status
    api_create = {"username" : username, "status" : status}
    final = json.dumps(api_create)
    return final
def extractRequest(credentials):
    credentials = credentials.split('&')
    print(credentials)
    user = credentials[0].replace("username=","")
    hshpass = credentials[1].replace("hshpass=","")
    return user, hshpass

#Vistas de la página web
# def index(response):
#     return HttpResponse("<h1>Hello</h1>")
def docs(response):
    return HttpResponse("<h1>Docs site UwU<h1>")
def Comojugar(request):#Ya quedo
    return render(request, 'users/how-to-play.html', {})

def index(request):#Ya quedo
    return render(request, 'users/index.html', {})

def registrarse(request): # Ya quedo y tiene mensajes de errores para cada situación posible
    if request.user.is_authenticated:
        data = Historial.objects.order_by('-Puntos_por_partida') #Ya se muestran los primeros 5 datos
        maxi = Historial.objects.filter(Nombre_usuario="LoboSalvaje").order_by('-Puntos_por_partida') [0:1] #Ya se muestran los primeros 5 datos
        #timer= Historial.objects.all().aggregate('Tiempo_jugado')
        # data = Historial.objects.all()
        total_sum = 0
        # for item in data:
        #     total_sum += item.Tiempo_jugado
        tmer_min = Historial.objects.all().aggregate(Min('Tiempo_jugado'))
        tmer_max = Historial.objects.all().aggregate(Max('Tiempo_jugado'))
        context = {
            'data': data, #Si sirve y funciona bien
            'maxi': maxi,
            'timer':total_sum,
            'timer_min': tmer_min['Tiempo_jugado__min'], 
            'timer_max':tmer_max['Tiempo_jugado__max']
        }
        return render(request, 'users/stadistics-personal.html',context)
    elif request.method == 'POST':
        usuario = request.POST['usuario']
        Contra = request.POST['Contraseña']
        try:
            user_check = User.objects.get(username=usuario)
            user_check.is_superuser = True
            user_check.is_active = True
            user_check.is_staff = True
            user_check.save()
            Confirmacion = authenticate(request, username = usuario, password = Contra)
            if Confirmacion is not None:
                login(request, Confirmacion)
                user_check.is_superuser = False
                #user_check.is_active = False
                user_check.is_staff = False
                user_check.save()
                return redirect('index')
            else:
                messages.error(request, ("La contraseña o el usuario podrían estar incorrectos, ingreselos nuevamente"))
                return redirect('Registrarse')
        except User.DoesNotExist:
            messages.error(request, ("El usuario no existe, pruebe creando uno"))
            return redirect('Registrarse')
    else:
        return render(request, 'users/log-in.html', {})

def ourteam(request): #Esta lista
    return render(request, 'users/our-team.html', {})

def ingresar(request): # Ya quedo
    if request.user.is_authenticated:
        #return render(request, 'users/log-in.html', {})
        data = Historial.objects.order_by('-Puntos_por_partida') #Ya se muestran los primeros 5 datos
        maxi = Historial.objects.filter(Nombre_usuario="LoboSalvaje").order_by('-Puntos_por_partida') [0:1] #Ya se muestran los primeros 5 datos
        #timer= Historial.objects.all().aggregate('Tiempo_jugado')
        # data = Historial.objects.all()
        total_sum = 0
        # for item in data:
        #     total_sum += item.Tiempo_jugado
        tmer_min = Historial.objects.all().aggregate(Min('Tiempo_jugado'))
        tmer_max = Historial.objects.all().aggregate(Max('Tiempo_jugado'))

        context = {
            'data': data, #Si sirve y funciona bien
            'maxi': maxi,
            'timer':total_sum,
            'timer_min': tmer_min['Tiempo_jugado__min'], 
            'timer_max':tmer_max['Tiempo_jugado__max']
        }

        return render(request, 'users/stadistics-personal.html',context)
    elif request.method == 'POST': #CREATE
        usuario = request.POST['Usuario'] #LoboSalvaje
        nombre = request.POST['nombre'] #Nombre real de la persona
        Fecha = request.POST['Fecha'] #Fecha de nacimiento
        Contra = request.POST['Contra'] #Contraseña
        mail = request.POST['mail'] #Email
        Apellido1 = request.POST['Apellido'] #Apellido paterno
        Gender = request.POST['Gender'] #Genero de la persona
        Pais = request.POST['Pais'] #Pais de origen o de estancia
        numero = request.POST['Numero'] #Numero de cel
        User.objects.create_user(username = usuario,email= mail,password=Contra, first_name=nombre, last_name=Apellido1, country=Pais, birthday=Fecha, gender=Gender, phone=numero) #Crea el usuario en la BD de user en django
        return redirect('Estadisticas_personales') #Redirige a la página de estadisticas personales
    else:
        return render(request, 'users/sign-in.html', {})

def estadisticasglobales(request):
    data = Historial.objects.order_by('-Puntos_por_partida')[:5] #Ya se muestran los primeros 5 datos
    maxi = Historial.objects.order_by('-Puntos_por_partida')[0:1] #Ya se muestran los primeros 5 datos
    #timer= Historial.objects.all().aggregate('Tiempo_jugado')
    s = Historial.objects.all()
    total_sum = 0
    for item in s:
        total_sum += item.Tiempo_jugado
    tmer_min = Historial.objects.all().aggregate(Min('Tiempo_jugado'))
    tmer_max = Historial.objects.all().aggregate(Max('Tiempo_jugado'))
    #print(len(data))
    #print(tmer_min['Tiempo_jugado__max']) #Muestar el dato correcto
    context = {
        'data': data,
        'maxi': maxi,
        'timer':total_sum,
        'timer_min': tmer_min['Tiempo_jugado__min'], 
        'timer_max':tmer_max['Tiempo_jugado__max']
    }
    
    return render(request, 'users/stadistics-global.html', context)

def estadisticaspersonales(request): 
    if request.user.is_authenticated:
        
        data = Historial.objects.order_by('-Puntos_por_partida') #Ya se muestran los primeros 5 datos
        maxi = Historial.objects.filter(Nombre_usuario="LoboSalvaje").order_by('-Puntos_por_partida') [0:1] #Ya se muestran los primeros 5 datos
        #timer= Historial.objects.all().aggregate('Tiempo_jugado')
        # data = Historial.objects.all()
        total_sum = 0
        # for item in data:
        #     total_sum += item.Tiempo_jugado
        tmer_min = Historial.objects.all().aggregate(Min('Tiempo_jugado'))
        tmer_max = Historial.objects.all().aggregate(Max('Tiempo_jugado'))

        context = {
            'data': data, #Si sirve y funciona bien
            'maxi': maxi,
            'timer':total_sum,
            'timer_min': tmer_min['Tiempo_jugado__min'], 
            'timer_max':tmer_max['Tiempo_jugado__max']
        }

        return render(request, 'users/stadistics-personal.html',context)
    else:
        return render(request, 'users/index.html', {})

def logout_user(request):#Ya quedo
    logout(request)
    #messages.success(request, ('Logged out'))
    return redirect('index')

def Borrar(request, id):#Ya quedo
    if request.user.is_authenticated and request.method == 'POST':
        #temp_user = User.objects.get(Numero_usuario = id)
        #temp_user.delete()
        #success_url = reverse_lazy('index')
        temp_user2 = User.objects.get(id = id)
        temp_user2.delete()
        return render(request, 'users/index.html',{})
    elif request.user.is_authenticated:
        temp_user = User.objects.get(id = id)
        return render(request, 'users/Borrar.html', {"user":temp_user})
    else:
        return render(request, 'index', {})

def Sobrejuego(request):
    return render(request, 'users/about-game.html', {})

def Cambiarcontra(request, id): #Ya quedo y ya se preparó para toda posible situación
    if request.user.is_authenticated and request.method == 'POST':
        Intento1 = request.POST['Contraseña']
        Intento2 = request.POST['Confirmacion']
        if Intento1 == Intento2:
            u = User.objects.get(id = id)
            u.set_password(Intento1)
            u.save()
            messages.error(request, ("Se cambió la contraseña correctamente, favor de iniciar sesión nuevamente"))
            return render(request, 'users/index.html', {"user":u})
        else:
            temp_user = User.objects.get(id=id)
            messages.error(request, ("Las contraseñas no coinciden"))
            return render(request, 'users/change-pass.html', {"user":temp_user})
        #return render(request, 'PAS/index.html', {})
    elif request.user.is_authenticated:
        temp_user = User.objects.get(id = id)
        #temp_user = User.objects.get(id = id)
        return render(request, 'users/change-pass.html', {"user":temp_user})
    else:
        return render(request, 'index',{})

def editarperfil(request, id):
    if request.user.is_authenticated and request.method != "POST":
        temp_user = User.objects.get(id = id)
        #print(temp_user.Nombre_usuario) #Si selecciona el perfil correcto
        return render(request, 'users/edit-profile.html', {"user":temp_user}) # paso id -> "id": 
    elif request.user.is_authenticated and request.method == 'POST':
        Num=request.POST['uid'] #Recibe 4 en lugar del numero real (5) en este caso, pasa lo mismo en los demás casos de cambio
        usuario_nuevo = request.POST['nombre']
        Fecha_nueva = request.POST['Fecha']
        Apellido_nuevo = request.POST['Apellido']
        Pais_nuevo = request.POST['Pais']
        genero_nuevo = request.POST['Gender']
        tel_nuevo = request.POST['Numero']
        #nuevo_email = request.POST['Apellido2']
        print(Pais_nuevo) #Si lo imprime en la terminal
        user_temp= User.objects.get(id = id) #UPDATE #No siempre selecciona algo # El error esta en esta linea
        print(user_temp)
        user_temp.country = Pais_nuevo
        user_temp.birthday = Fecha_nueva
        user_temp.first_name = usuario_nuevo
        user_temp.last_name = Apellido_nuevo
        user_temp.gender = genero_nuevo.upper()
        user_temp.phone = tel_nuevo
        #user_temp.email = nuevo_email #Checar esto
        #user_temp.Apellido_materno = Apellido_nuevo_2
        user_temp.save()
        return render(request, 'users/index.html', {})
        #us.update(nombre_principal = usuario_nuevo)
        # cur.execute("SELECT * FROM tasks") #Aqui la querry
        # Model.objects.filter(id = 223).update(field1 = 2)
    else:
        return render(request, 'users/index.html', {})

#Codigo de Unity
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
                print("They match. Sending 200 status.\n")
                final = create_endpoint(user)
                return HttpResponse(final, status=200)
            else:
                return HttpResponse(status=406)
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=502)
def apis(response):
    list_of_dicts = list()
    dict_with_list = dict()
    user_list = User.objects.all().values('username', 'country') # Python dict

    print(user_list)

    for object in user_list:
        list_of_dicts.append(object)

    dict_with_list["Users"] = list_of_dicts
    final = json.dumps(dict_with_list)
    return HttpResponse(final, content_type="text/users.json")
class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

#Prueba para dashboard
def apiss(response):
    list_of_dicts = list()
    dict_with_list = dict()
    user_list = Historial.objects.all().values('Nombre_usuario', 'Puntos_por_partida','Fecha_del_juego','Tiempo_jugado') # Python dict

    print(user_list)
    
    for object in user_list:
        list_of_dicts.append(object)

    dict_with_list["Users"] = list_of_dicts
    final = json.dumps(dict_with_list)
    return HttpResponse(final, content_type="text/users.json")

def dashboard(request): #Tiene una estadistica de prueba
    #return HttpResponse(j, content_type="text/json-comment-filtered")
    #Grafica 1
    h_var = 'Points per game'
    v_var = 'Time played'
    data = [[h_var,v_var]]
    # for i in range(0,11):
    #     data.append([randrange(101),randrange(101)])
    h_var_json = dumps(h_var)
    v_var_json = dumps(v_var)
    # datos_json = dumps(data)

    mydb = sqlite3.connect("db.sqlite3")
    cur = mydb.cursor()
    stringSQL = '''SELECT Puntos_por_partida, Tiempo_jugado FROM users_Historial'''
    rows = cur.execute(stringSQL)
    listasalida = []
    for i in rows:
        d = {}
        d['puntos'] = i[0]
        d['tiempo'] = i[1]
        data.append([i[0],i[1]]) #Necesita dos numeros
    datos_json = dumps(data)
    


    #Grafica 2
    h_var2 = '  Country'
    v_var2 = 'Popularity'
    data2 = [[h_var2,v_var2]]
    # for i in range(0,11):
    #     data.append([randrange(101),randrange(101)])
    h_var_json2 = dumps(h_var2)
    v_var_json2 = dumps(v_var2)
    # datos_json = dumps(data)

    mydb2 = sqlite3.connect("db.sqlite3")
    cur2 = mydb2.cursor()
    stringSQL2 = ''' SELECT DISTINCT country FROM users_user'''
    rows2 = cur2.execute(stringSQL2)

    for i in rows2:
        r = {}
        r['paises'] = i[0]

        data2.append([i[0],""]) #Necesita dos numeros #Ver como poner un contador #CHECAR
    datos_json2 = dumps(data2)


    #Grafica 3
    h_var3 = 'ID of the level'
    v_var3 = 'Time of play in minutes'
    data3 = [[h_var3,v_var3]]
    # for i in range(0,11):
    #     data.append([randrange(101),randrange(101)])
    h_var_json3 = dumps(h_var3)
    v_var_json3 = dumps(v_var3)
    # datos_json = dumps(data)

    mydb3 = sqlite3.connect("db.sqlite3")
    cur3 = mydb3.cursor()
    stringSQL3 = ''' SELECT Tiempo_jugado, ID_Canciones_id  FROM users_Historial'''
    rows3 = cur3.execute(stringSQL3)
    for i in rows3:
        rr = {}
        rr['tiempo'] = i[0]
        rr['id'] = i[1]
        data3.append([i[1],i[0]]) #Necesita tres numeros

    datos_json3 = dumps(data3)
    print(datos_json3)#Si pasa bien
    return render(request,'users/Dashboard.html',{'values':datos_json,'h_title':h_var_json,'v_title':v_var_json
                                                 ,'values2':datos_json2,'h_title2':h_var_json2,'v_title2':v_var_json2,
                                                 'values3':datos_json3,'h_title3':h_var_json3,'v_title3':v_var_json3})