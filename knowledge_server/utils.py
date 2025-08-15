import logging
import logging.handlers
import os


from configs import LOG_FILE_PATH, LOG_LEVEL

log_level_map = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}



def get_logging(log_name):
        
    log_level = os.getenv("LOG_LEVEL", LOG_LEVEL)
    if log_level is None:
        log_level = logging.INFO
    else:
        if log_level in log_level_map:
            log_level = log_level_map[log_level]
        else:
            log_level = logging.INFO

    logger = logging.getLogger(log_name)

    fh = logging.handlers.TimedRotatingFileHandler(filename=LOG_FILE_PATH, when='D', backupCount=7, encoding='utf-8')
    formatter = logging.Formatter(
        fmt="%(asctime)s %(name)s %(filename)s %(message)s",
        datefmt="%Y/%m/%d %X"
        )
    fh.setFormatter(formatter)
    logger.setLevel(log_level)
    logger.addHandler(fh)

    sh = logging.StreamHandler()#往屏幕上输出
    sh.setFormatter(formatter) #设置屏幕上显示的格式
    logger.addHandler(sh)

    return logger