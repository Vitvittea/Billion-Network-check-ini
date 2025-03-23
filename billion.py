import requests
import time

# URL untuk check-in harian, mendapatkan info akun, dan status level progres
CHECKIN_URL = "https://signup-backend.billions.network/claim-daily-reward"
USER_INFO_URL = "https://signup-backend.billions.network/me"
LEVEL_PROGRESS_URL = "https://signup-backend.billions.network/power/level-progression"

# Fungsi untuk membaca cookie dari file
def read_cookie_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Membaca cookie dari file
cookie = read_cookie_from_file("cookie.txt")

# Header yang dibutuhkan untuk request, termasuk cookie session_id
headers = {
    "Content-Type": "application/json",
    "Cookie": cookie,
}

def get_user_info():
    response = requests.get(USER_INFO_URL, headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        print("Informasi Akun:")
        print(f"ID Pengguna: {user_info.get('id')}")
        print(f"Nama Pengguna: {user_info.get('username')}")
        print(f"Email: {user_info.get('email')}")
        return True
    else:
        print("Gagal mendapatkan informasi akun:", response.status_code, response.text)
        return False

def get_level_progress():
    response = requests.get(LEVEL_PROGRESS_URL, headers=headers)
    if response.status_code == 200:
        level_data = response.json()
        if isinstance(level_data, list) and len(level_data) > 0:
            # Asumsi elemen pertama di dalam list berisi data level progres
            level_info = level_data[0]
            level = level_info.get("level", "N/A")
            current_progress = level_info.get("current_progress", "N/A")
            next_level_progress = level_info.get("next_level_progress", "N/A")
            print(f"Level: {level}")
            print(f"Current Progress: {current_progress}")
            print(f"Next Level Progress: {next_level_progress}")
            return True
        else:
            print("Data level progres tidak valid atau kosong.")
            return False
    else:
        print("Gagal mendapatkan status level progres:", response.status_code, response.text)
        return False

def checkin():
    response = requests.post(CHECKIN_URL, headers=headers)
    if response.status_code == 200:
        print("Check-in berhasil:", response.json())
    else:
        print("Check-in gagal:", response.status_code, response.text)

if __name__ == "__main__":
    if get_user_info():  # Pastikan informasi akun berhasil diambil
        if get_level_progress():  # Menampilkan status level progres
            checkin()
            print("Menunggu 24 jam untuk check-in berikutnya...")
            time.sleep(86400)  # Tunggu 24 jam
