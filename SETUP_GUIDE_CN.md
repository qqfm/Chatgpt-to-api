# WebGPT 安装和测试指南

## 📋 已解决的问题

在测试过程中发现并修复了以下问题：

### 1. 路径配置问题
**问题**：`start_chrome_debug.bat` 中硬编码了 `d:\webgpt\chrome_profile` 路径
**解决**：改为使用 `%~dp0chrome_profile`（脚本所在目录的相对路径）

### 2. Python 虚拟环境问题
**问题**：批处理脚本直接使用 `python` 命令，可能找不到正确的 Python 环境
**解决**：使用完整路径 `C:\GPTAPI\.venv\Scripts\python.exe`

### 3. Playwright 驱动未安装
**问题**：Playwright 浏览器驱动未安装，导致连接失败
**解决**：运行 `playwright install chromium --with-deps`

### 4. 缺少 requests 依赖
**问题**：测试脚本需要 requests 模块，但未在 requirements.txt 中声明
**解决**：添加 `requests` 到 requirements.txt

### 5. 服务启动方式问题
**问题**：在同一终端中启动服务容易受到信号干扰导致自动关闭
**解决**：修改 `run_headless.bat` 在新窗口启动服务

## 🚀 安装步骤

### 1. 安装 Python 依赖
```bash
cd C:\GPTAPI\Chatgpt-to-api-main
pip install -r requirements.txt
```

### 2. 安装 Playwright 浏览器驱动
```bash
C:\GPTAPI\.venv\Scripts\playwright.exe install chromium --with-deps
```

## ▶️ 使用步骤

### 第一步：启动 Chrome 调试模式
双击运行 `start_chrome_debug.bat`
- 会打开一个 Chrome 窗口（端口 9222）
- **首次使用请在此窗口手动登录 ChatGPT**
- **保持此窗口开启**（可以最小化）

### 第二步：启动 API 服务
双击运行 `run_headless.bat`
- 会在新窗口启动 FastAPI 服务
- 等待看到 "Uvicorn running on http://0.0.0.0:8000"
- **保持此窗口开启**

### 第三步：测试 API
在新的命令行窗口运行：
```bash
cd C:\GPTAPI\Chatgpt-to-api-main
C:\GPTAPI\.venv\Scripts\python.exe test_api.py
```

预期输出：
```
✅ Success! Response received in XX.XXs:
--------------------------------------------------
Service is working!
--------------------------------------------------
```

## 🔍 验证清单

- [ ] Chrome 在端口 9222 运行（`netstat -ano | findstr ":9222"`）
- [ ] API 服务在端口 8000 运行（`netstat -ano | findstr ":8000"`）
- [ ] 测试脚本返回成功响应
- [ ] ChatGPT 网页已登录

## ⚠️ 常见问题

### Q: 服务启动后立即关闭
**A**: 使用 `run_headless.bat` 在新窗口启动，避免在同一终端中运行

### Q: 连接 Chrome 失败
**A**: 确保先运行 `start_chrome_debug.bat` 并保持窗口开启

### Q: Playwright 驱动错误
**A**: 运行 `C:\GPTAPI\.venv\Scripts\playwright.exe install chromium --with-deps`

### Q: 测试响应缓慢（60+ 秒）
**A**: 这是正常的，因为需要等待 ChatGPT 网页生成完整响应

## 📁 项目文件说明

- `start_chrome_debug.bat` - 启动 Chrome 调试模式（修复了路径问题）
- `run_headless.bat` - 启动 API 服务（在新窗口，避免信号干扰）
- `main.py` - FastAPI 服务主程序
- `browser_manager.py` - Playwright 浏览器控制器
- `test_api.py` - API 功能测试脚本
- `requirements.txt` - Python 依赖列表（已添加 requests）

## ✅ 测试结果

测试日期：2026-01-18
- ✅ Chrome 调试模式启动成功
- ✅ API 服务连接 Chrome 成功
- ✅ API 端点响应正常
- ✅ ChatGPT 消息发送和接收成功
- ✅ 响应时间：约 68 秒（正常范围）

所有功能测试通过！🎉
