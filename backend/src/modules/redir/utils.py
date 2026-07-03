import secrets
import string


def redir_random_url():
    chars = string.ascii_letters + string.digits
    short_code = ''.join(secrets.choice(chars) for _ in range(7))
    return short_code