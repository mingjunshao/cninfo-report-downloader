# 上传到 GitHub 指南

本指南将帮助您将 cninfo-report-downloader 技能上传到 GitHub。

## 步骤 1：在 GitHub 上创建新仓库

1. 登录您的 GitHub 账号
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: cninfo-report-downloader
   - **Description**: 从巨潮网站下载指定公司、指定年份的年报和季度报告
   - **Visibility**: 选择 "Public" 或 "Private"
4. 点击 "Create repository"

## 步骤 2：初始化本地 Git 仓库

在 `cninfo-report-downloader` 目录中执行以下命令：

```bash
# 初始化 Git 仓库
git init

# 添加文件
git add .

# 提交初始版本
git commit -m "Initial commit: 巨潮报告下载器技能"
```

## 步骤 3：关联远程仓库并推送

1. 复制 GitHub 仓库的 HTTPS 或 SSH 链接
2. 执行以下命令：

```bash
# 添加远程仓库
git remote add origin https://github.com/yourusername/cninfo-report-downloader.git

# 推送代码到 GitHub
git push -u origin main
```

## 步骤 4：验证上传

1. 打开 GitHub 仓库页面
2. 确认所有文件已成功上传
3. 检查 README.md 是否正确显示

## 步骤 5：配置 GitHub Actions（可选）

如果您希望自动构建和发布包，可以配置 GitHub Actions。创建以下文件：

```yaml
# .github/workflows/python-publish.yml
name: Publish Python Package

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

## 注意事项

- 确保 `.gitignore` 文件已正确配置，避免上传不必要的文件
- 替换命令中的 `yourusername` 为您的 GitHub 用户名
- 如果使用 SSH 链接，确保您的 SSH 密钥已添加到 GitHub 账号
- 对于 PyPI 发布，需要在 GitHub Secrets 中添加 `PYPI_API_TOKEN`

## 后续维护

- 定期更新代码以适应巨潮网站的变化
- 响应用户反馈和 bug 报告
- 保持依赖项的更新
