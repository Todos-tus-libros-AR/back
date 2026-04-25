import secrets
import string


def generate_code():
    from .models import Discount

    while True:
        code = "".join(
            secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        if not Discount.objects.filter(code=code).exists():
            return code
