import logging
import os
import socket
from datetime import date, datetime
from typing import Callable, Optional
from domain.audit.audit_port import AuditPort


class FileAuditLogger(AuditPort):
    """Grava entradas de auditoria em {hostname}_{data}.log.

    log_dir_provider é chamado a cada escrita, permitindo que mudanças
    em log_path nas configurações tomem efeito imediatamente.
    """

    def __init__(self, log_dir_provider: Callable[[], str]):
        self._log_dir_provider = log_dir_provider
        self._hostname = socket.gethostname()
        self._current_key: Optional[tuple] = None
        self._logger: Optional[logging.Logger] = None

    def _get_logger(self) -> logging.Logger:
        today = date.today()
        log_dir = self._log_dir_provider()
        key = (today, log_dir)

        if key != self._current_key:
            os.makedirs(log_dir, exist_ok=True)
            name = f'audit.{self._hostname}.{today}.{hash(log_dir)}'
            logger = logging.getLogger(name)
            if not logger.handlers:
                path = os.path.join(log_dir, f'{self._hostname}_{today}.log')
                handler = logging.FileHandler(path, encoding='utf-8')
                handler.setFormatter(logging.Formatter('%(message)s'))
                logger.addHandler(handler)
                logger.setLevel(logging.INFO)
                logger.propagate = False
            self._logger = logger
            self._current_key = key

        return self._logger

    def log(self, actor: str, action: str) -> None:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._get_logger().info(f'{now}_{actor}_{action}')
