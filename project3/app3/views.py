from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED
from rest_framework.authtoken.models import Token
from django.contrib.auth.forms import UserCreationForm
from rest_framework import  permissions
from rest_framework import status
from app3.models import medical
from app3.forms import medicalForm
from app3.serializers import medicineSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q



@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def signup(request):
    form = UserCreationForm(data=request.data)
    if form.is_valid():
        user = form.save()
        return Response("account created successfully", status=HTTP_201_CREATED)
    return Response(form.errors, status=HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def create_medicine(request):
    form = medicalForm(request.POST)
    if form.is_valid():
        medicines = form.save()
        return Response({'id': medicines.id}, status=HTTP_201_CREATED)
    return Response(form.errors, status=HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def list_medicines(request):
    medicines = medical.objects.all()
    serializer = medicineSerializer(medicines, many=True)
    return Response(serializer.data)




@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def update_medicine(request, pk):
    medicines = get_object_or_404(medical, pk=pk)
    form = medicalForm(request.data, instance=medicines)
    if form.is_valid():
        form.save()
        serializer = medicineSerializer(medicines)
        return Response(serializer.data)
    else:
        return Response(form.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def delete_medicine(request, pk):
    try:
        medicines = medical.objects.get(pk=pk)
    except medical.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    medicines.delete()
    return Response("deleted successfully")

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def Search(request):
    q = request.GET.get('search')
    if q:
        medicines = medical.objects.filter(Q(name__istartswith=q))
        serializer = medicineSerializer(medicines, many=True)
        return Response(serializer.data)
    else:
        return Response(status=HTTP_404_NOT_FOUND)

