import logging
from typing import Optional
from domain import SettingsRepository
from domain.audit.audit_port import AuditPort

logger = logging.getLogger(__name__)


class SettingsUseCase:
    def __init__(self, settings_repo: SettingsRepository, audit: Optional[AuditPort] = None):
        self.settings_repo = settings_repo
        self.audit = audit

    def get_settings(self) -> dict:
        return self.settings_repo.get_all_settings()

    def update_all(self, data: dict, actor: str = '') -> None:
        for key, value in data.items():
            self.settings_repo.update_setting(key, value)
        if self.audit:
            self.audit.log(actor, 'configuracoes-atualizadas')
