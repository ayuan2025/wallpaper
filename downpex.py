import os
import requests
import random
import ctypes
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Pexels API
PEXELS_API_KEY = "dctBkbiFXRmqiC9nBveSW6Adiwo0xjpnuctguxnAv3jeBJH9Q7wdSqCp"
PEXELS_API_URL = "https://api.pexels.com/v1/curated"
headers = {
    "Authorization": PEXELS_API_KEY
}

# 壁纸存储目录
wallpapers_dir = "C:/Wallpapers"

# 确保目录存在
if not os.path.exists(wallpapers_dir):
    os.makedirs(wallpapers_dir)

def fetch_wallpaper():
    """
    获取符合宽高比要求的壁纸
    """
    print("Fetching wallpaper...")
    params = {
        "orientation": "landscape",  # 横向壁纸
        "size": "large",  # 大尺寸
        "page": random.randint(1, 10)  # 随机选择一页结果，避免每次获取相同的壁纸
    }

    # 设置请求重试机制
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    try:
        response = session.get(PEXELS_API_URL, headers=headers, params=params, verify=False)  # 禁用 SSL 验证
        if response.status_code == 200:
            data = response.json()
            if data['photos']:
                # 随机选择一张壁纸
                photo = random.choice(data['photos'])
                # 计算宽高比，确保是横向的
                width = photo['width']
                height = photo['height']
                aspect_ratio = width / height
                print(f"Wallpaper width: {width}, height: {height}, aspect ratio: {aspect_ratio}")

                # 放宽比例要求，宽高比在 1.5 到 3 之间即可
                if 1.5 <= aspect_ratio <= 3:
                    print("Found suitable wallpaper.")
                    return photo['src']['original']  # 使用原始尺寸的图片
                else:
                    print("Wallpaper aspect ratio is not within the acceptable range.")
            else:
                print("No photos found in the response.")
        else:
            print(f"Failed to fetch data from Pexels. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return None

def download_wallpaper(url):
    """
    下载壁纸
    """
    try:
        print(f"Downloading wallpaper from {url}...")
        response = requests.get(url)
        if response.status_code == 200:
            # 使用日期时间命名图片
            file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
            file_path = os.path.join(wallpapers_dir, file_name)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Wallpaper downloaded successfully: {file_name}")
            return file_path
        else:
            print(f"Failed to download wallpaper. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while downloading: {e}")
    return None

def set_wallpaper(file_path):
    """
    设置桌面壁纸
    """
    try:
        print(f"Setting wallpaper: {file_path}")
        ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 3)
        print("Wallpaper set successfully.")
    except Exception as e:
        print(f"Failed to set wallpaper: {e}")

def main():
    """
    主程序：循环获取壁纸，直到找到合适的横向壁纸
    """
    retry_count = 0
    max_retries = 100  # 增加最大重试次数

    print("Starting wallpaper program...")

    while retry_count < max_retries:
        wallpaper_url = fetch_wallpaper()
        if wallpaper_url:
            wallpaper_path = download_wallpaper(wallpaper_url)
            if wallpaper_path:
                set_wallpaper(wallpaper_path)
                break  # 成功下载并设置壁纸，退出循环
            else:
                print("Failed to download wallpaper.")
        else:
            print("No suitable wallpaper found.")
        
        retry_count += 1
        print(f"Retrying... ({retry_count}/{max_retries})")

    if retry_count == max_retries:
        print("Reached maximum retry attempts. Exiting.")

if __name__ == "__main__":
    main()
