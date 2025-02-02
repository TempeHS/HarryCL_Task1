import pyotp  # pip install pyotp
import qrcode # pip install qrcode

def gen_key():
    return pyotp.random_base32()
# Gemerates a random key for 2FA
def gen_url(key):
    return pyotp.totp.TOTP(key).provisioning_uri(name="Dev Diaries", issuer_name = 'Dev Diaries Auth')
# Generates a QR code for the user to scan
def get_2fa():
    key = gen_key()
    uri = gen_url(key)
    qrcode.make(uri).save("/workspaces/HarryCL_Task1/static/2fa_pics/newCode.png")
    return key

# Checks the 2FA code
def check_2fa(key: str, code: str):
    totp = pyotp.TOTP(key)
    return totp.verify(code)
