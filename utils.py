
import hashlib  # 提供哈希算法的库
import time  # 时间相关操作
from bs4 import BeautifulSoup  # 解析和操作XML的库

def sha1(str):
    return hashlib.sha1(str.encode("utf-8")).hexdigest()

def check_signature(signature, timestamp, nonce, echostr, token):
    """检查签名"""
    tmp_arr = [token, timestamp, nonce]
    tmp_arr.sort()
    tmp_str = "".join(tmp_arr)
    tmp_str = sha1(tmp_str)
    if tmp_str==signature:
        return True
    else:
        return False
    
def mk_res_xml(res, content):
    """生成回复消息的 XML 格式数据"""
    res_text = '''
<xml>
  <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
  <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
  <CreateTime>{CreateTime}</CreateTime>
  <MsgType><![CDATA[text]]></MsgType>
  <Content><![CDATA[{Content}]]></Content>
</xml>
'''.format(ToUserName=res['FromUserName'], FromUserName=res['ToUserName'], Content=content, CreateTime=str(int(time.time()))[:8])
    return res_text


def trans_xml_to_dict(xml):
    """
    将微信支付交互返回的 XML 格式数据转化为 Python Dict 对象
    
    :param xml: 原始 XML 格式数据
    :return: dict 对象
    """
    
    soup = BeautifulSoup(xml, features='xml')
    xml = soup.find('xml')
    if not xml:
        return {}
    
    # 将 XML 数据转化为 Dict
    data = dict([(item.name, item.text) for item in xml.find_all()])
    return data
