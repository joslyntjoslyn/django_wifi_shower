from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import *


class StartShower(APIView):
    def post(self, request):
        return Response(status=status.HTTP_200_OK)


class DeviceStatus(APIView):
    def post(self, request):
        data = request.data
        device = get_object_or_404(Device, mac_id=data['mac_id'])
        return Response(status=status.HTTP_200_OK)

