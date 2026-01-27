import time # 必须导入 time 模块
from common.rest_client import RestClient
from config import settings
from config.settings import BASE_URL

class WriterApi(RestClient):
    def __init__(self):
        super().__init__(BASE_URL)
        # 初始化基础仿真 Header
        self.update_header({
            "ptfrom": "authorwrite",
            "version": "5.12.0",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "referer": "https://pcwrite.yuewen.com/",
            "d1": "oueB3UP4BS5fMPWB1AYBRUm7mhVEpEl2HubDiZPRH98="
        })


    def _refresh_security_headers(self):
        """
        内部工具方法：用于在每次请求前生成最新的 13 位时间戳
        """
        current_ts = str(int(time.time() * 1000))
        self.update_header({"timestamp": current_ts})
    # -------------------------------

    def login(self):
        """登录接口 - 使用动态获取的最新登录凭证"""
        self._refresh_security_headers()
        path = "/ccauthorweb/pc/login/auth"
        # 动态获取最新的 LOGIN_PAYLOAD，而不是使用导入时的静态值
        return self.request("POST", path, json=settings.LOGIN_PAYLOAD)

    def get_customize_word_list(self):
        """接口1"""
        self._refresh_security_headers()
        path = "/writeraiapiserver/desk/customize/content/check/getCustomizeWordList"
        return self.request("GET", path)

    def get_spelling_home_list(self, page_no=1, page_size=10, filter_type=4):
        """接口2：新增的接口"""
        self._refresh_security_headers() # 调用刷新时间戳
        path = "/ccauthorweb/desk/spelling/getHomeList"
        params = {
            "pageNo": page_no,
            "pageSize": page_size,
            "filterType": filter_type
        }
        return self.request("GET", path, params=params)
    def create_novel(self, title="哈哈", coverurl="https://ccstatic-1252317822.file.myqcloud.com/ccstatic/writer/cover/cover_draft2.png", delivertype="1"):
        self._refresh_security_headers()
        path = '/ccauthorweb/desk/contbook/createNovel'
        params = {
            "Title": title,
            "CoverUrl": coverurl,
            "DeliverType": delivertype
        }
        return self.request("POST", path, params=params)

    def ptlogin_login(self, username, password, callback="jQuery112402980352746567616_1769501562986",
                      app_id="34", area_id="4", return_url="https://write.qq.com", 
                      ywtoken="9OyjjcdK80wDnqIvmSkCgRA76ngecyMn+yWrHsfugpQ="):
        """
        ptlogin 登录接口（UAT 环境）
        :param username: 用户名
        :param password: 加密后的密码
        :param callback: JSONP 回调函数名
        :param app_id: 应用ID
        :param area_id: 区域ID
        :param return_url: 登录成功后的返回URL
        :param ywtoken: token
        :return: 响应对象
        """
        # 设置特定的请求头（UAT 环境）
        headers = {
            "Host": "oaptlogin.yuewen.com",
            "Accept": "*/*",
            "Accept-Language": "zh-CN",
            "Referer": "https://oaptlogin.yuewen.com",
            "Sec-Fetch-Dest": "script",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Storage-Access": "active",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) authorwriteuat/5.13.0 Chrome/134.0.6998.205 Electron/35.7.0 Safari/537.36",
            "sec-ch-ua": "\"Not:A-Brand\";v=\"24\", \"Chromium\";v=\"134\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\""
        }
        
        # 设置 Cookie（UAT 环境）
        cookies = {
            "serial": "iX1FQLHlcARjin8QG02Wmm5NyTVQUTmSdgn/dZRONps=",
            "serialStr": "3e:1f:c5:35:16:46",
            "devicename": "authorwriteuat/5.13.0",
            "devicetype": "mac",
            "newstatisticUUID": "1769157889_416245081",
            "wal": "1",
            "ywbackurl_34": "https://write.qq.com",
            "ywtab": "qidian",
            "newstatisticSID": "1769501563_1447193381"
        }
        
        # 构建请求参数
        current_ts = str(int(time.time() * 1000))
        params = {
            "callback": callback,
            "appId": app_id,
            "areaId": area_id,
            "source": "",
            "returnurl": return_url,
            "version": "",
            "imei": "",
            "qimei": "",
            "target": "callback",
            "ticket": "1",
            "autotime": "60",
            "jumpdm": "yuewen",
            "ajaxdm": "yuewen",
            "auto": "0",
            "sdkversion": "",
            "ywtoken": ywtoken,
            "username": username,
            "password": password,
            "code": "",
            "method": "LoginV1.loginCallback",
            "sessionkey": "",
            "format": "jsonp",
            "_": current_ts
        }
        
        # 临时更新 session 的 headers 和 cookies
        self.session.headers.update(headers)
        self.session.cookies.update(cookies)
        
        # 发送请求（使用完整 URL，因为这是不同的域名 - UAT 环境）
        full_url = "https://oaptlogin.yuewen.com/login/login"
        response = self.session.request("GET", full_url, params=params, verify=False)
        
        return response