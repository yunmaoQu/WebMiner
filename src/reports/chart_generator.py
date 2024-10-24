# reporters/chart_generator.py 继续
from typing import Dict, Any, List
import plotly.graph_objects as go
import plotly.express as px
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class ChartGenerator:
    """图表生成器"""

    def generate_language_chart(self, data: Dict[str, Any]) -> str:
        """生成语言分布图表"""
        try:
            # 准备数据
            languages = [item['name'] for item in data['language_stats']]
            repos = [item['repos'] for item in data['language_stats']]
            
            # 创建图表
            fig = go.Figure(data=[
                go.Bar(
                    x=languages,
                    y=repos,
                    text=repos,
                    textposition='auto',
                )
            ])
            
            # 设置布局
            fig.update_layout(
                title='Repository Distribution by Language',
                xaxis_title='Programming Language',
                yaxis_title='Number of Repositories',
                template='plotly_white'
            )
            
            # 返回HTML
            return fig.to_html(full_html=False)
            
        except Exception as e:
            logger.error(f"Error generating language chart: {e}")
            raise

    
    def generate_activity_chart(self, data: Dict[str, Any]) -> str:
        """生成活跃度趋势图表"""
        try:
            # 准备数据
            repos = [repo['name'] for repo in data['trending_repos']]
            scores = [repo['activity_score'] for repo in data['trending_repos']]
            
            # 创建图表
            fig = go.Figure(data=[
                go.Bar(
                    x=repos,
                    y=scores,
                    text=[f"{score:.1f}" for score in scores],
                    textposition='auto',
                    marker_color='rgb(158,202,225)'
                )
            ])
            
            # 设置布局
            fig.update_layout(
                title='Repository Activity Scores',
                xaxis_title='Repository',
                yaxis_title='Activity Score',
                template='plotly_white',
                xaxis_tickangle=-45
            )
            
            return fig.to_html(full_html=False)
            
        except Exception as e:
            logger.error(f"Error generating activity chart: {e}")
            raise

    def generate_stars_trend_chart(self, data: Dict[str, Any]) -> str:
        """生成star趋势图表"""
        try:
            # 准备数据
            repos = [repo['name'] for repo in data['trending_repos']]
            stars = [repo['stars'] for repo in data['trending_repos']]
            today_stars = [repo['today_stars'] for repo in data['trending_repos']]
            
            # 创建图表
            fig = go.Figure()
            
            # 添加总stars柱状图
            fig.add_trace(
                go.Bar(
                    name='Total Stars',
                    x=repos,
                    y=stars,
                    text=[f"{s:,}" for s in stars],
                    textposition='auto',
                )
            )
            
            # 添加今日stars柱状图
            fig.add_trace(
                go.Bar(
                    name="Today's Stars",
                    x=repos,
                    y=today_stars,
                    text=[f"+{s:,}" for s in today_stars],
                    textposition='auto',
                )
            )
            
            # 设置布局
            fig.update_layout(
                title='Repository Stars Overview',
                xaxis_title='Repository',
                yaxis_title='Stars',
                barmode='group',
                template='plotly_white',
                xaxis_tickangle=-45
            )
            
            return fig.to_html(full_html=False)
            
        except Exception as e:
            logger.error(f"Error generating stars trend chart: {e}")
            raise

    def generate_language_trend_chart(self, data: Dict[str, Any]) -> str:
        """生成语言趋势图表"""
        try:
            # 准备数据
            languages = []
            repos_counts = []
            avg_activities = []
            total_stars = []
            
            for lang_stat in data['language_stats']:
                languages.append(lang_stat['name'])
                repos_counts.append(lang_stat['repos'])
                avg_activities.append(lang_stat['avg_activity'])
                total_stars.append(lang_stat['stars'])
            
            # 创建散点图
            fig = px.scatter(
                x=repos_counts,
                y=avg_activities,
                size=total_stars,
                text=languages,
                labels={
                    'x': 'Number of Repositories',
                    'y': 'Average Activity Score',
                    'size': 'Total Stars'
                }
            )
            
            # 更新布局
            fig.update_layout(
                title='Language Popularity vs Activity',
                template='plotly_white',
                showlegend=False
            )
            
            # 更新标记
            fig.update_traces(
                textposition='top center',
                marker=dict(sizeref=2.*max(total_stars)/(40.**2))
            )
            
            return fig.to_html(full_html=False)
            
        except Exception as e:
            logger.error(f"Error generating language trend chart: {e}")
            raise

    def generate_combined_report_charts(self, data: Dict[str, Any]) -> Dict[str, str]:
        """生成完整报告所需的所有图表"""
        try:
            charts = {
                'language_distribution': self.generate_language_chart(data),
                'activity_scores': self.generate_activity_chart(data),
                'stars_trend': self.generate_stars_trend_chart(data),
                'language_trends': self.generate_language_trend_chart(data)
            }
            
            return charts
            
        except Exception as e:
            logger.error(f"Error generating report charts: {e}")
            raise

    def _create_color_scale(self, values: List[float]) -> List[str]:
        """创建颜色渐变比例"""
        import numpy as np
        
        min_val = min(values)
        max_val = max(values)
        normalized = [(v - min_val) / (max_val - min_val) for v in values]
        
        colors = []
        for n in normalized:
            if n < 0.33:
                colors.append('rgb(158,202,225)')  # 浅蓝
            elif n < 0.66:
                colors.append('rgb(107,174,214)')  # 中蓝
            else:
                colors.append('rgb(49,130,189)')   # 深蓝
                
        return colors