# from django.shortcuts import render
# from django.shortcuts import get_object_or_404
# from django.views.decorators.csrf import csrf_exempt
# from res.utils import *
from json import encoder
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import json, hashlib, bcrypt
from datetime import datetime
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
        secure_pass = bcrypt.hashpw(payload['password'].encode('utf8'), bcrypt.gensalt())

        client = Client(id=client_id,
                        name=payload['name'],
                        lastname=payload['lastname'],
                        mail=payload['mail'],
                        phone=payload['phone'],
                        adress1=payload['adress1'],
                        adress2=payload['adress2'],
                        town=payload['town'],
                        password=secure_pass.decode('utf8'),
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

    def delete(self, request, client_id):
        try :
            client = Client.objects.get(id=client_id)
        except:
            response = json.dumps({
                "success":False,
                "data": f"Client id {client_id} not in database",
                })
            return HttpResponse(response, content_type='text/json')
        try:
            client.delete()
            response = json.dumps({
                "success":True,
                "data": f"Client {client_id} deleted",
                })
        except:
            response = json.dumps({
                "success": False,
                "data":f"Unable to delete client {client_id}"
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

    def delete(self, request):
        clients = Client.objects.all()
        client_count = 0
        for client in clients:
            client.delete()
            client_count += 1
        response = json.dumps({
            "success":True,
            "data": f"All clients have been flushed ! ({client_count})",
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
            client = Client.objects.get(mail=payload['mail'])
        except:
            response = json.dumps({
                "success": False,
                "data": "User not found",
                })
            return HttpResponse(response, content_type='text/json')

        if bcrypt.checkpw(payload['password'].encode('utf8'), client.password.encode('utf8')):
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



