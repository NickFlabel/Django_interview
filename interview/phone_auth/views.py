from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions

from .models import CustomUser, InviteCode
from .serializers import UserProfileSerializer, PhoneNumberSerializer, PhoneCodeSerializer, ActivateCodeSerializer
from .utils.user_utils import UserGetterOrCreator
from .utils.phone_code_utils import PhoneCodeManager, PhoneCodeSender, PhoneCodeChecker
from .utils.token_utils import TokenManager
from .utils.activation_code_utils import ActivationCodeManager
# Create your views here.

schema_view = get_schema_view(
    openapi.Info(
        title="Phone auth API",
        default_version='v1',
        description="API for Phone auth",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

class EnterPhoneNumber(APIView):

    @swagger_auto_schema(operation_description='Send user phone number for authorization', responses={200: None}, request_body=PhoneNumberSerializer)
    def post(self, request):
        phone_number = request.data.get('phone_number')
        user = UserGetterOrCreator(phone_number).get_or_create_user()
        code = PhoneCodeManager(user=user).get_or_create_code()
        PhoneCodeSender(phone_number=phone_number, code=code).send_sms_code()
        return Response(status=status.HTTP_200_OK)
    

class EnterPhoneCode(APIView):
    
    @swagger_auto_schema(operation_description='Send user phone code to get JWT token and finish authorization', responses={200: None, 403: None}, request_body=PhoneCodeSerializer)
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        tokens = TokenManager(phone_number).get_new_token()
        if PhoneCodeChecker(code=code, phone_number=phone_number).check_code_is_valid():
            PhoneCodeManager(user=CustomUser.objects.get(username=phone_number)).reset_code()
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class ProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return CustomUser.objects.all()
    
    @swagger_auto_schema(operation_description='Get user profile info', responses={200: None})
    def retrieve(self, request, *args, **kwargs):
        profile_user = self.get_object()
        if profile_user == request.user:
            serializer = self.get_serializer(profile_user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    
    
class ProfileRedirect(APIView):

    @swagger_auto_schema(operation_description='Redirects user to his profile', responses={301: None})
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile-detail', pk=request.user.pk)
        else:
            return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


class ActivationCode(APIView):
    permission_classes = [IsAuthenticated,]

    @swagger_auto_schema(operation_description='Set invite code from another user as current users activation code', responses={200: None},  request_body=ActivateCodeSerializer)
    def post(self, request):
        code = request.data.get('code')
        if ActivationCodeManager(user=request.user, code=code).set_activation_code():
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class Reset(APIView):
    parser_classes = []

    @swagger_auto_schema(operation_description='Delete all info from DB (for tests)', responses={200: None})
    def get(self, request):
        for user in CustomUser.objects.all():
            user.delete()
        return Response(status=status.HTTP_200_OK)

