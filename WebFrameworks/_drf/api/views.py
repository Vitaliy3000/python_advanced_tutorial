from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MyUser
from .serializers import MyUserSerializer


class ProductListView(APIView):
    def get(self, request):
        users = MyUser.objects.all()
        serializer = MyUserSerializer(users, many=True)
        return Response(serializer.data)
