from .models import User
from rest_framework import authentication, exceptions

class UserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')

        if not user_email or not user_password:
            return None

        try:
            user = User.objects.get(email=user_email)
            if user.password != user_password:
                return None
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Gagal login')

        return (user, None)
