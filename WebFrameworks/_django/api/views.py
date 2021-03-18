from django.http import HttpResponse
from .models import MyUser
import json


def results(request):
    if request.method == 'GET':
        users = MyUser.objects.all()
        return HttpResponse(
            json.dumps(
                [
                    {'first_name': user.first_name, 'last_name': user.last_name}
                    for user in users
                ]
            )
        )
