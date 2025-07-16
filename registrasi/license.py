#!/usr/bin/env python

"""
Copyright (c) 2023-2025 ibrut developers (https://github.com/khamdihi-dev)
Ganti Nama, Jual Enak Banget Lu, Gk Punya Malu??
"""

import os
import re
import sys
import time
import json
import base64
import random
import requests
import platform
import questionary
import urllib.parse

from datetime import date,datetime,timedelta
from zhfna import utils

P = "\033[97m"
J = "\033[33m"
K = "\033[32m"

class UserKey:
    """Kelas untuk mengelola lisensi pengguna."""

    def __init__(self):
        self.key_file = "data/.data_users.json"
        self.join_file = "data/.join.txt"
        self.info_file = "data/.info.txt"
        self.license_url = f'https://pastebin.com/raw/9k5Ndxr4?nocache={int(time.time())}'

    def konfirmasi_keys(self):
        """Memeriksa apakah lisensi pengguna valid atau kedaluwarsa."""
        return True
        # if os.path.isfile(self.key_file):
        #     try:
        #         with open(self.key_file, "r") as f:
        #             self.mmk = json.loads(f.read())

        #         response = requests.get(
        #             self.license_url,
        #             headers = {
        #                 "Cache-Control": "no-cache",
        #                 "Pragma": "no-cache",
        #                 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        #                 'accept-language': 'id,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        #                 'sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        #                 'sec-ch-ua-mobile': '?0',
        #                 'sec-ch-ua-platform': '"Windows"',
        #                 'sec-fetch-dest': 'document',
        #                 'sec-fetch-mode': 'navigate',
        #                 'sec-fetch-site': 'same-origin',
        #                 'sec-fetch-user': '?1',
        #                 'upgrade-insecure-requests': '1',
        #                 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        #         }).json()
        #         for self.xyz in response['data']['users']:
        #             if self.xyz['email'] == self.mmk['email']:
        #                 self.exp = self.xyz['kadarluarsa']
                        
        #                 hari, bulan_nama, tahun = self.exp.split("/")
        #                 bulan_dict = {"Januari": 1, "Februari": 2, "Maret": 3, "April": 4,"Mei": 5, "Juni": 6, "Juli": 7, "Agustus": 8,"September": 9, "Oktober": 10, "November": 11, "Desember": 12}
        #                 bulan = bulan_dict.get(bulan_nama, 0)
        #                 if bulan == 0:
        #                     print(f"{P}[{J}!{P}] Format tanggal salah: {self.exp}")
        #                     return self.beli_lisensi()
        #                 tanggal_kadaluarsa = date(int(tahun), bulan, int(hari))
        #                 hari_tersisa = (tanggal_kadaluarsa - date.today()).days
        #                 if hari_tersisa < 1:
        #                     print(f"{P}[{J}!{P}] Lisensi Anda sudah kedaluwarsa.")
        #                     return Akses().Daftar()
        #                 return True
                    
        #         print(f"{P}[{J}!{P}] Lisensi tidak ditemukan.")
        #         time.sleep(3)
        #         return Akses().Daftar()


        #     except Exception as e:
        #         input(e)
        #         exit()
        #         # return Akses().Daftar()

        # else:
        #     return Akses().Daftar()

    def beli_lisensi(self, user_name=None):
        """Membantu pengguna membeli lisensi baru."""
        try:
            response = requests.get(self.license_url).text
            new_key = base64.b16encode(platform.platform().encode()).decode()
    
            if re.search(fr"{new_key}.*", response):
                random_str = "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(10))
                unique_device_id = base64.b16encode(f"{platform.platform()}{random_str}".encode()).decode()
            else:
                unique_device_id = new_key
        except Exception as e:
            sys.exit(f"\n{P}[{J}!{P}] Kesalahan: {e}")
    
        harga = 50
        if os.path.isfile('data/.data_users.json') is False:user_point = 0
        else:user_point = json.loads(open('data/.data_users.json','r').read())['point']
        current_date = datetime.now()
        months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", 
                  "Agustus", "September", "Oktober", "November", "Desember"]
        join_date = f"{current_date.day}/{months[current_date.month - 1]}/{current_date.year}"
    
        utils.clear()
        print('Pilih Paket License anda\n')
        self.durasi = int(questionary.select('Pilih masa aktif (per minggu)', choices=['1', '2', '3', '4'], 
                                             style=utils.custom_style, **utils.qursor).ask())
        self.ask = questionary.select('Pilih paket', choices=['Crack dan amanin akun', 'Crack Only', 'Amanin Only'], 
                                      style=utils.custom_style, **utils.qursor).ask()
        
        if self.ask == 'Crack dan amanin akun':
            harga += 100
            
        self.harga = harga * self.durasi
        self.total_point = user_point + self.durasi
        kadarluarsa_date = current_date + timedelta(days=self.durasi * 7)
        kadarluarsa = f"{kadarluarsa_date.day}/{months[kadarluarsa_date.month - 1]}/{kadarluarsa_date.year}"
    
        print(f'\n[+] Kamu memilih paket {J}{self.ask}{P}\n[+] Total belanja : {J}{self.harga}k{P}\n[+] License {unique_device_id}')
        print(f'[+] Kadarluarsa pada: {J}{kadarluarsa}{P}')
        
        self.next = input('\n[?] Lanjut Membeli [y/t] : ').lower()
        if self.next == 't':
            exit('\nGood bye')
    
        print(f'\n[+] Kamu akan diarahkan ke WhatsApp atau kirim manual ke {J}083853140469{P}')
        
        users = json.dumps({
            'email': user_name,
            'license': unique_device_id,
            'paket': self.ask,
            'durasi': self.durasi,
            'totalBelanja': self.harga,
            'daftar': join_date,
            'kadarluarsa': kadarluarsa,
            'point':self.total_point
        }, indent=4)
    
        with open('data/.data_users.json', 'w') as f:
            f.write(users)
        print(f'[+] Kirim kode secara manual jika tidak di arahkan\n{users}')
        encoded_info = urllib.parse.quote(users)
        os.system(f"xdg-open https://wa.me/+6283853140469?text={encoded_info}")
        sys.exit()

class Akses:
    def __init__(self):pass

    def Daftar(self):
        """Membantu pengguna mendaftar."""
        utils.clear()
        return
        # print('[!] Gunakan nomor whatsapp yang kamu gunakan untuk mengirim license')
        # self.email = input('[?] Nomor whatsapp : ')
        # if len(self.email) <10:
        #     print('[!] Nomor tidak valid')
        #     time.sleep(3)
        #     self.Daftar()
        # UserKey().beli_lisensi(self.email)
