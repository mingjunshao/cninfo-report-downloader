#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
巨潮资讯网报告下载工具
用于下载指定公司、指定年份的年报和季度报告
"""

import requests
import re
import os
import argparse
import logging
from bs4 import BeautifulSoup
from urllib.parse import quote

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cninfo_download.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CNInfoReportDownloader:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    def search_company(self, company_name):
        """
        搜索公司信息
        :param company_name: 公司名称或股票代码
        :return: 公司信息字典，包含name（公司名称）
        """
        try:
            # 直接返回公司名称
            logger.info(f"搜索公司: {company_name}")
            return {
                'name': company_name,
                'code': company_name if re.match(r'^\d{6}$', company_name) else ''
            }
        except Exception as e:
            logger.error(f"搜索公司信息失败: {str(e)}")
            return {
                'name': company_name,
                'code': ''
            }
    def download_report(self, company_info, year, report_type, quarter=None):
        """
        下载报告
        :param company_info: 公司信息字典
        :param year: 年份
        :param report_type: 报告类型，'annual' 或 'quarterly'
        :param quarter: 季度，仅季度报告需要
        :return: 下载的文件路径
        """
        try:
            # 构建搜索关键词
            if report_type == 'annual':
                report_title = f"{year}年年度报告"
                report_keywords = [f"{year}年年度报告", f"{year}年度报告", f"年度报告"]
            else:
                if not quarter:
                    logger.error("季度报告需要指定季度")
                    return None
                quarter_map = {'1': '第一季度', '2': '半年度', '3': '第三季度', '4': '年度'}
                quarter_name = quarter_map.get(quarter, '')
                report_title = f"{year}年{quarter_name}报告"
                report_keywords = [f"{year}年{quarter_name}报告", f"{year}{quarter_name}报告", f"{quarter_name}报告"]
            
            logger.info(f"开始下载 {company_info['name']} {report_title}")
            
            # 尝试多种搜索策略
            search_patterns = [
                company_info['name'],  # 仅公司名称
                f"{company_info['name']} {year}",  # 公司名称+年份
                f"{company_info['name']} {report_title}",  # 公司名称+报告标题
                f"{company_info['code']}",  # 仅股票代码
                f"{company_info['code']} {year}",  # 股票代码+年份
            ]
            
            for search_key in search_patterns:
                search_url = f"http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey={quote(search_key)}"
                logger.info(f"搜索: {search_key}")
                
                # 使用GET请求
                try:
                    response = requests.get(search_url, headers=self.headers, timeout=10)
                    response.encoding = 'utf-8'
                except requests.exceptions.RequestException as e:
                    logger.error(f"请求搜索URL失败: {str(e)}")
                    continue
                
                # 解析搜索结果
                try:
                    data = response.json()
                except ValueError:
                    logger.warning(f"搜索 {search_key} 时响应不是JSON格式")
                    continue
                
                if data.get('announcements'):
                    logger.info(f"找到 {len(data['announcements'])} 条公告")
                    # 打印找到的公告标题
                    logger.debug("找到的公告标题:")
                    
                    # 优先选择完整版本的报告，而不是摘要
                    full_report_item = None
                    summary_report_item = None
                    
                    for item in data['announcements']:
                        title = item.get('announcementTitle', '')
                        logger.debug(f"- {title}")
                        # 检查标题是否包含任何报告关键词和年份
                        for keyword in report_keywords:
                            if keyword in title and str(year) in title:
                                # 区分完整报告和摘要
                                if '摘要' not in title:
                                    full_report_item = item
                                    break
                                elif summary_report_item is None:
                                    summary_report_item = item
                        if full_report_item:
                            break
                    
                    # 优先使用完整版本，如果没有则使用摘要版本
                    target_item = full_report_item or summary_report_item
                    
                    if target_item:
                        # 构建下载URL
                        adjunct_url = target_item.get('adjunctUrl')
                        if adjunct_url:
                            down_url = f"http://static.cninfo.com.cn/{adjunct_url}"
                            
                            # 下载文件
                            file_name = f"{company_info['name']}_{report_title}.pdf"
                            file_path = os.path.join(os.getcwd(), file_name)
                            
                            logger.info(f"正在下载 {file_name}...")
                            logger.info(f"下载链接: {down_url}")
                            
                            # 添加更多的请求头用于下载
                            down_headers = self.headers.copy()
                            down_headers['Accept'] = 'application/pdf, application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
                            
                            # 下载文件
                            try:
                                down_response = requests.get(down_url, headers=down_headers, timeout=30, stream=True)
                                down_response.raise_for_status()  # 检查HTTP错误
                                
                                with open(file_path, 'wb') as f:
                                    for chunk in down_response.iter_content(chunk_size=1024):
                                        if chunk:
                                            f.write(chunk)
                                
                                logger.info(f"下载完成，保存路径: {file_path}")
                                return file_path
                            except requests.exceptions.RequestException as e:
                                logger.error(f"下载文件时出错: {str(e)}")
                                # 如果完整版本下载失败，尝试下载摘要版本
                                if full_report_item and summary_report_item:
                                    logger.info("完整版本下载失败，尝试下载摘要版本...")
                                    adjunct_url = summary_report_item.get('adjunctUrl')
                                    if adjunct_url:
                                        down_url = f"http://static.cninfo.com.cn/{adjunct_url}"
                                        
                                        try:
                                            down_response = requests.get(down_url, headers=down_headers, timeout=30, stream=True)
                                            down_response.raise_for_status()
                                            
                                            with open(file_path, 'wb') as f:
                                                for chunk in down_response.iter_content(chunk_size=1024):
                                                    if chunk:
                                                        f.write(chunk)
                                            
                                            logger.info(f"摘要版本下载完成，保存路径: {file_path}")
                                            return file_path
                                        except requests.exceptions.RequestException as e:
                                            logger.error(f"摘要版本下载也失败: {str(e)}")
                                            continue
            
            logger.warning(f"未找到 {report_title}")
            return None
        except Exception as e:
            logger.error(f"下载报告失败: {str(e)}")
            # 打印响应内容以便调试
            try:
                if 'response' in locals():
                    logger.debug(f"响应内容: {response.text[:500]}")
            except:
                pass
            return None

def print_usage():
    """
    打印详细的使用说明
    """
    usage = """巨潮资讯网报告下载工具使用说明：

用法1：下载年报
    download_cninfo_report.exe 公司名称 年份 annual
    示例：download_cninfo_report.exe 贵州茅台 2023 annual
    示例：download_cninfo_report.exe 600519 2023 annual

用法2：下载季度报告
    download_cninfo_report.exe 公司名称 年份 quarterly --quarter 季度
    示例：download_cninfo_report.exe 东吴证券 2023 quarterly --quarter 1  # 第一季度
    示例：download_cninfo_report.exe 601555 2023 quarterly --quarter 2  # 半年度
    示例：download_cninfo_report.exe 601555 2023 quarterly --quarter 3  # 第三季度

参数说明：
    company     - 公司名称或股票代码
    year        - 报告年份（数字）
    type        - 报告类型：annual(年报) 或 quarterly(季度报告)
    --quarter   - 季度，仅季度报告需要，可选值：1, 2, 3, 4

注意事项：
    1. 搜索公司时，建议使用股票代码以提高搜索准确率
    2. 部分公司可能没有公开某些年份的报告
    3. 下载速度取决于网络状况和文件大小
    4. 巨潮网站可能会有访问限制，建议合理控制请求频率
"""
    print(usage)

def main():
    # 创建参数解析器
    parser = argparse.ArgumentParser(
        description='巨潮资讯网报告下载工具',
        add_help=False  # 禁用默认的帮助选项
    )
    
    # 添加参数
    parser.add_argument('company', nargs='?', help='公司名称或股票代码')
    parser.add_argument('year', nargs='?', type=int, help='报告年份')
    parser.add_argument('type', nargs='?', choices=['annual', 'quarterly'], help='报告类型: annual(年报) 或 quarterly(季度报告)')
    parser.add_argument('--quarter', choices=['1', '2', '3', '4'], help='季度，仅季度报告需要')
    parser.add_argument('-h', '--help', action='store_true', help='显示详细使用说明')
    
    try:
        args = parser.parse_args()
        
        # 检查是否请求帮助
        if args.help or not args.company or not args.year or not args.type:
            print_usage()
            return
        
        # 检查季度报告是否提供了季度参数
        if args.type == 'quarterly' and not args.quarter:
            logger.error("错误：季度报告需要指定季度参数 --quarter")
            print_usage()
            return
        
        # 验证年份范围
        import datetime
        current_year = datetime.datetime.now().year
        if args.year < 1990 or args.year > current_year:
            logger.error(f"错误：年份必须在1990到{current_year}之间")
            print_usage()
            return
        
        # 打印欢迎信息
        print(f"\n=== 巨潮资讯网报告下载工具 ===")
        print(f"正在处理：{args.company} {args.year}年 {args.type}报告")
        if args.quarter:
            print(f"季度：{args.quarter}")
        print("=============================\n")
        
        downloader = CNInfoReportDownloader()
        
        # 搜索公司信息
        logger.info(f"正在搜索公司: {args.company}...")
        company_info = downloader.search_company(args.company)
        
        if not company_info:
            logger.error(f"未找到公司: {args.company}")
            print_usage()
            return
        
        logger.info(f"找到公司: {company_info['name']} (代码: {company_info['code']})")
        
        # 下载报告
        result = downloader.download_report(company_info, args.year, args.type, args.quarter)
        
        if not result:
            logger.warning(f"未能下载 {args.company} {args.year}年的{args.type}报告")
            print("\n提示：请检查公司名称是否正确，或该公司是否发布了指定年份的报告。")
            print_usage()
            return
        else:
            print(f"\n✅ 下载完成！文件保存路径：{result}")
            print("\n提示：如果需要下载其他报告，请重新运行程序并指定不同的参数。")
            
    except argparse.ArgumentError as e:
        logger.error(f"参数错误: {str(e)}")
        print_usage()
    except ValueError as e:
        logger.error(f"参数值错误: {str(e)}")
        print("提示：年份必须是数字，请检查输入是否正确。")
        print_usage()
    except Exception as e:
        logger.error(f"运行错误: {str(e)}")
        print("提示：可能的原因包括网络连接问题、巨潮网站访问限制或参数输入错误。")
        print_usage()

if __name__ == '__main__':
    main()
