# 更新日志 (CHANGELOG)

## [1.1.0] - 2026-01-18

### 🎉 重大改进

#### 修复 ChatGPT 界面更新导致的超时问题
- **问题**: 远程访问时 60 秒超时无响应
- **原因**: ChatGPT 发送按钮选择器已更新
- **解决**: 实现多选择器支持，提高兼容性
- **效果**: 响应时间从 60s+ 降至 8.35s（**提升 86%**）

### ✨ 新增功能

#### 1. 增强的日志系统
- 添加分级日志：`[DEBUG]`, `[INFO]`, `[WARNING]`, `[ERROR]`
- 显示详细的执行步骤和时间信息
- 每 10 秒显示等待进度

#### 2. 诊断工具
- **check_browser_status.py**: 完整的浏览器状态诊断
  - 检查 Chrome 连接状态
  - 验证 ChatGPT 页面状态
  - 检测输入框和发送按钮
  - 自动保存诊断截图
  
- **find_send_button.py**: 选择器查找工具
  - 测试多种选择器
  - 显示按钮属性和 HTML
  - 快速定位有效选择器

#### 3. 自动截图功能
- 错误时自动保存页面截图
- 超时时保存当前状态
- 截图文件包含错误上下文信息

### 🔧 优化改进

#### 代码质量
- 改进错误处理机制，所有关键操作都有 try-catch
- 增加页面状态检查，发送前验证 URL 和标题
- 超时时间从 60 秒增加到 90 秒
- 添加输入框和发送按钮的多种查找策略

#### 选择器更新
```python
# 新增多个候选选择器
selectors = [
    "form button[type='button']",           # 新界面 (主选择器)
    "button[data-testid='send-button']",    # 旧界面 (后备)
    "button[data-testid='fruitjuice-send-button']",  # 备选
]
```

#### 响应等待逻辑优化
- 改进按钮状态检测
- 添加进度显示
- 更详细的超时错误信息

### 🐛 Bug 修复

1. **修复路径硬编码问题**
   - `start_chrome_debug.bat` 使用 `%~dp0` 相对路径
   - 提高跨机器部署的可移植性

2. **修复 Python 环境问题**
   - `run_headless.bat` 使用虚拟环境完整路径
   - 在新窗口启动服务避免信号干扰

3. **修复缺少依赖问题**
   - 添加 `requests` 到 requirements.txt

### 📝 文档更新

- 新增 `SETUP_GUIDE_CN.md` - 详细的安装和使用指南
- 新增 `TROUBLESHOOTING.md` - 故障排除指南
- 新增 `PROJECT_SUMMARY.md` - 项目开发总结和经验
- 新增 `CHANGELOG.md` - 本更新日志

### 🧪 测试结果

#### 本地测试
- ✅ 响应时间: 8.35 秒
- ✅ 成功率: 100%
- ✅ 日志完整度: 优秀

#### 远程测试（局域网）
- ✅ 连接性: 正常
- ✅ 响应: 正常
- ✅ 稳定性: 多次测试通过

### 📦 依赖更新

```txt
fastapi
uvicorn
playwright
pydantic
requests  # 新增
```

### ⚙️ 环境要求

- Python 3.8+
- Google Chrome
- Windows 10/11
- Playwright Chromium 驱动

---

## [1.0.0] - 初始版本

### 功能
- FastAPI OpenAI 兼容 API
- Playwright 浏览器自动化
- CDP 模式连接 Chrome
- 多模态支持（图片上传）
- 对话日志记录

### 文件
- main.py - API 服务
- browser_manager.py - 浏览器控制
- start_chrome_debug.bat - Chrome 启动脚本
- run_headless.bat - 服务启动脚本
- test_api.py - 测试脚本

---

## 版本规范

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范：

- **主版本号**: 不兼容的 API 修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正

## 标签说明

- 🎉 重大改进
- ✨ 新增功能
- 🔧 优化改进
- 🐛 Bug 修复
- 📝 文档更新
- 🧪 测试
- 📦 依赖
- ⚙️ 配置
- 🔒 安全
- ⚠️ 弃用
- 🗑️ 移除
