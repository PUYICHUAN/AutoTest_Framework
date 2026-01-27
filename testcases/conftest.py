import pytest
import re
import json
from api.writer_api import WriterApi
from config import settings


@pytest.fixture(scope="session", autouse=True)
def auto_refresh_login():
    """
    在所有测试开始前自动刷新登录凭证
    scope="session" 表示整个测试会话只执行一次
    autouse=True 表示自动使用，不需要在测试中显式声明
    """
    print("\n" + "="*60)
    print("🔄 开始自动刷新登录凭证...")
    print("="*60)
    
    writer = WriterApi()
    
    # 调用 ptlogin 获取最新凭证（UAT 环境）
    username = "testpuyc3"
    password = "624510103681a9ea78e10a472a087a017b1fe5873d6547ceca25acb3023b43342c336c0a6da0ce452b20ebe98450e1262c2e878d8f0c1be2bd5ca7a47dd8ceb105fa9121ac56c0eb40d8601e14e0747f26dd1e6cded1ff851d3893113312309bac6ffcf2d8cc87ed70a83cc9147720b2a53bb463417b13a8ad77c96a2780324b"
    
    try:
        res = writer.ptlogin_login(username=username, password=password)
        
        if res.status_code == 200:
            # 从 JSONP 响应中提取 JSON 数据
            match = re.search(r'\((.+)\)$', res.text)
            if match:
                json_str = match.group(1)
                data = json.loads(json_str)
                
                # 检查登录是否成功
                if data.get('code') == 0 or data.get('returnCode') == 0:
                    login_data = data.get('data', {})
                    
                    # 提取登录凭证
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
                        
                        print("✅ 登录凭证刷新成功！")
                        print(f"   ywGuid: {yw_guid}")
                        print(f"   ywKey: {yw_key}")
                        print(f"   ticket: {ticket}")
                        print("="*60 + "\n")
                    else:
                        print("⚠️ 警告：响应中未找到完整的登录凭证")
                        print(f"   响应数据: {login_data}")
                else:
                    print(f"❌ 登录失败，code: {data.get('code') or data.get('returnCode')}")
                    print(f"   响应: {data}")
            else:
                print("❌ 无法解析 JSONP 响应")
                print(f"   响应内容: {res.text[:200]}...")
        else:
            print(f"❌ 请求失败，状态码: {res.status_code}")
    except Exception as e:
        print(f"❌ 刷新登录凭证时出错: {str(e)}")
        print("   将使用配置文件中的默认凭证")
    
    # yield 之前的代码在测试开始前执行
    yield
    # yield 之后的代码在测试结束后执行（如果需要清理）
    print("\n" + "="*60)
    print("🏁 所有测试执行完毕")
    print("="*60)