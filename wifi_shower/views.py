import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import *
from .utils import send_command_to_device

SHOWER_MODE_TEXT = ['setup', 'post', 'challenge']


class StartShower(APIView):
    def post(self, request):
        data = request.data
        profile = get_object_or_404(Profile, pk=data['profile_id'])
        if not profile.user_id == data['user_id']:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        device = get_object_or_404(Device, pk=data['device_id'])
        if not device.user_id == data['user_id']:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not profile.old_shower_habits and data['shower_mode'] != 0:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Can not find old shower habits.'})

        showering_data = ShoweringData.objects.filter(user_id=data['user_id'], device_id=data['device_id'],
                                                      status=False).first()
        # if already doing shower
        if showering_data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Already doing shower.'})

        profile.last_shower_date = datetime.datetime.now()
        profile.save()
        showering_data = ShoweringData.objects.create(user_id=data['user_id'], profile_id=data['profile_id'],
                                                      device_id=data['device_id'], shower_mode=data['shower_mode'],
                                                      challenge_level=data.get('challenge_level'))

        send_command_to_device(device.mac_id + '_shower/command', 'starting')
        send_command_to_device(device.mac_id + '_shower/shower_mode', SHOWER_MODE_TEXT[showering_data.shower_mode])

        if showering_data.shower_mode != 0:
            send_command_to_device(device.mac_id + '_shower/shower_temp', profile.shower_temp)
        # if challenge mode
        elif showering_data.shower_mode == 2:
            send_command_to_device(device.mac_id + '_shower/chall_level', showering_data.challenge_level)
            challenge_time = profile.average_shower_time - (profile.aggregate_shower_savings * showering_data.challenge_level / 100.0) / 4.0 * 60
            send_command_to_device(device.mac_id + '_shower/chall_time', challenge_time)
            showering_data.challenge_time = challenge_time
            showering_data.save()

        return Response(status=status.HTTP_201_CREATED)


class DeviceStatus(APIView):
    def post(self, request):
        data = request.data
        device = get_object_or_404(Device, mac_id=data['mac_id'])
        alarm = data.get('alarm')
        if alarm:
            send_command_to_device(device.mac_id + '_shower/alarm', alarm)
        else:
            state = data.get('state')
            if not state:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            showering_data = get_object_or_404(ShoweringData, device_id=device.id, status=False)
            profile = showering_data.profile

            shower_cycle = data['shower_cycle']
            gallons_used = shower_cycle / 60.0 * 4
            shower_temp = data['shower_temp']
            gallons_saved = 0
            if profile.old_shower_habits:
                gallons_saved = gallons_used - profile.old_shower_habits
            # if setup mode
            if showering_data.shower_mode == 0:
                preheat_cycle = data['preheat_cycle']
                old_shower_habits = (preheat_cycle + shower_cycle) / 60.0 * 4.5
                showering_data.preheat_cycle = preheat_cycle
                showering_data.old_shower_habits = old_shower_habits
                profile.old_shower_habits = old_shower_habits
            # if challenge mode
            elif showering_data.shower_mode == 3:
                profile.challenge_level = showering_data.challenge_level

            showering_data.shower_cycle = shower_cycle
            showering_data.shower_temp = shower_temp
            showering_data.gallons_used = gallons_used
            showering_data.gallons_saved = gallons_saved
            showering_data.average_shower_time = (profile.average_shower_time * profile.shower_count + shower_cycle) / (profile.shower_count + 1)
            showering_data.aggregate_shower_savings = profile.aggregate_shower_savings + gallons_saved
            showering_data.average_shower_savings = showering_data.aggregate_shower_savings / (profile.shower_count + 1)
            showering_data.status = True
            showering_data.save()

            profile.shower_cycle = shower_cycle
            profile.gallons_saved = gallons_saved
            profile.shower_temp = shower_temp
            profile.average_shower_time = showering_data.average_shower_time
            profile.aggregate_shower_savings = showering_data.aggregate_shower_savings
            if showering_data.shower_mode != 0:
                profile.shower_count += 1
            profile.save()

        return Response(status=status.HTTP_200_OK)

