from phone_auth.models import CustomUser, PhoneCode
import time
import random
import string


class PhoneCodeManager:

    def __init__(self, user: CustomUser) -> None:
        self.user = user

    def reset_code(self):
        code = PhoneCode.objects.get(user=self.user)
        code.code = None
        code.save()

    def get_or_create_code(self) -> str:
        try:
            code = PhoneCode.objects.get(user=self.user)
            if not code.code:
                code.code = self._generate_random_code()
                code.save()
        except PhoneCode.DoesNotExist:
            code = PhoneCode(user=self.user)
            code.code = self._generate_random_code()
            code.save()
        
        return code

    def _generate_random_code(self) -> str:
        return '1234' # Shlould be random but for the sake of simulation is presented as '1234'
    
    def generate_new_code(self) -> None:
        code = PhoneCode.objects.get(user=self.user)
        code.code = self._generate_random_code()
        code.save()


class PhoneCodeSender:

    def __init__(self, code: str, phone_number: str) -> None:
        self.code = code
        self.phone_number = phone_number

    def send_sms_code(self) -> None:
        time.sleep(random.randint(1, 2))


class PhoneCodeChecker:

    def __init__(self, code: str, phone_number: str) -> None:
        self.code = code
        self.phone_number = phone_number

    def check_code_is_valid(self):
        try:
            code = PhoneCode.objects.get(code=self.code)
            user = CustomUser.objects.get(username=self.phone_number)
            if code.code == None:
                return False
            return code.user == user
        except PhoneCode.DoesNotExist or CustomUser.DoesNotExist:
            return False
