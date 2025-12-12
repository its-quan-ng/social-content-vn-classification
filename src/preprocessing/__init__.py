"""
Preprocessing Module for Vietnamese Sentiment Analysis
=======================================================

Modules:
- text_cleaner: Làm sạch văn bản (URL, HTML, mentions, ký tự lặp, v.v.)
- emoji_handler: Chuyển đổi emoji và emoticons sang tiếng Việt
- text_normalizer: Chuẩn hóa slang, teencode, viết tắt
- word_segmenter: Tách từ tiếng Việt (PyVi, VnCoreNLP)
- preprocessing_pipeline: Pipeline tích hợp tất cả các bước

Author: PPNCKH Project
"""

from .text_cleaner import TextCleaner
from .emoji_handler import EmojiHandler
from .text_normalizer import TextNormalizer
from .word_segmenter import WordSegmenter, SimpleWordSegmenter
from .preprocessing_pipeline import PreprocessingPipeline

__all__ = [
    'TextCleaner',
    'EmojiHandler',
    'TextNormalizer',
    'WordSegmenter',
    'SimpleWordSegmenter',
    'PreprocessingPipeline',
]

__version__ = '1.0.0'

