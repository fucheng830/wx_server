import requests
import json

class WeChat:
    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret
        self.access_token = self.get_access_token()

    def get_access_token(self):
        url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.appid}&secret={self.secret}'
        response = requests.get(url)
        access_token = response.json()['access_token']
        return access_token

    def create_temp_qrcode(self, scene_id, expire_seconds):
        url = f'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={self.access_token}'
        data = {
            "expire_seconds": expire_seconds,
            "action_name": "QR_SCENE",
            "action_info": {
                "scene": {
                    "scene_id": scene_id
                }
            }
        }
        response = requests.post(url, json=data)
        ticket = json.loads(response.text)['ticket']
        return ticket

    def create_permanent_qrcode(self, scene_id):
        url = f'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={self.access_token}'
        data = {
            "action_name": "QR_LIMIT_SCENE",
            "action_info": {
                "scene": {
                    "scene_id": scene_id
                }
            }
        }
        response = requests.post(url, json=data)
        ticket = json.loads(response.text)['ticket']
        return ticket

    def get_qrcode_image(self, ticket):
        ticket = requests.utils.quote(ticket)
        url = f'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={ticket}'
        response = requests.get(url)
        with open('qrcode.jpg', 'wb') as f:
            f.write(response.content)

    def get_user_info(self, openid):
        url = f"https://api.weixin.qq.com/cgi-bin/user/info?access_token={self.access_token}&openid={openid}&lang=zh_CN"
        response = requests.get(url)
        data = response.json()
        return data

if __name__=='__main__':

    # 示例使用
    appid = 'wxxxxxxxxxxxxxxxxx'
    secret = 'afxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    generator = WeChat(appid, secret)

    # 示例：生成临时二维码
    scene_id = 123
    expire_seconds = 604800
    ticket = generator.create_temp_qrcode(scene_id, expire_seconds)
    generator.get_qrcode_image(ticket)

    # 示例：生成永久二维码
    scene_id = 123
    ticket = generator.create_permanent_qrcode(scene_id)
    generator.get_qrcode_image(ticket)