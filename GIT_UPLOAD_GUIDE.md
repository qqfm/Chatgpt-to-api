# GitHub 上传指南

## 1. 准备工作
确保你拥有一个 GitHub 账号，并登录。

## 2.在 GitHub 创建仓库
1. 访问 [Create New Repository](https://github.com/new).
2. **Repository name**: 输入 `webgpt`。
3. **Visibility**: 选择 **Private** (推荐，保护隐私)。
4. **不要勾选** "Add a README" 或 ".gitignore"。
5. 点击 **Create repository**。

## 3. 连接并上传
复制你新仓库的 HTTPS 地址 (例如 `https://github.com/username/webgpt.git`)。

在 VS Code 终端中运行以下命令：

```powershell
# 替换为你的真实地址
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 切换主分支名
git branch -M main

# 推送
git push -u origin main
```

## 4. 常见问题

- **登录弹窗**: 推送时如果弹出 GitHub 登录窗口，请点击 "Sign in with browser" 并授权。
- **Permission denied**: 确保你是仓库的拥有者。
- **Remote origin already exists**: 如果提示这个错误，说明之前关联过，运行 `git remote remove origin` 先删除旧的，再重新 add。

## 5. 日常更新代码
当你修改了代码后，运行：

```powershell
git add .
git commit -m "更新说明"
git push
```
