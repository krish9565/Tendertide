from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    """
    Custom authentication backend to log in users using their email.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)  # Use email as identifier
            if user.check_password(password):  # Django automatically verifies hashed passwords
                return user
        except User.DoesNotExist:
            return None
