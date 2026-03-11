# 巨潮报告下载器 (cninfo-report-downloader)

从巨潮资讯网(www.cninfo.com.cn)下载指定公司、指定年份的年报和季度报告。

## 功能特点

- 支持下载指定公司的年报
- 支持下载指定公司的季度报告
- 自动搜索公司信息
- 优先下载完整版本的报告
- 支持命令行使用

## 安装

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/cninfo-report-downloader.git
cd cninfo-report-downloader

# 安装
pip install -e .
```

### 直接安装

```bash
pip install cninfo-report-downloader
```

## 使用方法

### 命令行使用

#### 下载年报

```bash
cninfo-download 公司名称 年份 annual
```

**示例**：
```bash
# 下载贵州茅台2023年的年报
cninfo-download 贵州茅台 2023 annual

# 使用股票代码下载
cninfo-download 600519 2023 annual
```

#### 下载季度报告

```bash
cninfo-download 公司名称 年份 quarterly --quarter 季度
```

**示例**：
```bash
# 下载东吴证券2023年第一季度的报告
cninfo-download 东吴证券 2023 quarterly --quarter 1

# 下载半年度报告
cninfo-download 东吴证券 2023 quarterly --quarter 2

# 下载第三季度报告
cninfo-download 东吴证券 2023 quarterly --quarter 3
```

### Python API 使用

```python
from cninfo_report_downloader import CNInfoReportDownloader

# 创建下载器实例
downloader = CNInfoReportDownloader()

# 搜索公司信息
company_info = downloader.search_company("贵州茅台")

# 下载年报
downloader.download_report(company_info, 2023, "annual")

# 下载季度报告
downloader.download_report(company_info, 2023, "quarterly", "1")
```

## 依赖

- Python 3.6+
- requests >= 2.32.0
- beautifulsoup4 >= 4.14.0

## 注意事项

1. 巨潮网站可能会有访问限制，建议合理控制请求频率
2. 部分公司可能没有公开某些年份的报告
3. 下载速度取决于网络状况和文件大小
4. 搜索公司时，建议使用股票代码以提高搜索准确率

## 许可证

MIT License
