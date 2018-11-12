'''my.log 파일과 스트림 로그를 생성하기 위한 파일입니다.'''
import logging


def getMyLogger():

    # 로깅 기본 포멧 설정
    mylogger = logging.getLogger('basic')
    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s')
    mylogger.setLevel(logging.DEBUG)

    # 스트림 핸들러 설정
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(formatter)

    # 파일 핸들러 설정
    file_handler = logging.FileHandler("my.log", encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 로깅 핸들러 추가
    mylogger.addHandler(file_handler)
    mylogger.addHandler(stream_handler)

    return mylogger
