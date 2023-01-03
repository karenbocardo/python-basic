import requests
import multiprocessing
import json
import os
from urllib.parse import urlparse
from PIL import Image

API_KEY = "6bkhiD1h7F4aaRTDZ3ysqNceU7ptioLBd1x7wDQx"
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_IMAGES = './output'

global data

'''
response example:

{
    "date": "2021-08-01",
    "explanation": "Pluto is more colorful than we can see. Color data and high-resolution images of our Solar System's most famous dwarf planet, taken by the robotic New Horizons spacecraft during its flyby in 2015 July, have been digitally combined to give an enhanced-color view of this ancient world sporting an unexpectedly young surface. The featured enhanced color image is not only esthetically pretty but scientifically useful, making surface regions of differing chemical composition visually distinct. For example, the light-colored heart-shaped Tombaugh Regio on the lower right is clearly shown here to be divisible into two regions that are geologically different, with the leftmost lobe Sputnik Planitia also appearing unusually smooth. After Pluto, New Horizons continued on, shooting  past asteroid Arrokoth in 2019 and has enough speed to escape our Solar System completely.    Pluto-Related Images with Brief Explanations: APOD Pluto Search",
    "hdurl": "https://apod.nasa.gov/apod/image/2108/PlutoEnhancedHiRes_NewHorizons_5000.jpg",
    "media_type": "image",
    "service_version": "v1",
    "title": "Pluto in Enhanced Color",
    "url": "https://apod.nasa.gov/apod/image/2108/PlutoEnhancedHiRes_NewHorizons_960.jpg"
}
'''

def print_dict(dicc: dict):
    pretty = json.dumps(dicc, indent=4)
    print(pretty)

def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:
    global data
    r = requests.get(url = APOD_ENDPOINT, params = locals())
    
    if r.status_code:
        data = r.json()
        return data

def download_image(elem, original=True):
    if elem["media_type"] == "video": return
    url = elem["url"]
    date = elem["date"]

    img = Image.open(requests.get(url, stream = True).raw)
    
    a = urlparse(url)
    filename = os.path.basename(a.path)
    if original: 
        path = os.path.join(OUTPUT_IMAGES, filename) # use original name from url
        img.save(path)
    else: 
        path = os.path.join(OUTPUT_IMAGES, f"{date}.jpg")
        img.convert('RGB').save(path) # to be able to save all of them as jpg

def download_apod_images(metadata: list):
    global data
    if not data: 
        print("couldn't get images")
        return 
    
    with multiprocessing.Pool() as pool:
        pool.map(download_image, data)

def main():
    if not os.path.exists(OUTPUT_IMAGES):
        os.makedirs(OUTPUT_IMAGES)

    metadata = get_apod_metadata(
        start_date='2021-08-01',
        end_date='2021-09-30',
        api_key=API_KEY,
    )
    download_apod_images(metadata=metadata)


if __name__ == '__main__':
    
    main()
