from setuptools import setup, find_packages

setup(
    name="cninfo-report-downloader",
    version="1.0.0",
    description="从巨潮网站下载指定公司、指定年份的年报和季度报告",
    long_description="""\
    该工具用于从巨潮资讯网(www.cninfo.com.cn)下载指定公司、指定年份的年报和季度报告。
    支持下载PDF格式的报告文件。
    """,
    author="Author",
    author_email="author@example.com",
    url="https://github.com/yourusername/cninfo-report-downloader",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.32.0",
        "beautifulsoup4>=4.14.0"
    ],
    entry_points={
        "console_scripts": [
            "cninfo-download = download_cninfo_report:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)