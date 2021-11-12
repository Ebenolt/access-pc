# from django.shortcuts import render
# from django.shortcuts import get_object_or_404
# from django.views.decorators.csrf import csrf_exempt
# from res.utils import *
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import json, hashlib, bcrypt
from datetime import datetime
from api.models import User
from api.models import Client
from api.models import Devis
from api.models import Facture
from api.models import Connexion
from api.models import Message
from api.models import Tarif


class hello(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        if (IsAuthenticated):
            response = json.dumps({
                "success":False,
                "data": "Bad endpoint, missing parameters"
            })
        else:
            response = json.dumps({
                "success":False,
                "data": "Not authenticated"
            })
        return HttpResponse(response, content_type='text/json')

class userView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            response = json.dumps({
                "success":True,
                "data":{
                    "Name":user.name,
                    "Last Name": user.lastname
                }
                })
        except:
            response = json.dumps({
                "success":False,
                "data":"No user with this id"
                })
        return HttpResponse(response, content_type='text/json')

    def post(self, request): 
        try :
            payload = json.loads(request.body)
        except: 
                response = json.dumps({
                "success":False,
                "data": "Missing JSON body / Missformated JSON",
                })
                return HttpResponse(response, content_type='text/json')

        for elem in ['name', 'lastname']:
            if elem not in payload:
                response = json.dumps({
                "success":False,
                "data": f"Missing parameter {elem}",
                })
                return HttpResponse(response, content_type='text/json')

        u_id = 0
        
        users = User.objects.all()
        for user in users:
            if user.id >= u_id:
                print(user.name, user.id)
                u_id = user.id +1
        
        user = User(name = payload['name'], lastname = payload['lastname'], user_id=u_id)
        try:
            user.save()
            response = json.dumps({
                "success":True,
                "data": f"User {payload['name']} {payload['lastname']} saved, ID: {u_id}",
                })
        except:
            response = json.dumps({
                "success": False,
                "data":"Unable to save user"
                })

        return HttpResponse(response, content_type='text/json')

    def delete(self, request, user_id):
        print("\n\n---"+str(user_id)+"---\n\n")
        try :
            user = User.objects.get(user_id=user_id)
        except:
            response = json.dumps({
                "success":False,
                "data": f"User id {user_id} not in database",
                })
            return HttpResponse(response, content_type='text/json')
        try:
            user.delete()
            response = json.dumps({
                "success":True,
                "data": f"User {user_id} deleted",
                })
        except:
            response = json.dumps({
                "success": False,
                "data":f"Unable to delete user {user_id}"
                })
        return HttpResponse(response, content_type='text/json')

class allUsersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            users = User.objects.all()
            response_data = {
                "success" : True,
                "data": []
            }
            for user in users:
                user_data = {
                    "id" : user.user_id,
                    "name": user.name,
                    "lastname": user.lastname
                }
                response_data['data'].append(user_data)
            response = json.dumps(response_data)
        except:
            response = json.dumps({
                "success": False,
                "data":"No user found"
                })
        return HttpResponse(response, content_type='text/json')

    def delete(self, request):
        users = User.objects.all()
        user_count = 0
        for user in users:
            user.delete()
            user_count += 1
        response = json.dumps({
            "success":True,
            "data": f"All users have been flushed ! ({user_count})",
            })
        return HttpResponse(response, content_type='text/json')


class clientView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
            response = json.dumps({
                "success":True,
                "data":{
                    "id": client.id,
                    "Name": client.name,
                    "Last Name": client.lastname,
                    "Mail": client.mail,
                    "Phone": client.phone,
                    "Address": [client.adress1,
                                client.adress2,
                                client.town
                                ],
                    "Pass": client.password,
                    "User level": client.userlevel,
                    "Passchange": client.passchange,
                    "Randomid": client.randomid,
                }
                })
        except:
            response = json.dumps({
                "success":False,
                "data":"No client with this id"
                })
        return HttpResponse(response, content_type='text/json')

    def post(self, request): 
        try :
            payload = json.loads(request.body)
        except: 
                response = json.dumps({
                "success":False,
                "data": "Missing JSON body / Missformated JSON",
                })
                return HttpResponse(response, content_type='text/json')

        missing = []
        for elem in Client.__dict__.keys():
            if elem not in payload and elem not in ['__module__',
                                                    '__str__',
                                                    '__doc__',
                                                    '_meta',
                                                    'DoesNotExist',
                                                    'MultipleObjectsReturned',
                                                    'objects',
                                                    'id',
                                                    'adress2',
                                                    'passchange',
                                                    'userlevel',
                                                    'randomid']:
                missing.append(elem)
            
        if len(missing) > 0:
            response = json.dumps({
                "success":False,
                "data": {
                    "Missing parameters": missing,
                }
            })
            return HttpResponse(response, content_type='text/json')

        client_id = 0
        clients = Client.objects.all()
        for client in clients:
            if client.id >= client_id:
                client_id = client.id +1

        if not('adress2' in payload):
            payload['address2'] = ""

        random = hashlib.md5(datetime.now().strftime("%H:%M:%S").encode()).hexdigest()[:8]
        secure_pass = bcrypt.hashpw(payload['password'].encode(), bcrypt.gensalt())
        print(secure_pass)

        client = Client(id=client_id,
                        name=payload['name'],
                        lastname=payload['lastname'],
                        mail=payload['mail'],
                        phone=payload['phone'],
                        adress1=payload['adress1'],
                        adress2=payload['adress2'],
                        town=payload['town'],
                        password=secure_pass,
                        userlevel=1,
                        passchange=False,
                        randomid=random
        )
        try:
            client.save()
            response = json.dumps({
                "success":True,
                "data": f"Client {client.name} {client.lastname} ({client.mail}) saved, ID: {client_id}",
                })
        except:
            response = json.dumps({
                "success": False,
                "data":"Unable to save client"
                })

        return HttpResponse(response, content_type='text/json')
    

class allClientView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            clients = Client.objects.all()
            response_data = []
            for client in clients:
                response_data.append({
                    "id": client.id,
                    "Name": client.name,
                    "Last Name": client.lastname,
                    "Mail": client.mail,
                    "Phone": client.phone,
                    "Address": [client.adress1,
                                client.adress2,
                                client.town
                                ],
                    "Pass": client.password,
                    "User level": client.userlevel,
                    "Passchange": client.passchange,
                    "Randomid": client.randomid,
                })

            response = json.dumps({
                "success":True,
                "data":response_data,
            })

        except:
            response = json.dumps({
                "success":False,
                "data":"No clients"
                })
        return HttpResponse(response, content_type='text/json')

class connect(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try :
            payload = json.loads(request.body)
        except: 
            response = json.dumps({
                "success":False,
                "data": "Missing JSON body / Missformated JSON",
                })
            return HttpResponse(response, content_type='text/json')

        try:
            print(payload['mail'])
            payload['mail'] = payload['mail'].encode()
            print(payload['mail'])
            client = Client.objects.get(mail=payload['mail'])
        except:
            response = json.dumps({
                "success": False,
                "data": "User not found",
                })
            return HttpResponse(response, content_type='text/json')

        if bcrypt.checkpw(payload['password'], client.password):
            response = json.dumps({
                "success":True,
                "data": "Connected",
            })
        else:
            response = json.dumps({
                "success":False,
                "data": "Please check password",
            })


        return HttpResponse(response, content_type='text/json')



