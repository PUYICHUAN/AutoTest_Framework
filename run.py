# run.py
import os
import pytest
import shutil

if __name__ == '__main__':
    # 1. 定义结果路径
    results_path = "./reports/allure-results"
    report_path = "./reports/allure-report"

    # 2. 清理掉旧的测试结果（可选）
    # 这样可以保证每次报告都是全新的，不会看到旧数据
    if os.path.exists(results_path):
        shutil.rmtree(results_path)

    # 3. 运行 Pytest
    # -s: 打印 print 内容
    # -v: 详细模式
    # --alluredir: 指定结果存放路径
    print("🚀 开始执行自动化测试...")
    pytest.main(["-s", "-v", "testcases/test_writer_ai.py", f"--alluredir={results_path}"])

    # 4. 生成可视化报告
    # --clean: 生成前清理旧报告目录
    print("📊 正在生成可视化报告...")
    os.system(f"allure generate {results_path} -o {report_path} --clean")

    # 5. 自动打开报告（关键一步）
    print("🌐 正在自动打开浏览器查看报告...")
    # 'allure open' 会启动一个本地服务并自动打开默认浏览器
    os.system(f"allure open {report_path}")