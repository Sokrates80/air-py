import pyb

AIRPY_ERROR = 3
AIRPY_WARNING = 2
AIRPY_DEBUG = 1
AIRPY_INFO = 0


__LOGGER_PRIORITY = AIRPY_INFO
__CACHING_ENABLED = False
__CACHE = []


def __validate_priority(priority):
    """
    Determines if log can be printed
    :param priority: priority to be matched
    :return:
    """
    global __LOGGER_PRIORITY
    return priority >= __LOGGER_PRIORITY


def __write_on_sd(text_list):
    """
    Writes on sd
    :param text_list: list of text to be written
    :return:
    """
    try:
        with open("/sd/airpy_log.txt", "a") as f:
            #for text in text_list
            f.write("%s\n" % text_list)
            f.close()
            pyb.sync()
    except OSError:
        pass


def __cache_log(text):
    """
    Caches log
    :param text: text to be cached
    :return:
    """
    pass


def __airpy_log(text):
    """
    Final gateway before writing the log
    :param text: text to be written
    :return:
    """
    global __CACHING_ENABLED
    log_line = ("%s\t%s" % (pyb.millis(), text))
    if __CACHING_ENABLED:
        __cache_log(log_line)
    else:
        #__write_on_sd([log_line])
        __write_on_sd(log_line)


def init(priority, enable_caching=False):
    """
    Logger entry point
    :param priority: logger default priority
    :param enable_caching: caching toggle
    :return:
    """
    global __CACHING_ENABLED
    __CACHING_ENABLED = enable_caching
    set_logger_priority(priority)


def set_logger_priority(priority):
    """
    Sets logging priority
    :param priority: new priority value
    :return:
    """
    global __LOGGER_PRIORITY
    __LOGGER_PRIORITY = priority


def flush():



def error(text):
    """
    Prints text with error priority
    :param text: text that will e printed
    :return:
    """
    if not __validate_priority(AIRPY_ERROR):
        return
    __airpy_log("ERROR\t{}".format(text))


def warning(text):
    """
    Prints text with warning priority
    :param text: text that will e printed
    :return:
    """
    if not __validate_priority(AIRPY_WARNING):
        return
    __airpy_log("WARNING\t{}".format(text))


def debug(text):
    """
    Prints text with debug priority
    :param text: text that will e printed
    :return:
    """
    if not __validate_priority(AIRPY_DEBUG):
        return
    __airpy_log("DEBUG\t{}".format(text))


def info(text):
    """
    Prints text with info priority
    :param text: text that will e printed
    :return:
    """
    if not __validate_priority(AIRPY_INFO):
        return
    __airpy_log("INFO\t{}".format(text))
