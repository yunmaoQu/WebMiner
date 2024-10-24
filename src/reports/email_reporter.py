import os
from typing import Dict, Any, List
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class EmailReporter:
    """邮件报告生成器"""

    def __init__(
        self, 
        template_dir: str = 'templates',
        smtp_host: str = None,
        smtp_port: int = None,
        smtp_user: str = None,
        smtp_password: str = None
    ):
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.smtp_host = smtp_host or os.getenv('SMTP_HOST')
        self.smtp_port = smtp_port or int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = smtp_user or os.getenv('SMTP_USER')
        self.smtp_password = smtp_password or os.getenv('SMTP_PASSWORD')

    def send_daily_report(
        self, 
        data: Dict[str, Any], 
        recipients: List[str]
    ) -> None:
        """发送每日报告"""
        try:
            template = self.env.get_template('email/daily_report.html')
            
            # 准备上下文数据
            context = {
                'report_date': datetime.now().strftime('%Y-%m-%d'),
                **data
            }
            
            # 渲染模板
            html_content = template.render(**context)
            
            # 发送邮件
            self._send_email(
                subject="GitHub Trending Daily Report",
                html_content=html_content,
                recipients=recipients
            )
            
            logger.info("Daily report sent successfully")
            
        except Exception as e:
            logger.error(f"Error sending daily report: {e}")
            raise

    def send_weekly_report(
        self, 
        data: Dict[str, Any], 
        recipients: List[str]
    ) -> None:
        """发送每周报告"""
        try:
            template = self.env.get_template('email/weekly_report.html')
            
            # 准备上下文数据
            context = {
                'start_date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
                'end_date': datetime.now().strftime('%Y-%m-%d'),
                **data
            }
            
            # 渲染模板
            html_content = template.render(**context)
            
            # 发送邮件
            self._send_email(
                subject="GitHub Trending Weekly Report",
                html_content=html_content,
                recipients=recipients
            )
            
            logger.info("Weekly report sent successfully")
            
        except Exception as e:
            logger.error(f"Error sending weekly report: {e}")
            raise

    def _send_email(
        self, 
        subject: str, 
        html_content: str, 
        recipients: List[str]
    ) -> None:
        """发送邮件"""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.smtp_user
        msg['To'] = ', '.join(recipients)
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)