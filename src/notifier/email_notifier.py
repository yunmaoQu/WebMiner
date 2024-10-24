# email_notifier.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)

class EmailNotifier:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.recipient_emails = os.getenv('RECIPIENT_EMAILS', '').split(',')

    def send_trending_report(self, trending_data):
        """发送趋势报告邮件"""
        if not self.sender_email or not self.sender_password:
            logger.warning("Email credentials not configured")
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(self.recipient_emails)
            msg['Subject'] = f'GitHub Trending Report - {datetime.now().strftime("%Y-%m-%d")}'

            # 创建HTML邮件内容
            html_content = self._create_html_report(trending_data)
            msg.attach(MIMEText(html_content, 'html'))

            # 发送邮件
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            logger.info("Trending report email sent successfully")

        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise

    def _create_html_report(self, trending_data):
        """创建HTML格式的报告"""
        html = """
        <html>
        <head>
            <style>
                table { border-collapse: collapse; width: 100%; }
                th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }
                th { background-color: #f2f2f2; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .trend-up { color: green; }
                .trend-down { color: red; }
            </style>
        </head>
        <body>
            <h2>GitHub Trending Repositories Report</h2>
            <table>
                <tr>
                    <th>Repository</th>
                    <th>Language</th>
                    <th>Activity Score</th>
                    <th>Score Change</th>
                    <th>Stars</th>
                    <th>Issues</th>
                </tr>
        """

        for repo in trending_data:
            name, score, stars, forks, issues, language, prev_score = repo
            score_change = score - (prev_score or score)
            trend_class = "trend-up" if score_change >= 0 else "trend-down"
            
            html += f"""
                <tr>
                    <td><a href="https://github.com/{name}">{name}</a></td>
                    <td>{language}</td>
                    <td>{score:.1f}</td>
                    <td class="{trend_class}">{score_change:+.1f}</td>
                    <td>{stars:,}</td>
                    <td>{issues}</td>
                </tr>
            """

        html += """
            </table>
            <p><small>Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
        </body>
        </html>
        """
        return html