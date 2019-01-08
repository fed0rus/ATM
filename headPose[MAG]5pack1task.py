import requests

#ru.imgbb.com
#BB-код полноразмерного со ссылкой
#В переменную "a" вставить BB-код, предварительно загрузив на сайт фотографии
a = '''[url=https://imgbb.com/][img]https://i.ibb.co/G9yz37F/0.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/Db9mCC4/1.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/hVYYWs6/2.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/GRpVrkG/3.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/99CxqNf/4.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/ccnGrgB/5.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/VYH9Hzj/6.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/b5N6MnL/7.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/6Z8gkRb/8.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/pJHNLgL/9.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/Lh1sqc8/10.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/S7kHbQ0/11.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/KNFbF9f/12.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/wNkcGkQ/13.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/Rz0dnX2/14.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/3RLfzRQ/15.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/gdGGptL/16.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/S00Z1z4/17.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/p36SLwv/18.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/bBNsh2Y/19.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/5Tk0Qz1/20.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/6BdVP3g/45.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/KyFKd4v/22.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/MPN9TzD/23.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/Ct3HC4s/24.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/23G1mXD/25.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/gRNMkHB/26.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/ct7JZNN/27.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/Rp45KkY/28.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/dMzBcqC/29.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/zndRhb3/30.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/nMfH3Th/31.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/JqkY9Rg/32.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/ctrmTvV/33.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/yBSnDcr/34.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/HqHpS51/35.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/HDnKBw6/36.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/QccFKZp/37.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/VxZgctq/38.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/zJKJLzW/39.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/HH9G1pb/3.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/2WNwD2z/41.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/555smZx/42.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/gy22kzS/43.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/k9jtvh4/44.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/RD9x2Fd/45.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/k6xscyk/46.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/bQNF1Y3/47.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/Y4SKz6T/48.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/3pZtc5g/49.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/pvxW3Qt/50.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/hM9L0Bq/95.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/10nr4fw/52.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/gjGv8rG/53.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/4FbHp38/54.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/vX7pWCR/55.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/N7xD1tz/56.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/spTJjH3/57.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/khdDCcK/58.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/10q1Pxt/59.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/s6hYYCf/60.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/yFKrpzY/61.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/HTZ37wW/62.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/ZBRsWcM/63.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/Qfyyw4K/64.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/pvZJfs9/65.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/rM4ZH1f/60.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/2svbPND/67.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/PC6c0c6/68.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/TkY5Ryc/69.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/HV3gx6d/70.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/8rBKBwD/71.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/k5WSmNL/72.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/8DN1V8q/73.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/D1LyJQT/74.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/qBzNL9m/75.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/XJt0nRT/76.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/MCycs3S/77.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/zfMFCR5/78.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/DbqbsMS/79.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/PgDgLfR/80.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/x6LcmtL/81.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/XzRwfp3/82.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/7pz3FjG/83.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/SmHh142/84.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/3FKd0nm/85.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/NrLf7Cx/86.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/t414LMH/87.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/HtQrzRR/88.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/QFxtcxw/89.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/bNsgQh7/90.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/cDFGTFq/91.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/d5cZBCC/92.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/T1Zf8fS/93.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/HHZ4mhH/94.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/hW2M9z9/95.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/3TvCmFq/96.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/kG02LK3/97.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/6szSQGt/98.jpg[/img][/url]
[url=https://imgbb.com/][img]https://i.ibb.co/g7RdZKd/99.jpg[/img][/url]'''.replace('[url=https://imgbb.com/][img]', '').replace('[/img][/url]', '')
a = a.split('\n')


headers = {'Ocp-Apim-Subscription-Key': your_key} #Сюда вставить ключ

params = {
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'headPose',
}

rollLeft = []
rollRight = []
turnLeft = []
turnRight = []

for i in range(len(a)):

    face_api_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect' #Ссылка на API
    image_url = a[i]

    response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
    faces = response.json()
    roll = faces[0]['faceAttributes']['headPose']['roll']
    yaw = faces[0]['faceAttributes']['headPose']['yaw']
    if (roll > 15):
        rollLeft.append(i)
    elif (roll < -15):
        rollRight.append(i)
    if (yaw > 15):
        turnLeft.append(i)
    elif (yaw < -15):
        turnRight.append(i)
    print(i, faces)


print('roll left: ', end='')
for i in rollLeft:
    print(i, end=' ')
print()
print('roll right: ', end='')
for i in rollRight:
    print(i, end=' ')
print()
print('turn left: ', end='')
for i in turnLeft:
    print(i, end=' ')
print()
print('turn right: ', end='')
for i in turnRight:
    print(i, end=' ')
