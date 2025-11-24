"""
微信 API 工具类
"""
import httpx
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
from wxcloudrun.core.config import get_settings


class WeChatAPIError(Exception):
    """微信 API 错误"""
    def __init__(self, errcode: int, errmsg: str):
        self.errcode = errcode
        self.errmsg = errmsg
        super().__init__(f"微信API错误 [{errcode}]: {errmsg}")


 


class WeChatAPI:
    """微信小程序 API 客户端"""
    
    BASE_URL = "https://api.weixin.qq.com"
    
    def __init__(self):
        settings = get_settings()
        self.appid = settings.wx_appid
        self.appsecret = settings.wx_appsecret
        self.verify = settings.ca_bundle_path or settings.http_verify
        self.logger = logging.getLogger(__name__)
        
        if not self.appid or not self.appsecret:
            raise ValueError("微信小程序 AppID 和 AppSecret 未配置")
    
    async def code2session(self, code: str) -> Dict[str, str]:
        """
        登录凭证校验
        
        Args:
            code: 小程序登录时获取的 code
            
        Returns:
            {
                "openid": "用户唯一标识",
                "session_key": "会话密钥",
                "unionid": "用户在开放平台的唯一标识符"  # 可选
            }
            
        Raises:
            WeChatAPIError: 微信API返回错误时抛出
        """
        url = f"{self.BASE_URL}/sns/jscode2session"
        params = {
            "appid": self.appid,
            "secret": self.appsecret,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        
        self.logger.info("WeChatAPI.code2session: request begin")
        async with httpx.AsyncClient(verify=self.verify) as client:
            response = await client.get(url, params=params)
            data = response.json()
        self.logger.info(f"WeChatAPI.code2session: response received errcode={data.get('errcode')} openid={data.get('openid')}")
        
        # 检查错误
        if "errcode" in data and data["errcode"] != 0:
            self.logger.error(f"WeChatAPI.code2session: error errcode={data.get('errcode')} errmsg={data.get('errmsg')}")
            raise WeChatAPIError(data["errcode"], data.get("errmsg", "未知错误"))
        
        return {
            "openid": data.get("openid"),
            "session_key": data.get("session_key"),
            "unionid": data.get("unionid")
        }
    
    async def check_session_key(self, openid: str, session_key: str) -> bool:
        """
        检验登录态
        
        Args:
            openid: 用户唯一标识
            session_key: 会话密钥
            
        Returns:
            True: session_key 有效
            False: session_key 无效
            
        Note:
            根据微信文档，checkSessionKey 接口需要 access_token
            但实际上微信推荐的做法是通过调用其他需要 session_key 的接口来验证
            这里我们采用调用 getUserInfo 解密的方式来间接验证
        """
        # 微信官方文档：https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/checkSessionKey.html
        # 需要先获取 access_token
        access_token = await self._get_access_token()
        
        url = f"{self.BASE_URL}/wxa/checksession"
        params = {
            "access_token": access_token,
            "openid": openid,
            "signature": "",  # 这里需要根据实际情况计算签名
            "sig_method": "hmac_sha256"
        }
        
        try:
            async with httpx.AsyncClient(verify=self.verify) as client:
                response = await client.get(url, params=params)
                data = response.json()
            self.logger.info(f"WeChatAPI.check_session_key: response errcode={data.get('errcode')} openid={openid}")
            # errcode=0 表示有效，errcode=87009 表示无效
            return data.get("errcode") == 0
        except Exception:
            self.logger.exception("WeChatAPI.check_session_key: exception")
            return False
    
    async def reset_session_key(self, openid: str, session_key: str) -> Dict[str, str]:
        """
        重置登录态
        
        Args:
            openid: 用户唯一标识
            session_key: 当前会话密钥
            
        Returns:
            {
                "openid": "用户唯一标识",
                "session_key": "新的会话密钥"
            }
            
        Raises:
            WeChatAPIError: 微信API返回错误时抛出
        """
        # 微信官方文档：https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/ResetUserSessionKey.html
        access_token = await self._get_access_token()
        
        url = f"{self.BASE_URL}/wxa/resetusersessionkey"
        params = {
            "access_token": access_token
        }
        
        data = {
            "openid": openid,
            "signature": "",  # 需要根据实际情况计算签名
            "sig_method": "hmac_sha256"
        }
        
        self.logger.info("WeChatAPI.reset_session_key: request begin")
        async with httpx.AsyncClient(verify=self.verify) as client:
            response = await client.post(url, params=params, json=data)
            result = response.json()
        self.logger.info(f"WeChatAPI.reset_session_key: response errcode={result.get('errcode')} openid={result.get('openid')}")
        
        # 检查错误
        if "errcode" in result and result["errcode"] != 0:
            self.logger.error(f"WeChatAPI.reset_session_key: error errcode={result.get('errcode')} errmsg={result.get('errmsg')}")
            raise WeChatAPIError(result["errcode"], result.get("errmsg", "未知错误"))
        
        return {
            "openid": result.get("openid"),
            "session_key": result.get("session_key")
        }
    
    async def _get_access_token(self) -> str:
        """
        获取接口调用凭证 access_token（数据库缓存）
        """
        from wxcloudrun.core.database import SessionLocal
        from wxcloudrun.crud.wechat_token import get_token, upsert_token

        # 1. 读缓存
        try:
            with SessionLocal() as db:
                rec = get_token(db, self.appid)
                if rec and rec.expires_at > datetime.utcnow():
                    return rec.token
        except Exception:
            # 数据库不可用或表未创建时，跳过DB缓存
            pass

        # 2. 请求微信
        url = f"{self.BASE_URL}/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.appsecret
        }
        self.logger.info(f"wechat.token: request begin appid={self.appid}")
        async with httpx.AsyncClient(verify=self.verify) as client:
            response = await client.get(url, params=params)
            data = response.json()
        self.logger.info(f"wechat.token: response errcode={data.get('errcode')} expires_in={data.get('expires_in')}")
        if "errcode" in data and data["errcode"] != 0:
            raise WeChatAPIError(data["errcode"], data.get("errmsg", "未知错误"))
        token = data.get("access_token")
        expires_in = int(data.get("expires_in", 7200))
        expire_at_dt = datetime.utcnow() + timedelta(seconds=max(expires_in - 120, 300))

        # 3. 写缓存
        try:
            with SessionLocal() as db:
                upsert_token(db, self.appid, token, expire_at_dt)
            self.logger.info("wechat.token: cached to db successfully")
        except Exception:
            self.logger.warning("wechat.token: cache to db failed, continue without db cache")

        return token

    async def get_wxacode_unlimit(self, scene: str, page: str, width: int = 430) -> bytes:
        """
        获取小程序码（无限制）

        文档：https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/qrcode-link/qr-code/getUnlimitedQRCode.html

        Args:
            scene: 自定义场景值（不超过32个可见字符）
            page: 小程序页面路径，如 "pages/family/join"
            width: 图片宽度，默认 430

        Returns:
            PNG 二进制内容
        """
        access_token = await self._get_access_token()
        url = f"{self.BASE_URL}/wxa/getwxacodeunlimit?access_token={access_token}"
        payload = {
            "scene": scene,
            "page": page,
            "width": width,
            "check_path": False
        }
        self.logger.info(f"wechat.qrcode: request scene={scene} page={page}")
        async with httpx.AsyncClient(verify=self.verify) as client:
            resp = await client.post(url, json=payload)
            content_type = resp.headers.get("Content-Type", "")
            if content_type.startswith("image/"):
                self.logger.info("wechat.qrcode: success image returned")
                return resp.content
            data = resp.json()
        self.logger.error(f"wechat.qrcode: error errcode={data.get('errcode')} errmsg={data.get('errmsg')}")
        raise WeChatAPIError(data.get("errcode", -1), data.get("errmsg", "获取小程序码失败"))

    async def send_subscribe_message(self, openid: str, template_id: str, page: str, data: Dict, miniprogram_state: str = "formal") -> bool:
        """
        发送订阅消息
        
        Args:
            openid: 接收者（用户）的 openid
            template_id: 所需下发的订阅消息的id
            page: 点击模板卡片后的跳转页面，仅限本小程序内的页面
            data: 模板内容，格式形如 { "key1": { "value": any }, "key2": { "value": any } }
            miniprogram_state: 跳转小程序类型：developer为开发版；trial为体验版；formal为正式版；默认为正式版
            
        Returns:
            True: 发送成功
            False: 发送失败
        """
        access_token = await self._get_access_token()
        url = f"{self.BASE_URL}/cgi-bin/message/subscribe/send?access_token={access_token}"
        
        payload = {
            "touser": openid,
            "template_id": template_id,
            "page": page,
            "data": data,
            "miniprogram_state": miniprogram_state,
            "lang": "zh_CN"
        }
        
        self.logger.info(f"wechat.subscribe_msg: request openid={openid} template_id={template_id}")
        async with httpx.AsyncClient(verify=self.verify) as client:
            resp = await client.post(url, json=payload)
            result = resp.json()
            
        self.logger.info(f"wechat.subscribe_msg: response errcode={result.get('errcode')} errmsg={result.get('errmsg')}")
        
        if result.get("errcode") == 0:
            return True
        
        self.logger.error(f"wechat.subscribe_msg: failed errcode={result.get('errcode')} errmsg={result.get('errmsg')}")
        return False


# 创建全局实例
_WX_API_INSTANCE: Optional[WeChatAPI] = None


def get_wechat_api() -> WeChatAPI:
    if _WX_API_INSTANCE is None:
        # 创建单例实例，复用内部配置与缓存逻辑
        globals()["_WX_API_INSTANCE"] = WeChatAPI()
    return _WX_API_INSTANCE
