from phone_auth.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class TokenManager:

    def __init__(self, phone_number: str) -> None:
        self.phone_number = phone_number

    def get_new_token(self) -> dict:
        try:
            user = CustomUser.objects.get(username=self.phone_number)
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        except CustomUser.DoesNotExist:
            return
