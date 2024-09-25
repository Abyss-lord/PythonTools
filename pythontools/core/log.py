#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   log.py
@Date       :   2024/09/25
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/09/25
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import collections
import logging
import os
import re
import sys
import threading
import time
from logging import Logger, handlers

from .constants.string_constant import CharPool
from .errors import LoggerException
from .utils.osutils import SysUtil

ROTATION = 0
INFINITE = 1

ROTATION_COUNTS = 30
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
G_INITED_LOGGER: list[str] = []


info = logging.info
warn = logging.warning
warning = logging.warning
error = logging.error
debug = logging.debug
critical = logging.critical
fatal = logging.fatal


LoggerParams = collections.namedtuple(
    "LoggerParams",
    [
        "loglevel",  # one of logging.INFO logging.DEBUG logging.xxx levels
        "logfile",  # valid logfile position,  e.g.   /home/test/test.log
        "log_type",  # log.ROTATION  log.INFINITE
        "max_log_size",
        "print_console",
        "gen_wf",  # True/False, generate log lines with level >= WARNING
        "field_splitter",
    ],
)


class _Singleton:  # pylint: disable=R0903
    """
    internal use for logging
    """

    _LOCK = threading.Lock()

    def __init__(self, cls):
        self.__instance = None
        self.__cls = cls

    def __call__(self, *args, **kwargs):
        # pylint: disable=consider-using-with
        self._LOCK.acquire()
        if self.__instance is None:
            self.__instance = self.__cls(*args, **kwargs)
        self._LOCK.release()
        return self.__instance


class _MsgFilter(logging.Filter):
    """
    日志级别过滤器
    """

    # pylint: disable= super-init-not-called
    def __init__(self, msg_level=logging.WARNING):
        self.msg_level = msg_level

    def filter(self, record):
        return record.levelno < self.msg_level


class LogInitializer:
    """
    default log initializer
    """

    @classmethod
    def setup_file_logger(
        cls,
        logger: Logger,
        log_params: LoggerParams,
    ) -> None:
        """
        初始化文件 logger 对象

        Parameters
        ----------
        logger : Logger
            待初始化的 logger 对象
        log_params : LoggerParams
            配置参数

        Raises
        ------
        OSError
            如果日志文件不存在，则尝试创建日志文件，但文件创建失败时抛出 OSError 异常
        """
        loglevel = log_params.loglevel
        str_log_file = log_params.logfile

        # 设置日志级别
        logger.setLevel(loglevel)
        # 创建日志文件
        cls._check_and_create_log_file(str_log_file)
        # 设置日志格式
        formatter = cls.get_formatter(log_params)
        # 设置控制台 handler
        cls.set_stream_handler(logger, log_params, formatter)
        # 设置文件 handler
        cls.set_file_handler(logger, log_params, formatter)

    @classmethod
    def proc_thd_id(cls) -> str:
        """
        获取进程ID:线程ID

        Returns
        -------
        str
            进程ID:线程ID
        """
        return f"{os.getpid()}:{threading.current_thread().ident}"

    @classmethod
    def get_code_line(cls, back=0) -> int:
        """
        获取代码行号

        Parameters
        ----------
        back : int, optional
            栈帧索引, by default 0

        Returns
        -------
        int
            给定栈帧的行号
        """
        return sys._getframe(back + 1).f_lineno  # traceback pylint:disable=W0212

    @classmethod
    def get_code_file(cls, back=0) -> str:
        """
        返回给定栈帧代码对象所属的文件名

        Parameters
        ----------
        back : int, optional
            回溯的栈帧层级, by default 0

        Returns
        -------
        str
            给定栈帧代码对象所属的文件名
        """
        return os.path.basename(sys._getframe(back + 1).f_code.co_filename)

    @classmethod
    def log_file_func_info(
        cls,
        msg: str,
        back_trace_len: int = 0,
    ) -> str:
        """
        返回日志回溯信息

        Parameters
        ----------
        msg : str
            日志信息
        back_trace_len : int, optional
            回溯的栈帧层级, by default 0

        Returns
        -------
        str
            日志回溯信息
        """

        temp_msg = f" * {cls.proc_thd_id()} {cls.get_code_file(2 + back_trace_len)}:\
            {cls.get_code_line(2 + back_trace_len)}]"

        return f"{temp_msg}{msg}"

    @classmethod
    def get_formatter(cls, log_params: LoggerParams) -> logging.Formatter:
        """
        获取日志formatter

        Parameters
        ----------
        log_params : LoggerParams
            日志参数

        Returns
        -------
        logging.Formatter
            Formatter 实例
        """
        tznum = time.strftime("%z")
        tzkey = time.strftime("%Z")
        splitter = log_params.field_splitter
        return logging.Formatter(
            fmt=f" %(asctime)s {tznum}({tzkey}) {splitter} %(levelname)-10s {splitter} "
            f"%(process)d:%(threadName)s(%(thread)x) {splitter} %(filename)s#%(funcName)s:%(lineno)s - %(message)s"
        )

    @classmethod
    def set_stream_handler(
        cls,
        logger: Logger,
        log_params: LoggerParams,
        formatter: logging.Formatter,
    ) -> None:
        """
        设置控制台 handler

        Parameters
        ----------
        logger : Logger
            待设置 Logger 对象
        log_params : LoggerParams
            设置参数
        formatter : logging.Formatter
            Formatter 实例
        """
        is_print_console = log_params.print_console
        if is_print_console:
            info("print_console enabled, will print to stdout")
            streamhandler = logging.StreamHandler()
            loglevel = log_params.loglevel
            streamhandler.setLevel(loglevel)
            streamhandler.setFormatter(formatter)
            logger.addHandler(streamhandler)

    @classmethod
    def set_file_handler(
        cls,
        logger: Logger,
        log_params: LoggerParams,
        formatter: logging.Formatter,
    ) -> None:
        """
        设置文件 handler

        Parameters
        ----------
        logger : Logger
            要设置的Logger对象
        log_params : LoggerParams
            设置参数
        formatter : logging.Formatter
            Formatter 实例
        """
        log_level = log_params.loglevel

        fdhandler = cls._get_file_handler(log_params)

        fdhandler.setFormatter(formatter)  # type: ignore
        fdhandler.setLevel(log_level)
        cls._set_wf(logger, log_params, formatter, fdhandler)
        logger.addHandler(fdhandler)

    @classmethod
    def _set_wf(cls, logger: Logger, log_params: LoggerParams, formatter, fdhandler):
        gen_wf = log_params.gen_wf
        str_log_file = log_params.logfile
        if gen_wf:
            file_wf = f"{str(str_log_file)}.wf"
            warn_handler = logging.FileHandler(file_wf, "a", encoding="utf-8")
            warn_handler.setLevel(logging.WARNING)
            warn_handler.setFormatter(formatter)
            logger.addHandler(warn_handler)
            fdhandler.addFilter(_MsgFilter(logging.WARNING))  # type: ignore

    @classmethod
    def _get_file_handler(cls, log_params: LoggerParams) -> handlers.RotatingFileHandler | logging.FileHandler:
        str_log_file = log_params.logfile
        log_type = log_params.log_type
        maxsize = log_params.max_log_size

        return (
            handlers.RotatingFileHandler(str_log_file, "a", maxsize, ROTATION_COUNTS, encoding="utf-8")
            if log_type == ROTATION
            else logging.FileHandler(str_log_file, "a", encoding="utf-8")
        )  # type: ignore

    @classmethod
    def _check_and_create_log_file(cls, str_log_file: str) -> None:
        if not os.path.exists(str_log_file):
            try:
                if SysUtil.is_linux_platform():
                    os.mknod(str_log_file)
                else:
                    with open(str_log_file, "w+") as f_handle:
                        f_handle.write("\n")
            except OSError as os_err:
                raise OSError("log file does not exist. try to create it. but file creation failed") from os_err


@_Singleton
class _RootLoggerMan:
    _instance = None
    _rootlogger: Logger | None = None
    _b_rotation = False
    _logfile = ""
    _log_type = ROTATION
    _logger_name: str | None = None
    _LOCK = threading.Lock()

    def __init__(self) -> None:
        pass

    def get_root_logger(self) -> Logger:
        """
        获取 Root logger

        Returns
        -------
        Logger
            root Logger 对象

        Raises
        ------
        LoggerException
            如果 root logger 未初始化，则抛出 LoggerException 异常
        """

        if self._rootlogger is None:
            raise LoggerException("The Cup logger has not been initialized Yet. " + "Call init_comlog() first")

        return self._rootlogger

    def set_rootlogger(
        self,
        logger_name: str,
        logger: Logger,
    ) -> None:
        if self._rootlogger is not None:
            raise LoggerException(
                """WARNING!!! The cup logger has been initialized already
                .Plz do NOT init_comlog twice"""
            )
        self._rootlogger = logger
        self._logger_name = logger_name

    def reset_rootlogger(self, logger) -> None:
        """
        重置logger

        Parameters
        ----------
        logger : Logger
            Logger 对象
        """

        temp_logger = self._rootlogger
        # 移除 handler
        while len(temp_logger.handlers) > 0:  # type: ignore
            temp_logger.removeHandler(temp_logger.handlers[0])  # type: ignore
        del temp_logger
        self._rootlogger = logger
        logging.root = logger

    def is_initialized(self) -> bool:
        """
        是否已经初始化

        Returns
        -------
        bool
            是否初始化，即是否存在 root logger
        """
        return self._rootlogger is not None


def init_comlog(
    logger_name: str,
    loglevel: int = logging.INFO,
    logfile: str = "cup.log",
    log_type: int = ROTATION,
    max_log_size: int = 1073741824,
    is_print_console: bool = False,
    gen_wf: bool = False,
):
    """
    初始化默认logger

    Parameters
    ----------
    logger_name : str
        logger 名称
    loglevel : int, optional
        logger日志等级, by default logging.INFO
    logfile : str, optional
        日志文件名称, by default "cup.log"
    log_type : int, optional
        日志文件类型, by default ROTATION
    max_log_size : int, optional
        日志文件最大大小, by default 1073741824
    is_print_console : bool, optional
        是否显示到控制台, by default False
    gen_wf : bool, optional
        是否创建警告日志文件, by default False
    """
    logger_man = _RootLoggerMan()
    root_logger = logging.getLogger()
    if not logger_man.is_initialized():
        logger_man.set_rootlogger(logger_name, root_logger)
        LogInitializer._check_and_create_log_file(logfile)

        logger_params = LoggerParams(
            loglevel,
            logfile,
            log_type,
            max_log_size,
            is_print_console,
            gen_wf,
            CharPool.VERTICAL_LINE,
        )
        LogInitializer.setup_file_logger(root_logger, logger_params)
        info("-" * 20 + "Log Initialized Successfully" + "-" * 20)
        global G_INITED_LOGGER
        G_INITED_LOGGER.append(logger_name)
    else:
        print(
            f"[{LogInitializer.get_code_file(1)}:{LogInitializer.get_code_line(1)}] \
                init_comlog has been already initialized"
        )


def re_init_comlog(
    logger_name,
    loglevel=logging.INFO,
    logfile="cup.log",
    log_type=ROTATION,
    max_log_size=1073741824,
    is_print_console=False,
    gen_wf=False,
):
    """
    reinitialize default root logger for logging

    :param loggername:
        logger name, should be different from the original one
    """
    # 检查 logger_name 是否已经被使用
    global G_INITED_LOGGER
    if logger_name in G_INITED_LOGGER:
        msg = f"logger name:{logger_name} has been already used!!! Change a name"
        raise ValueError(msg)

    G_INITED_LOGGER.append(logger_name)
    tmp_logger = logging.getLogger(logger_name)
    LogInitializer._check_and_create_log_file(logfile)
    logger_man = _RootLoggerMan()
    logger_params = LoggerParams(
        loglevel,
        logfile,
        log_type,
        max_log_size,
        is_print_console,
        gen_wf,
        CharPool.VERTICAL_LINE,
    )
    LogInitializer.setup_file_logger(tmp_logger, logger_params)
    logger_man.reset_rootlogger(tmp_logger)
    info("-" * 20 + "Log Reinitialized Successfully" + "-" * 20)


def _fail_handle(msg, e):
    print(f"{msg}\nerror:{e}")


def backtrace_info(msg, back_trace_len=0):
    """
    info with backtrace support
    """
    try:
        msg = LogInitializer.log_file_func_info(msg, back_trace_len)
        logger_man = _RootLoggerMan()
        logger_man.get_root_logger().info(msg)
    except LoggerException:
        return
    except Exception as err:
        _fail_handle(msg, err)


def backtrace_debug(msg, back_trace_len=0):
    """
    debug with backtrace support
    """
    try:
        msg = LogInitializer.log_file_func_info(msg, back_trace_len)
        logger_man = _RootLoggerMan()
        logger_man.get_root_logger().debug(msg)
    except LoggerException:
        return
    except Exception as err:
        _fail_handle(msg, err)


def backtrace_warn(msg, back_trace_len=0):
    """
    warning msg with backtrace support
    """
    try:
        msg = LogInitializer.log_file_func_info(msg, back_trace_len)
        logger_man = _RootLoggerMan()
        logger_man.get_root_logger().warning(msg)
    except LoggerException:
        return
    # pylint: disable=broad-except
    except Exception as err:
        _fail_handle(msg, err)


def backtrace_error(msg, back_trace_len=0):
    """
    error msg with backtarce support
    """
    try:
        msg = LogInitializer.log_file_func_info(msg, back_trace_len)
        logger_man = _RootLoggerMan()
        logger_man.get_root_logger().error(msg)
    except LoggerException as log_err:
        _fail_handle(msg, log_err)
    except Exception as err:
        _fail_handle(msg, err)


def backtrace_critical(msg, back_trace_len=0):
    """
    logging.CRITICAL with backtrace support
    """
    try:
        msg = LogInitializer.log_file_func_info(msg, back_trace_len)
        logger_man = _RootLoggerMan()
        logger_man.get_root_logger().critical(msg)
    except LoggerException:
        return
    # pylint:disable=broad-except
    except Exception as err:
        _fail_handle(msg, err)


def set_log_level(logging_level: int) -> None:
    """
    运行时设置loggers的日志级别

    Examples:
    --------
    >>> from core import log
    >>> log.set_log_level(log.DEBUG)     # 设置日志级别为DEBUG

    Parameters
    ----------
    logging_level : int
        日志级别
    """
    logger_man = _RootLoggerMan()
    logger_man.get_root_logger().setLevel(logging_level)


def parse(logline):
    """
    return a dict if the line is valid.
    Otherwise, return None

    :raise Exception:
        ValueError if logline is invalid

    ::

        dict_info:= {
           'loglevel': 'DEBUG',
           'date': '2015-10-14',
           'time': '16:12:22,924',
           'pid': 8808,
           'tid': 1111111,
           'srcline': 'util.py:33',
           'msg': 'this is the log content',
           'tznum': 8,
           'tzstr': 'CST'
        }

    """
    content = logline[logline.rfind("]") + 1 :].strip()
    # content = content[(content.find(']') + 1):]
    # content = content[(content.find(']') + 1):].strip()
    regex = re.compile("[ \t]+")
    items = regex.split(logline)
    loglevel, date, time_, timezone, _, pid_tid, src = items[:7]
    pid, tid = pid_tid.strip("[]").split(":")
    tznum, tzkey = timezone.strip("+)").split("(")
    try:
        return {
            "loglevel": loglevel.strip(":"),
            "date": date,
            "time": time_,
            "pid": pid,
            "tid": tid,
            "srcline": src.strip("[]"),
            "msg": content,
            "tznum": int(tznum),
            "tzkey": tzkey,
        }
    # pylint: disable = W0703
    except Exception as errinfo:
        raise ValueError(errinfo) from errinfo


def info_if(bol, msg, back_trace_len=1):
    """log msg with info loglevel if bol is true"""
    if bol:
        info(msg, back_trace_len)


def error_if(bol, msg, back_trace_len=1):
    """log msg with error loglevel if bol is true"""
    if bol:
        error(msg, back_trace_len)


def warn_if(bol, msg, back_trace_len=1):
    """log msg with error loglevel if bol is true"""
    if bol:
        warn(msg, back_trace_len)


def critical_if(bol, msg, back_trace_len=1):
    """log msg with critical loglevel if bol is true"""
    if bol:
        critical(msg, back_trace_len)


def debug_if(bol, msg, back_trace_len=1):
    """log msg with critical loglevel if bol is true"""
    if bol:
        debug(msg, back_trace_len)


def fatal_if(bol, msg, back_trace_len=1):
    """log msg with info loglevel if bol is true"""
    if bol:
        fatal(msg, back_trace_len)
