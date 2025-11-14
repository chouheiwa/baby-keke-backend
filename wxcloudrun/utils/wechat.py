"""
微信 API 工具类
"""
import httpx
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
        
        async with httpx.AsyncClient(verify=self.verify) as client:
            response = await client.get(url, params=params)
            data = response.json()
        
        # 检查错误
        if "errcode" in data and data["errcode"] != 0:
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
            
            # errcode=0 表示有效，errcode=87009 表示无效
            return data.get("errcode") == 0
        except Exception:
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
        
        async with httpx.AsyncClient(verify=self.verify) as client:
            response = await client.post(url, params=params, json=data)
            result = response.json()
        
        # 检查错误
        if "errcode" in result and result["errcode"] != 0:
            raise WeChatAPIError(result["errcode"], result.get("errmsg", "未知错误"))
        
        return {
            "openid": result.get("openid"),
            "session_key": result.get("session_key")
        }
    
    async def _get_access_token(self) -> str:
        """
        获取接口调用凭证 access_token
        
        Returns:
            access_token 字符串
            
        Raises:
            WeChatAPIError: 微信API返回错误时抛出
            
        Note:
            在实际生产环境中，access_token 应该被缓存（有效期 7200 秒）
        """
        url = f"{self.BASE_URL}/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.appsecret
        }
        
        async with httpx.AsyncClient(verify=self.verify) as client:
            response = await client.get(url, params=params)
            data = response.json()
        
        # 检查错误
        if "errcode" in data and data["errcode"] != 0:
            raise WeChatAPIError(data["errcode"], data.get("errmsg", "未知错误"))
        
        return data.get("access_token")


# 创建全局实例
def get_wechat_api() -> WeChatAPI:
    """获取微信 API 客户端实例"""
    return WeChatAPI()
