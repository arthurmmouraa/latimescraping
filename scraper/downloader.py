import os

import requests
from loguru import logger


def download_image(image_url, save_dir):
    if not image_url:
        return None
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        filename = extract_image_filename(image_url)
        save_path = os.path.join(save_dir, filename)
        with open(save_path, "wb") as out_file:
            for chunk in response.iter_content(chunk_size=8192):
                out_file.write(chunk)
        logger.info("Image successfully downloaded: {}", filename)
        return filename
    except requests.RequestException as e:
        logger.error("Error downloading the image {}: {}", image_url, e)
        return None


def extract_image_filename(image_src):
    if image_src:
        img_filename = image_src.replace("%2F", "/")
        img_filename = img_filename.split("/")[-1]
        return img_filename
    return None
