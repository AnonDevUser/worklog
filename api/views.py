from rest_framework.decorators import api_view
from rest_framework.response import Response
from book.models import UserProfile, Task
from .serializers import UserSerializer, TaskSerializer 

@api_view(["GET"])
def main(request):
    return Response({"message": "Hello, World!"})

@api_view(["POST"])
def set_task(request):
    ...

@api_view(["GET"])
def get_task(request):
    ...

@api_view(["POST"])
def edit_task(request):
    ...

@api_view(["GET"])
def summary(request):
    ...
