import requests
import json
import urllib3
import allure

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RestClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def update_header(self, header_dict):
        """
        定义这个方法，用于更新全局请求头
        """
        self.session.headers.update(header_dict)

    def request(self, method, url, **kwargs):
        full_url = self.base_url + url

        # 资深测开技巧：让请求也可以走 Charles 代理，方便对比
        # 如果你想在 Charles 看 Python 的请求，取消下面两行的注释
        # proxies = {"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888"}
        # kwargs["proxies"] = proxies

        with allure.step(f"发送 {method} 请求: {url}"):
            response = self.session.request(method, full_url, verify=False, **kwargs)

            print(f"\n{'=' * 60}\n【请求地址】: {method} {full_url}")
            if kwargs.get("json"):
                print(f"【请求体】  : {json.dumps(kwargs['json'], indent=4, ensure_ascii=False)}")

            print(f"【状态码】  : {response.status_code}")

            try:
                res_json = response.json()
                print(f"【响应正文】: \n{json.dumps(res_json, indent=4, ensure_ascii=False)}")
                allure.attach(json.dumps(res_json, indent=4, ensure_ascii=False), "接口响应",
                              allure.attachment_type.JSON)
            except:
                print(f"【响应正文】: {response.text}")

            return response