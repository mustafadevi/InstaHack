# InstaHack
InstaHack adalah alat penetration testing berbasis Python yang dirancang untuk menguji keamanan akun Instagram melalui metode brute-force pada halaman login. Alat ini hanya ditujukan untuk penggunaan edukatif dan etis. Jangan gunakan untuk aktivitas ilegal.

# Install InstaHack
```bash
pkg update && upgrade
termux-change-repo
pkg install git python -y
git clone https://github.com/zara3303/InstaHack
cd InstaHack
pip3.12 install -r requirements.txt
python3.12 run.py
