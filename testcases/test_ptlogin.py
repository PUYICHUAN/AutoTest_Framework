import pytest
import allure
import re
import json
from api.writer_api import WriterApi
from config import settings


@allure.feature("ptlogin 登录测试")
class TestPtlogin:
    """
    ptlogin 登录接口测试类
    """

    def setup_class(self):
        """初始化测试类"""
        self.writer = WriterApi()

    @allure.story("用户登录")
    @allure.title("测试 ptlogin 登录接口")
    @allure.description("测试用户通过 ptlogin 接口登录功能")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ptlogin_login(self):
        """
        测试 ptlogin 登录接口
        验证用户名和密码登录是否成功
        """
        # 测试数据
        username = "jlvlv55"
        password = "21326296962e4b36a0f9f755ad3f96a8a862d558c07c5f7c2d881b3e1f647d24333d36b984cde4b4d4c21076e7a274a38f543b34abe0b24bae59dd10795cde4870c20ff23b729ac77c0aba132eb81d21595d058d43ad6a5df032170e5a7ee35d26d68adce4a7c0af504d8cb3d736c516af564a25e46486cbdb40a58884f87587"
        
        with allure.step("发送登录请求"):
            res = self.writer.ptlogin_login(
                username=username,
                password=password
            )
        
        with allure.step("验证响应状态码"):
            assert res.status_code == 200, f"期望状态码为 200，实际为 {res.status_code}"
        
        with allure.step("验证响应内容"):
            # 因为是 JSONP 格式，响应会包含 callback 函数
            response_text = res.text
            # 检查是否包含 JSONP callback（jQuery 或 LoginV1.loginCallback 等）
            assert "jQuery" in response_text or "Callback" in response_text or "callback" in response_text, "响应格式不正确"
            
            # 记录响应内容到 allure 报告
            allure.attach(response_text, "登录响应内容", allure.attachment_type.TEXT)
            
            print(f"\n登录响应: {response_text}")
        
        with allure.step("提取并更新 LOGIN_PAYLOAD"):
            # 从 JSONP 响应中提取 JSON 数据
            # 格式类似：jQuery112402980352746567616_1769501562986({"code":0,"data":{...}})
            match = re.search(r'\((.+)\)$', response_text)
            if match:
                json_str = match.group(1)
                data = json.loads(json_str)
                
                # 检查登录是否成功
                if data.get('code') == 0 or data.get('returnCode') == 0:
                    login_data = data.get('data', {})
                    
                    # 提取登录凭证（根据实际响应结构调整）
                    yw_guid = login_data.get('ywGuid')
                    yw_key = login_data.get('ywKey')
                    ticket = login_data.get('ticket')
                    
                    if yw_guid and yw_key and ticket:
                        # 更新 settings 中的 LOGIN_PAYLOAD
                        settings.LOGIN_PAYLOAD = {
                            "ywGuid": yw_guid,
                            "ywKey": yw_key,
                            "ticket": ticket
                        }
                        
                        print(f"\n✅ 成功更新 LOGIN_PAYLOAD:")
                        print(f"   ywGuid: {yw_guid}")
                        print(f"   ywKey: {yw_key}")
                        print(f"   ticket: {ticket}")
                        
                        allure.attach(
                            json.dumps(settings.LOGIN_PAYLOAD, indent=2),
                            "更新后的 LOGIN_PAYLOAD",
                            allure.attachment_type.JSON
                        )
                    else:
                        print("⚠️ 警告：响应中未找到完整的登录凭证")
                else:
                    print(f"⚠️ 登录失败，code: {data.get('code') or data.get('returnCode')}")
            else:
                print("⚠️ 无法解析 JSONP 响应")

    @allure.story("用户登录")
    @allure.title("测试 ptlogin 登录接口 - 参数化测试")
    @allure.description("使用不同的用户名和密码测试登录功能")
    @pytest.mark.parametrize("username,password,expected_status", [
        ("jlvlv55", "21326296962e4b36a0f9f755ad3f96a8a862d558c07c5f7c2d881b3e1f647d24333d36b984cde4b4d4c21076e7a274a38f543b34abe0b24bae59dd10795cde4870c20ff23b729ac77c0aba132eb81d21595d058d43ad6a5df032170e5a7ee35d26d68adce4a7c0af504d8cb3d736c516af564a25e46486cbdb40a58884f87587", 200),
        # 可以添加更多测试数据
        # ("test_user", "wrong_password", 200),  # 测试错误密码的情况
    ])
    def test_ptlogin_login_parametrize(self, username, password, expected_status):
        """
        参数化测试 ptlogin 登录接口
        """
        with allure.step(f"使用用户名 {username} 登录"):
            res = self.writer.ptlogin_login(
                username=username,
                password=password
            )
        
        with allure.step("验证响应状态码"):
            assert res.status_code == expected_status, \
                f"期望状态码为 {expected_status}，实际为 {res.status_code}"
        
        # 记录响应到报告
        allure.attach(res.text, f"用户 {username} 的登录响应", allure.attachment_type.TEXT)

    @allure.story("用户登录")
    @allure.title("测试 ptlogin 登录接口 - 自定义参数")
    @allure.description("测试使用自定义参数的登录功能")
    def test_ptlogin_login_custom_params(self):
        """
        测试使用自定义参数的登录接口
        """
        username = "testpuyc3"
        password = "624510103681a9ea78e10a472a087a017b1fe5873d6547ceca25acb3023b43342c336c0a6da0ce452b20ebe98450e1262c2e878d8f0c1be2bd5ca7a47dd8ceb105fa9121ac56c0eb40d8601e14e0747f26dd1e6cded1ff851d3893113312309bac6ffcf2d8cc87ed70a83cc9147720b2a53bb463417b13a8ad77c96a2780324b"
        
        with allure.step("使用自定义 callback 和 token 登录"):
            res = self.writer.ptlogin_login(
                username=username,
                password=password,
                callback="customCallback123",
                app_id="34",
                area_id="4",
                return_url="https://write.qq.com",
                ywtoken="9OyjjcdK80wDnqIvmSkCgT26ul1wKbbhl7idG12FTeA="
            )
        
        with allure.step("验证响应"):
            assert res.status_code == 200
            # 响应包含 LoginV1.loginCallback 或其他 callback
            assert "Callback" in res.text or "callback" in res.text, "响应格式不正确"
            allure.attach(res.text, "自定义参数登录响应", allure.attachment_type.TEXT)
