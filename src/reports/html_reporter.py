import os
from datetime import datetime
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class HTMLReporter:
    """HTML报告生成器"""

    def __init__(self, template_dir: str = 'templates'):
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
    def generate_trending_report(self, data: Dict[str, Any]) -> str:
        """
        生成趋势报告
        
        Args:
            data: 报告数据
            
        Returns:
            生成的HTML报告路径
        """
        try:
            template = self.env.get_template('web/trending.html')
            
            # 准备上下文数据
            context = {
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                **data
            }
            
            # 渲染模板
            html_content = template.render(**context)
            
            # 保存报告
            report_path = self._save_report(html_content)
            logger.info(f"Generated trending report: {report_path}")
            
            return report_path
            
        except Exception as e:
            logger.error(f"Error generating trending report: {e}")
            raise

    def _save_report(self, content: str) -> str:
        """保存报告到文件"""
        # 创建reports目录
        os.makedirs('reports', exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'reports/trending_report_{timestamp}.html'
        
        # 保存文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return filename