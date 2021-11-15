# from django.shortcuts import render
# from django.shortcuts import get_object_or_404
# from django.views.decorators.csrf import csrf_exempt
from json import encoder
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import json
import hashlib
import bcrypt
from datetime import date, datetime
from api.models import Client
from api.models import Devis
from api.models import Facture
from api.models import Connexion
from api.models import Message
from api.models import Tarif
from res.utils import dateConverter

date_converter = dateConverter()


class hello(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if (IsAuthenticated):
            response = json.dumps({
                "success": False,
                "data": "Bad endpoint, missing parameters"
            })
        else:
            response = json.dumps({
                "success": False,
                "data": "Not authenticated"
            })
        return HttpResponse(response, content_type='text/json')


class clientView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
            response = json.dumps({
                "success": True,
                "data": {
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
                "success": False,
                "data": "No client with this id"
            })
        return HttpResponse(response, content_type='text/json')

    def post(self, request):
        try:
            payload = json.loads(request.body)
        except:
            response = json.dumps({
                "success": False,
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
                "success": False,
                "data": {
                    "Missing parameters": missing,
                }
            })
            return HttpResponse(response, content_type='text/json')

        client_id = 0
        clients = Client.objects.all()
        for client in clients:
            if client.id >= client_id:
                client_id = client.id + 1

        if not('adress2' in payload):
            payload['address2'] = ""

        random = hashlib.md5(datetime.now().strftime(
            "%H:%M:%S").encode()).hexdigest()[:8]
        secure_pass = bcrypt.hashpw(
            payload['password'].encode('utf8'), bcrypt.gensalt())

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
                "success": True,
                "data": f"Client {client.name} {client.lastname} ({client.mail}) saved, ID: {client_id}",
            })
        except:
            response = json.dumps({
                "success": False,
                "data": "Unable to save client"
            })

        return HttpResponse(response, content_type='text/json')

    def patch(self, request, client_id):
        try:
            payload = json.loads(request.body)
        except:
            response = json.dumps({
                "success": False,
                "data": "Missing JSON body / Missformated JSON",
            })
            return HttpResponse(response, content_type='text/json')

        try:
            client = Client.objects.get(id=client_id)
        except:
            response = json.dumps({
                "success": False,
                "data": f"User id {client_id} not found",
            })
            return HttpResponse(response, content_type='text/json')

        for key, value in payload.items():
            if key not in ['id', 'password']:
                setattr(client, key, value)

        try:
            client.save()
            response = json.dumps({
                "success": True,
                "data": f"Client {client.name} {client.lastname} ({client.mail}) saved",
            })
        except:
            response = json.dumps({
                "success": False,
                "data": "Unable to save client"
            })

        return HttpResponse(response, content_type='text/json')

    def delete(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
        except:
            response = json.dumps({
                "success": False,
                "data": f"Client id {client_id} not in database",
            })
            return HttpResponse(response, content_type='text/json')
        try:
            client.delete()
            response = json.dumps({
                "success": True,
                "data": f"Client {client_id} deleted",
            })
        except:
            response = json.dumps({
                "success": False,
                "data": f"Unable to delete client {client_id}"
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
                "success": True,
                "data": response_data,
            })

        except:
            response = json.dumps({
                "success": False,
                "data": "No clients"
            })
        return HttpResponse(response, content_type='text/json')

    def delete(self, request):
        clients = Client.objects.all()
        client_count = 0
        for client in clients:
            client.delete()
            client_count += 1
        response = json.dumps({
            "success": True,
            "data": f"All clients have been flushed ! ({client_count})",
        })
        return HttpResponse(response, content_type='text/json')


class devisView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, devis_id):
        try:
            devis = Devis.objects.get(id=devis_id)
            try:
                devis_owner = Client.objects.get(id=devis.owner)
                owner_data = {
                    "id": devis_owner.id,
                    "Name": devis_owner.name,
                    "Last Name": devis_owner.lastname,
                    "Mail": devis_owner.mail,
                    "Phone": devis_owner.phone,
                    "Address": [devis_owner.adress1,
                                devis_owner.adress2,
                                devis_owner.town
                                ]
                }
            except:
                owner_data = devis.owner

            devis_date = date_converter.dateToStr(devis.date, "%d/%m/%Y")
            response = json.dumps({
                "success": True,
                "data": {
                    "id": devis.id,
                    "Owner": owner_data,
                    "Amount": devis.amount,
                    "Date": devis_date,
                    "FullID": devis.fullid
                }
            })
        except:
            response = json.dumps({
                "success": False,
                "data": "No devis with this id"
            })
        return HttpResponse(response, content_type='text/json')

    def post(self, request):
        try:
            payload = json.loads(request.body)
        except:
            response = json.dumps({
                "success": False,
                "data": "Missing JSON body / Missformated JSON",
            })
            return HttpResponse(response, content_type='text/json')

        missing = []
        for elem in Devis.__dict__.keys():
            if elem not in payload and elem not in ['__module__',
                                                    '__str__',
                                                    '__doc__',
                                                    '_meta',
                                                    'DoesNotExist',
                                                    'MultipleObjectsReturned',
                                                    'get_next_by_date',
                                                    'get_previous_by_date',
                                                    'objects',
                                                    'id',
                                                    'fullid',
                                                    'date']:
                missing.append(elem)

        if len(missing) > 0:
            response = json.dumps({
                "success": False,
                "data": {
                    "Missing parameters": missing,
                }
            })
            return HttpResponse(response, content_type='text/json')

        devis_id = 0
        deviss = Devis.objects.all()
        for devis in deviss:
            if devis.id >= devis_id:
                devis_id = devis.id + 1

        if 'date' in payload:
            devis_date = date_converter.strToDate(payload['date'])
        else:
            devis_date = date.today()

        devis_fullid = date_converter.dateToStr(
            devis_date, "%y%m%d")+str(devis_id)

        devis = Devis(id=devis_id,
                      owner=payload['owner'],
                      amount=payload['amount'],
                      date=devis_date,
                      fullid=devis_fullid
                      )
        try:
            devis.save()
            response = json.dumps({
                "success": True,
                "data": f"Devis {devis.fullid} - {devis.date} of {devis.amount} saved",
            })
        except error as e:
            print(e)
            response = json.dumps({
                "success": False,
                "data": "Unable to save devis"
            })

        return HttpResponse(response, content_type='text/json')

    def delete(self, request, devis_id):
        try:
            devis = Devis.objects.get(id=devis_id)
        except:
            response = json.dumps({
                "success": False,
                "data": f"Devis id {devis_id} not in database",
            })
            return HttpResponse(response, content_type='text/json')
        try:
            devis.delete()
            response = json.dumps({
                "success": True,
                "data": f"Devis {devis_id} deleted",
            })
        except:
            response = json.dumps({
                "success": False,
                "data": f"Unable to delete devis {devis_id}"
            })
        return HttpResponse(response, content_type='text/json')


class allDevisView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            deviss = Devis.objects.all()
            response_data = []
            for devis in deviss:
                try:
                    devis_owner = Client.objects.get(id=devis.owner)
                    owner_data = {
                        "id": devis_owner.id,
                        "Name": devis_owner.name,
                        "Last Name": devis_owner.lastname,
                        "Mail": devis_owner.mail
                    }
                except:
                    owner_data = devis.owner

                devis_date = date_converter.dateToStr(devis.date, "%d/%m/%Y")

                response_data.append({
                    "id": devis.id,
                    "Owner": owner_data,
                    "Amount": devis.amount,
                    "Date": devis_date,
                    "FullID": devis.fullid
                })

            response = json.dumps({
                "success": True,
                "data": response_data,
            })

        except:
            response = json.dumps({
                "success": False,
                "data": "No devis"
            })
        return HttpResponse(response, content_type='text/json')

    def delete(self, request):
        deviss = Devis.objects.all()
        devis_count = 0
        for devis in deviss:
            devis.delete()
            devis_count += 1
        response = json.dumps({
            "success": True,
            "data": f"All devis have been flushed ! ({devis_count})",
        })
        return HttpResponse(response, content_type='text/json')


class factureView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, facture_id):
        try:
            facture = Facture.objects.get(id=facture_id)
            try:
                facture_owner = Client.objects.get(id=facture.owner)
                owner_data = {
                    "id": facture_owner.id,
                    "Name": facture_owner.name,
                    "Last Name": facture_owner.lastname,
                    "Mail": facture_owner.mail,
                    "Phone": facture_owner.phone,
                    "Address": [facture_owner.adress1,
                                facture_owner.adress2,
                                facture_owner.town
                                ]
                }
            except:
                owner_data = facture.owner

            facture_date = date_converter.dateToStr(facture.date, "%d/%m/%Y")
            response = json.dumps({
                "success": True,
                "data": {
                    "id": facture.id,
                    "Owner": owner_data,
                    "Amount": facture.amount,
                    "Date": facture_date,
                    "Paid": facture.paid,
                    "Intent_id": facture.intent_id,
                    "FullID": facture.fullid
                }
            })
        except:
            response = json.dumps({
                "success": False,
                "data": "No facture with this id"
            })
        return HttpResponse(response, content_type='text/json')

    def post(self, request):
        try:
            payload = json.loads(request.body)
        except:
            response = json.dumps({
                "success": False,
                "data": "Missing JSON body / Missformated JSON",
            })
            return HttpResponse(response, content_type='text/json')

        missing = []
        for elem in Facture.__dict__.keys():
            if elem not in payload and elem not in ['__module__',
                                                    '__str__',
                                                    '__doc__',
                                                    '_meta',
                                                    'DoesNotExist',
                                                    'MultipleObjectsReturned',
                                                    'get_next_by_date',
                                                    'get_previous_by_date',
                                                    'objects',
                                                    'id',
                                                    'fullid',
                                                    'date',
                                                    'paid',
                                                    'intent_id']:
                missing.append(elem)

        if len(missing) > 0:
            response = json.dumps({
                "success": False,
                "data": {
                    "Missing parameters": missing,
                }
            })
            return HttpResponse(response, content_type='text/json')

        facture_id = 0
        factures = Facture.objects.all()
        for facture in factures:
            if facture.id >= facture_id:
                facture_id = facture.id + 1

        if 'date' in payload:
            facture_date = date_converter.strToDate(payload['date'])
        else:
            facture_date = date.today()

        facture_fullid = date_converter.dateToStr(
            facture_date, "%y%m%d")+str(facture_id)

        facture = Facture(id=facture_id,
                          owner=payload['owner'],
                          amount=payload['amount'],
                          date=facture_date,
                          paid=False,
                          intent_id="",
                          fullid=facture_fullid
                          )
        try:
            facture.save()
            response = json.dumps({
                "success": True,
                "data": f"Facture {facture.fullid} - {facture.date} of {facture.amount} saved",
            })
        except error as e:
            print(e)
            response = json.dumps({
                "success": False,
                "data": "Unable to save facture"
            })

        return HttpResponse(response, content_type='text/json')

    def patch(self, request, facture_id):
        try:
            payload = json.loads(request.body)
        except:
            response = json.dumps({
                "success": False,
                "data": "Missing JSON body / Missformated JSON",
            })
            return HttpResponse(response, content_type='text/json')

        try:
            facture = Facture.objects.get(id=facture_id)
        except:
            response = json.dumps({
                "success": False,
                "data": f"User id {facture_id} not found",
            })
            return HttpResponse(response, content_type='text/json')

        for key, value in payload.items():
            if key not in ['id', 'owner', 'amount', 'date', 'fullID']:
                setattr(facture, key, value)

        try:
            facture.save()
            response = json.dumps({
                "success": True,
                "data": f"Facture {facture.fullid} of {facture.amount} ({facture.owner} paid: {facture.paid}) saved",
            })
        except:
            response = json.dumps({
                "success": False,
                "data": "Unable to save facture"
            })

        return HttpResponse(response, content_type='text/json')

    def delete(self, request, facture_id):
        try:
            facture = Facture.objects.get(id=facture_id)
        except:
            response = json.dumps({
                "success": False,
                "data": f"Facture id {facture_id} not in database",
            })
            return HttpResponse(response, content_type='text/json')
        try:
            facture.delete()
            response = json.dumps({
                "success": True,
                "data": f"Facture {facture_id} deleted",
            })
        except:
            response = json.dumps({
                "success": False,
                "data": f"Unable to delete Facture {facture_id}"
            })
        return HttpResponse(response, content_type='text/json')


class allFactureView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            factures = Facture.objects.all()
            response_data = []
            for facture in factures:
                try:
                    facture_owner = Client.objects.get(id=facture.owner)
                    owner_data = {
                        "id": facture_owner.id,
                        "Name": facture_owner.name,
                        "Last Name": facture_owner.lastname,
                        "Mail": facture_owner.mail
                    }
                except:
                    owner_data = facture.owner

                facture_date = date_converter.dateToStr(
                    facture.date, "%d/%m/%Y")

                response_data.append({
                    "id": facture.id,
                    "Owner": owner_data,
                    "Amount": facture.amount,
                    "Date": facture_date,
                    "Paid": facture.paid,
                    "Intent_id": facture.intent_id,
                    "FullID": facture.fullid
                })

            response = json.dumps({
                "success": True,
                "data": response_data,
            })

        except:
            response = json.dumps({
                "success": False,
                "data": "No factures"
            })
        return HttpResponse(response, content_type='text/json')

    def delete(self, request):
        factures = Facture.objects.all()
        factures_count = 0
        for facture in factures:
            facture.delete()
            factures_count += 1
        response = json.dumps({
            "success": True,
            "data": f"All bills have been flushed ! ({factures_count})",
        })
        return HttpResponse(response, content_type='text/json')
<<<<<<< HEAD


=======
>>>>>>> c8aba7c682dec564e569160eae0ffc8f75bc7e80
class payFactureView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, facture_id):
        response = json.dumps({
            "success": False,
            "data": "To be implemented"
        })
        return HttpResponse(response, content_type='text/json')

    def post(self, request, facture_id):
        response = json.dumps({
            "success": False,
            "data": "To be implemented"
        })
        return HttpResponse(response, content_type='text/json')
class tarifsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, tarif_id):
        try:
            tarif = Tarif.objects.get(id=tarif_id)
            response = json.dumps({
                "success": True,
                "data": {
                    "id": tarif.id,
                    "Category": tarif.category,
                    "Longname": tarif.longname,
                    "Shortname": tarif.shortname,
                    "Price": tarif.price,
                    "Private": tarif.private,
                }
            })
        except:
            response = json.dumps({
                "success": False,
                "data": "No tarif with this id"
            })
        return HttpResponse(response, content_type='text/json')
    
    def post(self, request):

        try:
            payload = json.loads(request.body)
        except:
            response = json.dumps({
                "success": False,
                "data": "Missing JSON body / Missformated JSON",
            })
            return HttpResponse(response, content_type='text/json')

        missing = []
        for elem in Tarif.__dict__.keys():
            if elem not in payload and elem not in ['__module__',
                                                    '__str__',
                                                    '__doc__',
                                                    '_meta',
                                                    'DoesNotExist',
                                                    'MultipleObjectsReturned',
                                                    'objects',
                                                    'id']:
                missing.append(elem)

        if len(missing) > 0:
            response = json.dumps({
                "success": False,
                "data": {
                    "Missing parameters": missing,
                }
            })
            return HttpResponse(response, content_type='text/json')

        tarif_id = 0
        tarifs = Tarif.objects.all()
        for tarif in tarifs:
            if tarif.id >= tarif_id:
                tarif_id = tarif.id + 1

        tarif = Tarif(id=tarif_id,
                        category=payload['category'],
                        longname=payload['longname'],
                        shortname=payload['shortname'],
                        price=payload['price'],
                        private=payload['private'],
                        )
        try:
            tarif.save()
            response = json.dumps({
                "success": True,
                "data": f"Tarif {tarif.shortname} - {tarif.price}€ (Private: {tarif.private}) saved, ID: {tarif_id}",
            })
        except:
            response = json.dumps({
                "success": False,
                "data": "Unable to save tarif"
            })

        return HttpResponse(response, content_type='text/json')
    
    def patch(self, request, tarif_id):
        try:
            payload = json.loads(request.body)
        except:
            response = json.dumps({
                "success": False,
                "data": "Missing JSON body / Missformated JSON",
            })
            return HttpResponse(response, content_type='text/json')

        try:
            tarif = Tarif.objects.get(id=tarif_id)
        except:
            response = json.dumps({
                "success": False,
                "data": f"Tarif id {tarif_id} not found",
            })
            return HttpResponse(response, content_type='text/json')

        for key, value in payload.items():
            if key not in ['id']:
                setattr(tarif, key, value)

        try:
            tarif.save()
            response = json.dumps({
                "success": True,
                "data": f"Tarif {tarif.shortname} {tarif.price}€ (ID: {tarif.id} - Private: {tarif.private}) saved",
            })
        except:
            response = json.dumps({
                "success": False,
                "data": "Unable to save tarif"
            })

        return HttpResponse(response, content_type='text/json')

<<<<<<< HEAD

=======
    def delete(self, request, tarif_id):
        try:
            tarif = Tarif.objects.get(id=tarif_id)
        except:
            response = json.dumps({
                "success": False,
                "data": f"Tarif id {tarif_id} not in database",
            })
            return HttpResponse(response, content_type='text/json')
        try:
            tarif.delete()
            response = json.dumps({
                "success": True,
                "data": f"Tarif {tarif_id} deleted",
            })
        except:
            response = json.dumps({
                "success": False,
                "data": f"Unable to delete tarif {tarif_id}"
            })
        return HttpResponse(response, content_type='text/json')
class allTarifsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            tarifs = Tarif.objects.all()
            tarifs_list = {}
            for tarif in tarifs:
                if tarif.category not in tarifs_list:
                    tarifs_list[tarif.category] = []
                tarifs_list[tarif.category].append({
                    "id": tarif.id,
                    "category": tarif.category,
                    "longname": tarif.longname,
                    "shortname": tarif.shortname,
                    "price": tarif.price,
                    "private": tarif.private,
                })
        
        except:
            response = json.dumps({
                "success": False,
                "data": "No tarifs"
            })
            return HttpResponse(response, content_type='text/json')

        try :
            for category, tarifs in tarifs_list.items():
                tarifs_list[category] = sorted(tarifs, key=lambda tarif: tarif['price'])
            
            response_data = tarifs_list

            response = json.dumps({
                "success": True,
                "data": response_data,
            })

            return HttpResponse(response, content_type='text/json')
        except :
            response = json.dumps({
                "success": False,
                "data": "Error while processing tarif sorting"
            })
            return HttpResponse(response, content_type='text/json')

    def delete(self, request):
        tarifs = Tarif.objects.all()
        tarifs_count = 0
        for tarif in tarifs:
            tarif.delete()
            tarifs_count += 1
        response = json.dumps({
            "success": True,
            "data": f"All tarifs have been flushed ! ({tarifs_count})",
        })
        return HttpResponse(response, content_type='text/json')
>>>>>>> c8aba7c682dec564e569160eae0ffc8f75bc7e80
class connect(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            payload = json.loads(request.body)
        except:
            response = json.dumps({
                "success": False,
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
                "success": True,
                "data": "Connected",
            })
        else:
            response = json.dumps({
                "success": False,
                "data": "Please check password",
            })

        return HttpResponse(response, content_type='text/json')
