from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserModelSerializer
from .models import UserModel
from django.shortcuts import get_object_or_404


from .forms import *

from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from .forms import UserRegistrationForm
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .forms import UserRegistrationForm
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from django.utils.safestring import mark_safe

# Create your views here.
class UserModelAPI(generics.GenericAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserModelSerializer
    queryset = UserModel.objects.all()
    
    def get(self,request):
        qs = UserModel.objects.all()
        serializer = UserModelSerializer(qs,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request):
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserModelAPI_ID(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserModelSerializer
    queryset = UserModel.objects.all()

    def get_object(self, id):
        return get_object_or_404(UserModel, id=id)
    def get(self,request,id):
        qs = self.get_object(id)
        serializer = UserModelSerializer(qs)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self,request,id):
        qs = self.get_object(id)
        serializer = UserModelSerializer(instance=qs, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        qs = self.get_object(id)
        if qs:
            qs.delete()
            return Response({'msg':'deleted item successfully'})
        return Response({'msg':'not found details'})


def indexPage(request):
    return render(request, 'Login/index.html')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can log in to your account.")
        return redirect('login')  

    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('index')  


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("Login/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        truncated_email = f'{to_email[:3]}...{to_email[-12:]}'
        messages.success(
        request,
        f'<span style="font-family: cursive; font-size: 26px;">Dear {user}, a verification mail has been sent to {truncated_email}. '
        '<br>Please click on the link provided to activate your account.</span>'
)

    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')



def registerPage(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            message = activateEmail(request, user, form.cleaned_data.get('email'))
            messages.success(request, message)
            return redirect('verify')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserRegistrationForm()
    return render( request=request,template_name="Login/signup.html",context={"form": form}
        )

def loginPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        upass = request.POST.get('user_password')
        user = authenticate(request,email=uname,password=upass)
        if user is not None:
            login(request,user)
            return redirect('base')
        else:
            messages.error(request, "Incorrect credentials. Please try again.")
            # Pass the error message to the template
            return render(request, 'Login/login.html', {'error_message': messages.get_messages(request)})
    return render(request,'Login/login.html')

@login_required(login_url='login')
def basePage(request):
    return render(request,'Login/base.html')

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))
@login_required(login_url='login')

def submit_form(request):
    return redirect('base')


def edit_profilePage(request):
    # You can add logic here to retrieve user data if needed
    return render(request, 'Login/edit_profile.html')


def profilePage(request):
    user_posts = request.user.postmodel_set.all()
    return render(request, 'Login/profile.html', {'user_posts': user_posts})
    # return render(request, 'Login/profile.html')

def change_passwordPage(request):
    return render(request, 'Login/change.html')

def verifyPage(request):
    return render(request, 'Login/verify.html')