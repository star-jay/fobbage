from rest_framework_simplejwt.views import (
    TokenObtainPairView as TokenObtainPairViewBase,
)

from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from rest_framework import status
from fobbage.accounts.forms import UserCreationForm
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


class TokenObtainPairView(TokenObtainPairViewBase):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Audit the token authentication
            User.objects.get(username=request.data['username'])
        return response


def simple_token(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.data['username'],
            password=request.data['password'])
        token = Token.objects.create(user=user)
        return Response(
            data=dict(token=token), status=201)
