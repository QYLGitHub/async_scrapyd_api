""""
scrapyd api 的异步实现
"""
from .client import ScrapyApi as _ScrapyApi


class AsyncScrapyApi(_ScrapyApi):
    pass


version = __version__ = '0.0.1'
__all_ = ["AsyncScrapyApi"]
