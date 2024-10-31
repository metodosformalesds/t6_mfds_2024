from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail

def simple_mail(request):
    send_mail (subject='hola',
               message='mensaje',
               from_email='u21210757@utp.edu.pe',
               recipient_list=['u21210757@utp.edu.pe'])
    return HttpResponse('Mensaje Enviado')
