from contextlib import contextmanager
from typing import Generator
from sqlalchemy.orm import Session

@contextmanager
def get_db_session(db_manager) -> Generator[Session, None, None]:
    """
    数据库会话上下文管理器
    
    Usage:
        with get_db_session(db_manager) as session:
            session.query(...)
    """
    session = db_manager.get_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()