from django.db import models


class Client(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=32)
    lastname = models.CharField(max_length=32)
    mail = models.EmailField()
    phone = models.CharField(max_length=16)
    adress1 = models.CharField(max_length=32)
    adress2 = models.CharField(max_length=32)
    town = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    userlevel = models.IntegerField()
    passchange = models.BooleanField()
    randomid = models.CharField(max_length=16)

    def __str__(self):
        return f"[{self.id}] Client {self.lastname} {self.name} ({self.mail})"


class Devis(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    owner = models.IntegerField()
    amount = models.FloatField()
    date = models.DateField()
    fullid = models.CharField(max_length=16)

    def __str__(self):
        return f"[{self.id}] Devis {self.fullid} - {self.amount}€ (on {self.date} to {self.owner})"


class Facture(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    owner = models.IntegerField()
    amount = models.FloatField()
    date = models.DateField()
    paid = models.BooleanField()
    intent_id = models.CharField(max_length=32)
    fullid = models.CharField(max_length=16)

    def __str__(self):
        return f"[{self.id}] Facture {self.fullid} - {self.amount}€ (on {self.date} to {self.owner} paid : {self.paid})"


class Connexion(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    user_id = models.IntegerField()
    ip = models.CharField(max_length=32)
    lasttry = models.DateTimeField()
    trynumber = models.IntegerField()

    def __str__(self):
        return f"[{self.id}] Connexion {self.trynumber} times on {self.ip} ({self.user_id}) - {self.date}"


class Message(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    ip = models.CharField(max_length=32)
    lasttry = models.DateTimeField()
    trynumber = models.IntegerField()
    sender_name = models.CharField(max_length=64)
    sender_mail = models.EmailField()
    content = models.CharField(max_length=1024)
    date = models.DateTimeField()

    def __str__(self):
        return f"[{self.id}] Message from {self.sender_name} ({self.sender_mail}) on {self.date}"


class Tarif(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    category = models.CharField(max_length=32)
    longname = models.CharField(max_length=128)
    shortname = models.CharField(max_length=32)
    price = models.FloatField()
    private = models.BooleanField()

    def __str__(self):
        return f"[{self.id}] Price for {self.shortname} in {self.category} is {self.price} (private: {self.private})"
