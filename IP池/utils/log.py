import sys
import logging

from settings import LOG_LEVEL,LOG_DATEFMT,LOG_FMT,LOG_FILENAME


class Logger(object):
    def __init__(self):
        # 获取一个logger对象
        self._logger = logging.getLogger()
        # 设置format对象
        self.formatter = logging.Formatter(fmt=LOG_FMT, datefmt=LOG_DATEFMT)
        # 设置文件日志模式
        self._logger.addHandler(self.get_file_handler(LOG_FILENAME))
        # 设置终端日志模式
        self._logger.addHandler(self._get_console_handler())
        # 设置日志等级
        self._logger.setLevel(LOG_LEVEL)

    def get_file_handler(self, filename):
        # 获取一个文件日志handler
        filehandler = logging.FileHandler(filename=filename, encoding='utf-8')
        # 设置日志格式
        filehandler.setFormatter(self.formatter)
        # 返回
        return filehandler

    def _get_console_handler(self):
        # 获取一个输出到终端日志的handler
        console_handler = logging.StreamHandler(sys.stdout)
        # 设置日志格式
        console_handler.setFormatter(self.formatter)
        # 返回handler
        return console_handler

    @property
    def logger(self):
        return self._logger


# 初始化并配一个logger对象
# 使用时，直接导入logger就可以使用
logger = Logger().logger

if __name__ == '__main__':
    logger.debug("调试信息")
    logger.info("状态信息")
    logger.warning("警告信息")
    logger.error("错误信息")
    logger.critical("严重错误信息")
