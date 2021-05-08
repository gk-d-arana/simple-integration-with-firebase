from django.http import Http404

from django.shortcuts import render, redirect

import pyrebase


# imports to send messages to mobile apps
"""
from fcm_django.models import FCMDevice

from fcm_django.fcm import fcm_send_message

import firebase_admin

from firebase_admin import credentials

cred = credentials.Certificate("path to your admin config key")
firebase_admin.initialize_app(cred)
"""

firebaseConfig = {
    "apiKey": "#########################",
    "databaseURL": "#########################",
    "authDomain": "#########################",
    "projectId": "#########################",
    "storageBucket": "#########################",
    "messagingSenderId": "#########################",
    "appId": "#########################",
    "measurementId": "#########################"
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

db = firebase.database()


def phone_verification(request, phone_number):
    if 'unverified' in request.session:
        try:
            del request.session['unverified']
        except KeyError:
            pass
        return render(request, 'users/phone_verification.html', {'phone_number': phone_number})
    else:
        raise Http404


def home_view(request):
    return render(request, 'users/home.html', {})


def signup_view(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phonenumber = request.POST.get('phonenumber')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            auth.create_user_with_email_and_password(email, password)
        except:
            return render(request, 'users/signup.html', {'message': 'Sorry Email Already Exists'})
        try:
            data = {'firstname': firstname, 'lastname': lastname, 'email': email, 'phonenumber': phonenumber,'password': password}
            db.child('Users').child(f'user {UsersCount[0].val()+1}').set(data)
            newCount = UsersCount[0].val() + 1
            db.child('UsersCount').update({'UsersCount': newCount})
        except Exception as e:
            print(e)
            return render(request, 'users/signup.html', {'message': 'Sorry An Error Occured'})
        request.session['unverified'] = "Yes"
        if phonenumber[0] == '+':
            real_phonenumber = phonenumber[1:]
            print(real_phonenumber)
        else:
            real_phonenumber = phonenumber
        return redirect(phone_verification, real_phonenumber)
    return render(request, 'users/signup.html', {})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            auth.sign_in_with_email_and_password(email, password)
        except:
            return render(request, 'users/login.html', {'message': 'Sorry Please Check Your Email Or Password'})
        return render(request, 'users/home.html', {'message': 'Successfuly logged in'})
    return render(request, 'users/login.html', {})
