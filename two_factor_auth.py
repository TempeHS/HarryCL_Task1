import pyotp  # pip install pyotp
import qrcode # pip install qrcode

def gen_key():
    return pyotp.random_base32()
# Gemerates a random key for 2FA
def gen_url(key, devtag:str):
    return pyotp.totp.TOTP(key).provisioning_uri(name=devtag, issuer_name = 'Dev Diaries Auth')
# Generates a QR code for the user to scan
def get_2fa(devtag:str, key=None):
    if key is None:
        key = gen_key()
    uri = gen_url(key, devtag)
    qrcode.make(uri).save("/workspaces/HarryCL_Task1/static/2fa_pics/newCode.png")
    return key

# Checks the 2FA code
def check_2fa(token, secret):
    totp = pyotp.TOTP(secret)
    return totp.verify(token)
