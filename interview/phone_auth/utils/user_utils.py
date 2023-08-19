from phone_auth.models import CustomUser
from .invite_code_utils import InviteCodeCreator

class UserGetterOrCreator:

    def __init__(self, phone_number: str) -> None:
        self.phone_number = phone_number
        self.user = None

    def get_or_create_user(self) -> CustomUser:
        self.user, created = CustomUser.objects.get_or_create(username=self.phone_number)

        if created:
            InviteCodeCreator(self.user).create_code()

        return self.user