def    print(LOGIN_PAYLOAD):
    pass的 `LOGIN_PAYLOAD`（包含 ywGuid、ywKey、ticket）会过期，导致测试失败。

## 解决方案

### 1. 自动刷新机制（推荐）✅
通过 `conftest.py` 中的 `auto_refresh_login` fixture 实现：
- **执行时机**：所有测试开始前自动执行
- **执行频率**：每次运行 pytest 时执行一次（session 级别）
- **工作流程**：
  1. 调用 `ptlogin_login()` 获取最新登录凭证
  2. 从 JSONP 响应中解析出 ywGuid、ywKey、ticket
  3. 动态更新 `settings.LOGIN_PAYLOAD`
  4. 后续所有测试使用最新的凭证

### 2. 手动刷新（备用方案）
运行 `test_ptlogin.py` 中的测试用例，会在测试过程中更新凭证：
```bash
pytest testcases/test_ptlogin.py::TestPtlogin::test_ptlogin_login -v
```

## 使用方法

### 正常运行测试
```bash
# 方式1：使用 run.py
python3 run.py

# 方式2：直接使用 pytest
pytest testcases/ -v

# 方式3：运行特定测试
pytest testcases/test_writer_ai.py -v
```

**无需任何额外操作**，`conftest.py` 会自动在测试前刷新登录凭证！

## 文件说明

### 1. `testcases/conftest.py`
- 包含 `auto_refresh_login` fixture
- 自动在所有测试前执行
- 负责刷新登录凭证

### 2. `testcases/test_ptlogin.py`
- 包含 ptlogin 登录接口的测试用例
- 可以手动运行来测试登录功能
- 也会更新登录凭证（但主要用于测试）

### 3. `api/writer_api.py`
- `login()` 方法：使用 `settings.LOGIN_PAYLOAD` 进行登录
- `ptlogin_login()` 方法：获取新的登录凭证

### 4. `config/settings.py`
- 存储 `LOGIN_PAYLOAD`（会被动态更新）

## 工作流程图

```
开始运行测试
    ↓
conftest.py 自动执行
    ↓
调用 ptlogin_login() 获取新凭证
    ↓
解析响应，提取 ywGuid/ywKey/ticket
    ↓
更新 settings.LOGIN_PAYLOAD
    ↓
执行所有测试用例（使用最新凭证）
    ↓
测试完成
```

## 注意事项

1. **用户名密码**：目前硬编码在 `conftest.py` 中，如需修改请编辑该文件
2. **响应格式**：假设 ptlogin 返回的 JSONP 格式为 `callback({"code":0,"data":{...}})`
3. **错误处理**：如果刷新失败，会使用 `settings.py` 中的默认凭证
4. **日志输出**：刷新过程会在控制台输出详细日志

## 调试

如果登录仍然失败，请检查：

1. **查看刷新日志**：
   ```bash
   pytest testcases/ -v -s
   ```
   `-s` 参数会显示 print 输出

2. **手动测试 ptlogin**：
   ```bash
   pytest testcases/test_ptlogin.py::TestPtlogin::test_ptlogin_login -v -s
   ```

3. **检查响应格式**：
   查看 ptlogin 的实际响应，确认字段名称是否正确

4. **验证凭证是否更新**：
   在测试中添加打印：
   ```python
   from config import settings
   print(settings.LOGIN_PAYLOAD)
   ```
