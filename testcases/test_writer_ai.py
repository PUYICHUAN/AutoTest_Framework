import pytest
import allure
from api.writer_api import WriterApi
from common.yaml_handler import read_yaml


@allure.feature("创作中心自动化测试")
class TestWriter:

    def setup_class(self):
        self.writer = WriterApi()
        self.writer.login()

    # --- 用例 1：自定义词库 ---
    @allure.story("词库业务")
    def test_get_word_list_flow(self):
        res = self.writer.get_customize_word_list()
        assert str(res.json().get("code") or res.json().get("returnCode")) == "2000"

    # --- 用例 2：拼写检查首页 (确保有这个函数) ---
    @allure.story("拼字业务")
    # 如果你用了 YAML，确保 read_yaml 路径和 key 正确
    @pytest.mark.parametrize("case_data", read_yaml("spelling_data.yaml")["test_get_home_list"])
    def test_get_spelling_home_list(self, case_data):
        allure.dynamic.title(case_data["case_name"])
        res = self.writer.get_spelling_home_list(
            page_no=case_data["pageNo"],
            page_size=case_data["pageSize"],
            filter_type=case_data["filterType"]
        )
        assert str(res.json().get("code") or res.json().get("returnCode")) == "2000"