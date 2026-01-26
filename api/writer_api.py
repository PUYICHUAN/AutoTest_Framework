import time # 必须导入 time 模块
from common.rest_client import RestClient
from config.settings import BASE_URL, LOGIN_PAYLOAD

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

    # --- 核心修复：添加这个方法定义 ---
    def _refresh_security_headers(self):
        """
        内部工具方法：用于在每次请求前生成最新的 13 位时间戳
        """
        current_ts = str(int(time.time() * 1000))
        self.update_header({"timestamp": current_ts})
    # -------------------------------

    def login(self):
        """登录接口"""
        self._refresh_security_headers() # 现在调用就不会报错了
        path = "/ccauthorweb/pc/login/auth"
        return self.request("POST", path, json=LOGIN_PAYLOAD)

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