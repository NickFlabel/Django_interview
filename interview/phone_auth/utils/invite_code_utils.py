import random
import string
from phone_auth.models import InviteCode, CustomUser

class InviteCodeCreator:

    def __init__(self, user: CustomUser, code: str = None) -> None:
        self.code = code
        self.user = user

    def create_code(self) -> InviteCode:
        self.code = self._get_code()
        self.code_entry = InviteCode()
        self.code_entry.invite_code = self.code
        self.code_entry.user_owner = self.user
        self.code_entry.save()
        return self.code_entry

    def _get_code(self) -> str:
        if not self.code:
            return self._generate_invite_code()
        else:
            if self._check_code_does_not_exist():
                return self.code
            else:
                return self._generate_invite_code()

    def _generate_invite_code(self) -> str:
        while True:
            characters = string.ascii_letters + string.digits
            self.code = ''.join(random.choice(characters) for _ in range(6))
            if self._check_code_does_not_exist():
                return self.code


    def _check_code_does_not_exist(self) -> bool:
        try:
            InviteCode.objects.get(invite_code=self.code)
            return False
        except InviteCode.DoesNotExist:
            return True
