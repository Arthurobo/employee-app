from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from .serializers import RegistrationSerializer
from rest_framework import generics
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AccountAuthenticationForm
from django.conf import settings
from accounts.models import Account


class MyCustomPagination(PageNumberPagination):
    page_size = 5


class RegistrationView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Account.objects.all()
    serializer_class = RegistrationSerializer



def logout_view(request):
    logout(request)
    return redirect('ticket:tickets')



# New login view that redirects and not like the old login 
# view that uses the get_redirect_f _exists
def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('ticket:tickets')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if request.GET:
                    if request.GET.get("next"):
                        return redirect(request.GET.get('next'))
                return redirect('ticket:tickets')
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, "accounts/login.html", context)




def get_redirect_if_exists(request):
    # redirect = None
    redirect = settings.LOGIN_REDIRECT_URL
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("NEXT"))
    return redirect