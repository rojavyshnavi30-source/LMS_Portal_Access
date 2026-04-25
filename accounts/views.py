from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth


def register(request):
    if request.method == 'POST':  # POST = POST => True
        username = request.POST['username']  # Raja
        email = request.POST['email']  # raj@peramsons.com
        password1 = request.POST['password']  # Welcome@123
        password2 = request.POST['password2']  # Welcome@123

        if password1 == password2:  # Welcome@123 == Welcome@123
            if User.objects.filter(username=username).exists():
                print('username Exists...! Try with another name')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    print("Email is already taken, Try another one")
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()  # Send the data to the database : Table : User
                    return redirect('login')
        else:
            print("Password did not match")
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':  # if the condition is true it should enter in to the if condition
        username = request.POST['username']  # raja
        password = request.POST['password']  # Welcome@123
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            print("Login Successfull..!")
            return redirect('course_list')
        else:
            print("Invaild Credentials")
            return redirect('login')
    else:
         return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':    # True
        auth.logout(request)
        print("Logout From Website...")
        return redirect('course_list')


