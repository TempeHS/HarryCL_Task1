import pyotp  # pip install pyotp
import qrcode # pip install qrcode

def gen_key():
    return pyotp.random_base32()

def gen_url(key):
    return pyotp.totp.TOTP(key).provisioning_uri(name="bob", issuer_name = '2fa App')

def verify_code(key: str, code: str):
    totp = pyotp.TOTP(key)
    return totp.verify(code)

def get_2fa():
    key = gen_key()
    uri = gen_url(key)
    qrcode.make(uri).save("/workspaces/HarryCL_Task1/static/2fa_pics/newCode.png")
    return key

def check_2fa(key: str, code: str):
    totp = pyotp.TOTP(key)
    return totp.verify(code)

