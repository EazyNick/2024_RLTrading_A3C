from .Logger import LogManager

log_manager = LogManager()

# Logger를 패키지 내에서 사용 가능하게 설정
__all__ = ['log_manager']