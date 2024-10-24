import logging
from alembic import command
from alembic.config import Config
from pathlib import Path

logger = logging.getLogger(__name__)

class DatabaseMigration:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.alembic_cfg = self._get_alembic_config()

    def _get_alembic_config(self) -> Config:
        """获取 Alembic 配置"""
        project_root = Path(__file__).parent.parent.parent
        alembic_cfg = Config()
        alembic_cfg.set_main_option("script_location", str(project_root / "migrations"))
        alembic_cfg.set_main_option("sqlalchemy.url", self.db_url)
        return alembic_cfg

    def upgrade(self, revision: str = "head") -> None:
        """升级数据库到最新版本"""
        try:
            logger.info(f"Upgrading database to revision: {revision}")
            command.upgrade(self.alembic_cfg, revision)
        except Exception as e:
            logger.error(f"Database upgrade failed: {e}")
            raise

    def downgrade(self, revision: str) -> None:
        """回滚数据库到指定版本"""
        try:
            logger.info(f"Downgrading database to revision: {revision}")
            command.downgrade(self.alembic_cfg, revision)
        except Exception as e:
            logger.error(f"Database downgrade failed: {e}")
            raise

    def create_migration(self, message: str) -> None:
        """创建新的迁移脚本"""
        try:
            logger.info(f"Creating new migration: {message}")
            command.revision(self.alembic_cfg, message=message, autogenerate=True)
        except Exception as e:
            logger.error(f"Failed to create migration: {e}")
            raise