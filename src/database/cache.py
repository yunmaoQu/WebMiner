from functools import wraps
from typing import Any, Callable
import redis
import json
import pickle
from datetime import timedelta

class CacheManager:
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis = redis.from_url(redis_url)

    def cache(
        self,
        prefix: str,
        expire: int = 300
    ) -> Callable:
        """
        缓存装饰器
        
        Args:
            prefix: 缓存键前缀
            expire: 过期时间（秒）
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                # 生成缓存键
                cache_key = f"{prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
                
                # 尝试从缓存获取
                cached_data = self.redis.get(cache_key)
                if cached_data:
                    return pickle.loads(cached_data)
                
                # 执行函数
                result = func(*args, **kwargs)
                
                # 存入缓存
                self.redis.setex(
                    cache_key,
                    timedelta(seconds=expire),
                    pickle.dumps(result)
                )
                
                return result
            return wrapper
        return decorator

    def invalidate(self, prefix: str) -> None:
        """清除指定前缀的缓存"""
        for key in self.redis.scan_iter(f"{prefix}:*"):
            self.redis.delete(key)