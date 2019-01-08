import requests

#headers в соответствии с функией
headers = {'Ocp-Apim-Subscription-Key': your_key} #Сюда ключ

#Параметры в соответствии с функией
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
image_url = 'https://lover.ru/cache/images/9c4d96175c1835df4854e91008218203/resizeCrop_700_525_center_center__.jpg'

response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
faces = response.json()
print(faces)
