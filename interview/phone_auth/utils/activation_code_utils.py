from phone_auth.models import CustomUser, InviteCode


class ActivationCodeManager:

    def __init__(self, user: CustomUser, code: InviteCode) -> None:
        self.user = user
        self.code = code

    def set_activation_code(self):
        if activation_code := self._get_activation_code():
            if self.user.activation_code or self.user.invite_code.invite_code == self.code:
                return False
            self.user.activation_code = activation_code
            self.user.save()
            return True
        else:
            return False

    def _get_activation_code(self):
        try:
            print(self.code)
            invite_code = InviteCode.objects.get(invite_code=self.code)
            return invite_code
        except InviteCode.DoesNotExist:
            return False