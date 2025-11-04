from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(object):
    def authenticate(self, request, username=None, password=None):
        User = get_user_model()
        user = None
        # Try by email first, but handle non-unique emails safely
        if username and '@' in str(username):
            user = User.objects.filter(email=username).order_by('id').first()
        # Fallback to username
        if not user:
            user = User.objects.filter(username=username).order_by('id').first()
        if not user:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
