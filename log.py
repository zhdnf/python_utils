#encoding=utf-8

import logging
import logging.handlers

class MyLog:

# Logger,Handler,Formatter
    def __init__(self):
        self.log = logging
        self.logger = None
        self.handler = None
        self.formatter = None
        
    # Logger Config
    def logger_config(self, name, level):
        self.logger = self.log.getLogger(name)
        self.logger.setLevel(level)
    
    # Handler Config
    def handler_config(self, path):
        self.handler = self.log.FileHandler(path)
    
    # Formatter Config
    def formatter_config(self):
        # 示例: 2017-05-06 14:22:1 - DEBUG - This is a debug log
        log_format = "%(asctime)s - %(levelname)s - %(message)s"
        time_format = "%m/%d/%Y %H:%M:%S"
        self.formatter = self.log.Formatter(log_format, time_format)

    def add_handler_formatter(self):
        self.handler.setFormatter(self.formatter)

    def add_logger_handler(self):
        self.logger.addHandler(self.handler)

def create_log(name, path, level):
    
    mylog = MyLog()
    
    mylog.logger_config(name, level)
    mylog.handler_config(path)
    mylog.formatter_config()
   
    # handler添加formatter,(可选，不添加无格式)
    mylog.add_handler_formatter()
   
    # logger添加handler(必选)
    mylog.add_logger_handler()
    
    return mylog.logger


if __name__ == "__main__":
        mylog = create_log("mylog", "/root/logging.log", 10)
        mylog.debug("123")
        mylog.warn("123")
        mylog.error("123")
        mylog.critical("123")
