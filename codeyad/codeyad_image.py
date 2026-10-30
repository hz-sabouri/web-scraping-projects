import requests
from urllib.parse import urljoin
import os

url = "https://api.codeyad.com/api/course/getByFilter"
url_image1 ="https://codeyad.com/_ipx/w_600&f_webp&q_90&fit_contain/codeyad/assets/images/Courses/"
images = []
folder_path = 'D:/learn/Web Scraping codeyad/exercise/chapter3/images'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

for i in range(1,15):
    params = {
        'pageId' : i,
        'take' : 12
    }
    response = requests.get(url,params=params)
    datajson = response.json()
    for item in datajson['data']['data']:
        uri_image2 = item["imageName"]
        url_image = urljoin(url_image1,uri_image2)
        images.append(url_image)
    
for idx, image_url in enumerate(images):
    response0 = requests.get(image_url)
    
    if response0.status_code == 200:
        content = response0.content
        image_name = f'image_{idx + 1}.jpg' 
        image_path = os.path.join(folder_path, image_name)

        with open(image_path, 'wb') as image:
            image.write(content)
        print(f"Image {idx + 1} downloaded successfully.")
    else:
        print(f"Failed to download image {idx + 1}. Status code: {response0.status_code}")