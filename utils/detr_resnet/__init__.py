import aiohttp
import numpy as np
import base64
import json
import cv2
from config import init_config
configs=init_config("./config/bot.json")

API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
headers = {"Authorization": configs.huggin["token"]}

async def query(filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(filename,headers=headers) as result:
            resp=await result.read()
        async with session.post(API_URL,data=resp,headers=headers) as res:
            response=await res.text()
            return await tag(resp,json.loads(response))

async def tag(d,lable_list): 
    img = cv2.imdecode(np.frombuffer(d, np.uint8), cv2.IMREAD_COLOR)
    for _ in range(len(lable_list)):
        xmin=int(lable_list[_]["box"]['xmin'])
        xmax=int(lable_list[_]["box"]['xmax'])
        ymin=lable_list[_]["box"]['ymin']
        ymax=int(lable_list[_]["box"]['ymax'])
        lable=lable_list[_]['label']
        scores=lable_list[_]['score']
        print(xmin,xmax,ymin,ymax,lable,scores)
        cv2.rectangle(img=img,pt1=(xmin,ymin),pt2=(xmax,ymax),color=(0, 255, 0),thickness=2)
        font = cv2.FONT_HERSHEY_SIMPLEX  # 定义字体
        imgzi = cv2.putText(img, '{} {:.3f}'.format(lable,scores), (xmin, ymax-20), font, 1.2, (0, 255, 255), 4)
    img = cv2.imencode('.jpg', img)[1]
    image_code = str(base64.b64encode(img))[2:-1]
    return image_code
