import logging
import os
from logging import handlers

# logging => é um objeto UNICO no app chamado ROOT LOOGER
# Recebe de uma variavel de ambiente do linux o nivel de mensagens mostradas na tela
# $export LOG_LEVEL= debug/info/warning/error/critical
LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()

# Log Instance (reusable)
log = logging.Logger("Dundie" + __name__)

# ===> FORMATACAO
fmt = logging.Formatter("%(asctime)s %(name)s [%(levelname)s] " "line:%(lineno)d file:%(filename)s: %(message)s")


def get_logger(log_file="dundie.log"):
    """Return a CUSTOM logger"""

    # ===> HANDLER para setar o LEVEL  [ch = console handler] [fh = file hander]
    # handler => classes responsaveis pelo destino onde o Log sera impreso
    # Default => STDERR
    """
    ch = logging.StreamHandler() # envia o STDERR &2> do Linux
    ch.setLevel(logging.DEBUG)
    """
    # logging.handlers.RotatingFileHandler(filename, mode='a', maxBytes=0, backupCount=0,
    #                                      encoding=None, delay=False, errors=None)
    # 10**6 = 1MB
    fh = handlers.RotatingFileHandler(log_file, mode="a", maxBytes=3000000, backupCount=10)

    fh.setLevel(LOG_LEVEL)

    # ch.setFormatter(fmt)
    fh.setFormatter(fmt)

    # ===>  DESTINO
    # log.addHandler(ch)
    log.addHandler(fh)
    return log
