from django.contrib.auth import get_user_model
from rest_framework_jwt.views import ObtainJSONWebToken

User = get_user_model()


class AuditedObtainJSONWebToken(ObtainJSONWebToken):
    """
    Wrapper around `ObtainJSONWebToken` that sends an audit signal
    when a user requests a token.
    """
    pass
