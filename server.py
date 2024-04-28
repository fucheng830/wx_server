# 加载环境变量
# 读取环境变量
from dotenv import load_dotenv
import os

env_name = '.env' 
dotenv_path = os.path.join(os.path.dirname(__file__), env_name)
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)

import requests
from fastapi import FastAPI, Request
from wechat import WeChat
from config import APP_ID, APP_SECRET
from database import redis_conn, SessionLocal, get_db
from sqlalchemy.orm import Session
from model import *

from typing import Optional
from utils import *
from fastapi import Depends
import logging
from fastapi.responses import JSONResponse

app = FastAPI()

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) # 设置日志级别

@app.get('/wechat/{id}')
def check_url(
    id: str,
    signature: str,
    timestamp: str,
    nonce: str,
    request: Request,
    echostr: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # 根据传入的ID获取服务配置信息
    app_config = db.query(ServiceConfiguration).filter(ServiceConfiguration.id == id).first()
    
    token = app_config.token  # 假设 ServiceConfiguration 模型中有一个存储token的字段
    check_result = check_signature(signature, timestamp, nonce, echostr, token)
    if check_result:
        if echostr:
            return int(echostr)
        else:
            return 'true'
    else:
        return 'false'

@app.post('/wechat/{id}')
async def handle_msg(request: Request, id: str, db: Session = Depends(get_db)):
    """处理消息函数
    
    1. 处理扫码事件
    2. 通知用户扫码场景id给注册验证
    """
    try:
        body = await request.body()
        post_data = trans_xml_to_dict(body)
        # 根据传入的ID获取服务配置信息
        app_config = db.query(ServiceConfiguration).filter(ServiceConfiguration.id == id).first()
        APP_ID = app_config.appid
        APP_SECRET = app_config.appsecret

        # 事件处理
        if post_data.get('Event'):
            if post_data.get('Event') == u'subscribe' or post_data.get('Event') == u'SCAN':
                # 关注事件处理，自动登录或者注册账号
                return parse_subscribe(post_data, APP_ID, APP_SECRET, app_config.parse_event_url)
            
            elif post_data.get('Event') == u'unsubscribe':
                # 取消关注事件处理
                return parse_unsubscribe(post_data)
            elif post_data.get('Event') == u'CLICK':
                # 点击事件处理
                return parse_click(post_data)
        else:
            # 消息处理
            return parse_msg(post_data)
            # return mk_res_xml(post_data, '欢迎关注！')
 
    except ValueError as e:  # 捕获并处理 ValueError 异常
        return JSONResponse(status_code=422, content={"message": "传入的数据无法解析为有效的格式"})


def parse_subscribe(post_data, app_id, app_secret, parse_event_url):
    """关注事件处理"""
    # 获取用户 OpenID
    openid = post_data['FromUserName']
    # 获取用户信息
    wc = WeChat(app_id, app_secret)
    user_info = wc.get_user_info(openid)

    event_key = post_data.get('EventKey')
    if event_key:
        event_key = event_key.strip()
        event_key = event_key.split('_')[-1]
        if event_key:
            qr_scene = str(event_key)
            response = requests.post(parse_event_url, json={'qr_scene': qr_scene, 'user_info': user_info})
            print(response.text)
            if response.status_code != 200:
                return mk_res_xml(post_data, '登录失败！')
            else:
                return mk_res_xml(post_data, '登录成功！')

    return mk_res_xml(post_data, '欢迎关注！我是一个可以帮您保存任意网页进知识库的智能助手，您可以<a href="http://www.baidu.com">点击登录绑定账号</a>，绑定后您可以通过发送网页链接的方式将网页保存到知识库中。在您需要的时候可以随时问我关于您保存的网页的问题。')



def parse_unsubscribe(post_data):
    """取消关注事件处理"""
    # 获取用户 OpenID
    openid = post_data['FromUserName']
    # 获取用户信息
    # user_info = get_user_info(openid)
    return 'success'

def parse_click(post_data):
    """点击事件处理"""
    # 获取用户 OpenID
    openid = post_data['FromUserName']
    # 获取用户信息
    # user_info = get_user_info(openid)
    return 'success'

def parse_msg(post_data):
    """消息处理"""
    # 获取用户 OpenID
    openid = post_data['FromUserName']
    # 获取用户信息
    wc = WeChat(APP_ID, APP_SECRET)
    user_info = wc.get_user_info(openid)
    print(user_info)
    print(post_data)
    return 'success'



@app.post('/{id}/scan_qr')
async def handle_msg(request: Request, id: str, db: Session = Depends(get_db)):
    """处理消息函数
    
    1. 处理扫码事件
    2. 通知用户扫码场景id给注册验证
    """
    try:
        params = await request.json()
        qr_scene = params.get('scene_id')
        if not qr_scene:
            return JSONResponse(status_code=422, content={"message": "参数 scene_id 不能为空"})
        # 根据传入的ID获取服务配置信息
        app_config = db.query(ServiceConfiguration).filter(ServiceConfiguration.id == id).first()
        APP_ID = app_config.appid
        APP_SECRET = app_config.appsecret
        generator = WeChat(APP_ID, APP_SECRET)
        ticket = generator.create_temp_qrcode(str(qr_scene), 604800)
        return {'ticket': ticket}
    except ValueError as e:  # 捕获并处理 ValueError 异常
        return JSONResponse(status_code=422, content={"message": "传入的数据无法解析为有效的格式"})


@app.post('/send_mail')
async def send_mail(request: Request):
    """
    发送邮件的接口

    请求方法：POST
    请求参数：
        - content: 邮件内容
        - access_token: 访问令牌，用于身份验证
    返回结果：
        - 若邮件发送成功，返回邮件发送结果的JSON数据
        - 若邮件发送失败，返回一个包含失败消息的JSON数据
    """
    data = await request.json()
    content = data['content']
    access_token = data['access_token']
    url = f'https://qyapi.weixin.qq.com/cgi-bin/exmail/app/compose_send?access_token={access_token}'
    res = requests.post(url, json=content)
    if res.status_code==200:
        return {'message': '邮件发送成功'}
    else:
        return {'message': '邮件发送失败'}


@app.post('/token')
async def get_access_token(request: Request):
    """处理消息"""
    data = await request.json()
    APPID = data['appid']
    SECRET = data['secret']
    res = requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={APPID}&corpsecret={SECRET}')
    res_data = res.json()
    return res_data['access_token'] 
