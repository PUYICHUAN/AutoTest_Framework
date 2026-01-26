import yaml
import os


def read_yaml(file_name):
    """
    读取 data 文件夹下的 yaml 文件
    """
    # 获取项目根目录的绝对路径
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, "data", file_name)

    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data