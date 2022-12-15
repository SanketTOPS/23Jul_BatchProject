from django.shortcuts import render,redirect
from .forms import signupForm,UpdateForm,notesForm
from .models import userSignup
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import send_mail
from BatchProject import settings
import random
import requests

# Create your views here.
def index(request):
    if request.method=='POST':
        if request.POST.get('signup')=='signup':
            newuser=signupForm(request.POST)
            if newuser.is_valid():
                newuser.save()
                print("User created successfully!")

                # Email Sending Code
                otp=random.randint(11111,99999)
                sub="Welcome!"
                msg=f"Dear User!\nYour account has been created with us!\nEnjoy our services.\nYour One Time Password {otp}\nIf any query, contact on\nhelp@notesapp.com | +91 9724799469"
                from_email=settings.EMAIL_HOST_USER
                #to_email=["ronakmarvaniya78@gmail.com","shanku.makadia@gmail.com"]
                to_email=[request.POST['username']]
                send_mail(subject=sub,message=msg,from_email=from_email,recipient_list=to_email)

                return redirect('notes')
            else:
                print(newuser.errors)
        elif request.POST.get('login')=='login':
            unm=request.POST['username']
            pas=request.POST['password']

            user=userSignup.objects.filter(username=unm,password=pas)
            uid=userSignup.objects.get(username=unm) # get userid
            print("Userid:",uid.id)
            if user: #true
                print("Login Successfully!")
                request.session['user']=unm
                request.session['uid']=uid.id

                #OTP SMS Sending
                otp=random.randint(11111,99999)
                url = "https://www.fast2sms.com/dev/bulkV2"
                #querystring = {"authorization":"PSqGhvu5BkQv1WEvvWH6PIgV0vr1IcOIEzgsN1fZMHFG0WJapJ1hGGIwYfq8","variables_values":f"{otp}","route":"otp","numbers":"8200035165,+15622286865"}
                querystring = {"authorization":"PSqGhvu5BkQv1WEvvWH6PIgV0vr1IcOIEzgsN1fZMHFG0WJapJ1hGGIwYfq8","message":f"Dear User\nYour account has been logged in some where! If you, so ignor this msg.\nYour OTP is {otp}","language":"english","route":"q","numbers":"8200035165"}
                headers = {
                    'cache-control': "no-cache"
                }
                response = requests.request("GET", url, headers=headers, params=querystring)
                print(response.text)

                return redirect('notes')
            else:
                print("Error! Username or Password does't match.")
    return render(request,'index.html')


def notes(request):
    user=request.session.get('user')
    if request.method=='POST':
        mynote=notesForm(request.POST,request.FILES)
        if mynote.is_valid():
            mynote.save()
            print("Your notes has been uploaded!")
        else:
            print(mynote.errors)
    return render(request,'notes.html',{'user':user})

#@login_required
def profile(request):
    user=request.session.get('user')
    uid=request.session.get('uid')
    cid=userSignup.objects.get(id=uid)
    if request.method=='POST':
        update=UpdateForm(request.POST)
        if update.is_valid():
            update=UpdateForm(request.POST,instance=cid)
            update.save()
            print("Your profile has been updated!")
            return redirect('notes')
        else:
            print(update.errors)
    return render(request,'profile.html',{'user':user,'uid':userSignup.objects.get(id=uid)})

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def userlogout(request):
    logout(request)
    return redirect('/')