# 微信公众号云端公共函数
- 支持pc端微信扫码登录
- 支持微信浏览器点击按钮登录
- 支持获取token

## 使用方法
- 配置服务项目
  配置项：
    - 项目名称
    - appid
    - appsecret


## 1. 微信接口

### 1.1 验证微信URL

- **Endpoint:** `/wechat/{id}`
- **Method:** GET
- **Parameters:**
  - `id` (str): 服务配置ID
  - `signature` (str): 微信加密签名
  - `timestamp` (str): 时间戳
  - `nonce` (str): 随机数
  - `echostr` (Optional[str]): 随机字符串
- **Response:**
  - `int` or `str`: 返回验证结果

### 1.2 处理微信消息

- **Endpoint:** `/wechat/{id}`
- **Method:** POST
- **Parameters:**
  - `id` (str): 服务配置ID
- **Request Body:**
  - XML data: 微信消息数据
- **Response:**
  - XML data: 处理后的消息内容

### 1.3 处理扫码事件

- **Endpoint:** `/{id}/scan_qr`
- **Method:** POST
- **Parameters:**
  - `id` (str): 服务配置ID
- **Request Body:**
  - `scene_id`: 扫码场景ID
- **Response:**
  - JSON: 包含生成的二维码票据

## 2. 邮件发送接口

### 2.1 发送邮件

- **Endpoint:** `/send_mail`
- **Method:** POST
- **Request Body:**
  - `content`: 邮件内容
  - `access_token`: 访问令牌
- **Response:**
  - JSON: 邮件发送结果

## 3. 访问令牌接口

### 3.1 获取访问令牌

- **Endpoint:** `/token`
- **Method:** POST
- **Request Body:**
  - `appid`: 应用ID
  - `secret`: 应用密钥
- **Response:**
  - JSON: 包含访问令牌信息

