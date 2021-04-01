from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from fobbage.accounts.forms import UserCreationForm

from fobbage.accounts.serializers import UserSerializer


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


class UserInfoAPIView(APIView):
    """
    Information about the currently authenticated user
    """

    def get(self, request, format=None):
        user = request.user

        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
