import requests
import os
from datetime import datetime
import ctypes

# 必应壁纸 JSON 接口
BING_URL = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"

# 获取当前日期
current_date = datetime.now().strftime("%Y-%m-%d")
download_dir = "C:\\Wallpapers"  # 你希望保存壁纸的路径

# 如果保存文件夹不存在，创建它
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# 使用 requests 获取 JSON 数据
print(f"Fetching JSON from: {BING_URL}")
response = requests.get(BING_URL)

# 检查响应是否成功
if response.status_code == 200:
    print("Successfully fetched the JSON!")
    json_data = response.json()

    # 提取图片 URL
    image_url = json_data["images"][0]["url"]
    print(f"Image URL: https://www.bing.com{image_url}")

    # 生成壁纸的本地文件路径，按当前日期命名
    wallpaper_filename = f"BingWallpaper_{current_date}.jpg"
    wallpaper_path = os.path.join(download_dir, wallpaper_filename)

    # 下载壁纸
    wallpaper_url = f"https://www.bing.com{image_url}"
    image_response = requests.get(wallpaper_url)

    if image_response.status_code == 200:
        with open(wallpaper_path, 'wb') as f:
            f.write(image_response.content)
        print(f"Wallpaper downloaded to {wallpaper_path}")

        # 设置壁纸为桌面背景
        # Windows 操作系统
        ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 3)
        print("Wallpaper set as desktop wallpaper.")
    else:
        print(f"Failed to download the image. Status code: {image_response.status_code}")
else:
    print(f"Failed to fetch JSON. Status code: {response.status_code}")
