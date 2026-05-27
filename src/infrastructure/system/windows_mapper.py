import logging
import subprocess
import platform
import re
import os
from domain import DriveMapper

logger = logging.getLogger(__name__)

_CANDIDATE_LETTERS = 'FGHIJKLMNOPQRSTUVWXYZ'


def _run_net_use() -> str:
    for enc in ('cp850', 'cp1252', 'utf-8'):
        try:
            result = subprocess.run(
                ['net', 'use'], capture_output=True, text=True, encoding=enc
            )
            return result.stdout
        except Exception:
            continue
    return ''


def _run_subst() -> str:
    try:
        result = subprocess.run(
            ['subst'], capture_output=True, text=True, encoding='cp850'
        )
        return result.stdout
    except Exception:
        return ''


def _parse_mapped_drives(net_use_output: str, subst_output: str) -> list[dict]:
    drives = []

    for line in net_use_output.splitlines():
        match = re.search(r'(\S+)\s+([A-Z]):\s+(\\\\[^\s]+)', line)
        if match:
            drives.append({
                'status': match.group(1),
                'letter': match.group(2),
                'path': match.group(3),
                'type': 'network'
            })

    for line in subst_output.splitlines():
        match = re.search(r'([A-Z]):\\:\s+=>\s+(.+)', line)
        if match:
            drives.append({
                'status': 'OK',
                'letter': match.group(1),
                'path': match.group(2).strip(),
                'type': 'local'
            })

    return drives


class WindowsDriveMapper(DriveMapper):

    def get_available_letter(self) -> str | None:
        try:
            net_out = _run_net_use()
            sub_out = _run_subst()
            drives = _parse_mapped_drives(net_out, sub_out)
            used = set(d['letter'] for d in drives)
            used |= set(re.findall(r'\b([A-Z]):', net_out))
            used |= set(re.findall(r'\b([A-Z]):', sub_out))

            for letter in _CANDIDATE_LETTERS:
                if letter not in used:
                    return letter
        except Exception:
            pass
        return None

    def map_drive(self, drive_letter: str, network_path: str) -> tuple[bool, str]:
        if platform.system() != 'Windows':
            return False, 'Sistema operacional não é Windows.'

        try:
            if not os.path.exists(network_path):
                logger.debug('Criando diretório: %s', network_path)
                os.makedirs(network_path, exist_ok=True)

            drive_letter_clean = drive_letter.rstrip(':')
            is_local = re.match(r'^[A-Z]:', network_path, re.I)

            if is_local:
                cmd = ['subst', f'{drive_letter_clean}:', network_path]
            else:
                cmd = ['net', 'use', f'{drive_letter_clean}:', network_path, '/persistent:no']

            result = subprocess.run(
                cmd, capture_output=True, text=True, encoding='cp850', timeout=10
            )

            logger.debug('Mapeando (%s): returncode=%s', cmd[0], result.returncode)

            if result.returncode == 0:
                return True, f'Unidade {drive_letter_clean}: mapeada → {network_path}'

            error = result.stderr.strip() or result.stdout.strip()
            return False, f'Erro ao mapear: {error}'

        except subprocess.TimeoutExpired:
            return False, 'Timeout: servidor não respondeu.'
        except Exception as e:
            return False, f'Erro inesperado: {str(e)}'

    def unmap_drive(self, drive_letter: str) -> tuple[bool, str]:
        drive_letter_clean = drive_letter.rstrip(':')
        errors = []

        try:
            cmd = ['net', 'use', f'{drive_letter_clean}:', '/delete', '/y']
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='cp850')
            if res.returncode == 0:
                return True, f'Unidade {drive_letter_clean}: desmontada (net use).'
            errors.append(res.stderr.strip())
        except Exception as e:
            errors.append(str(e))

        try:
            cmd = ['subst', f'{drive_letter_clean}:', '/d']
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='cp850')
            if res.returncode == 0:
                return True, f'Unidade {drive_letter_clean}: desmontada (subst).'
            errors.append(res.stderr.strip())
        except Exception as e:
            errors.append(str(e))

        return False, f"Erro ao desmontar {drive_letter_clean}: " + " | ".join(filter(None, errors))

    def get_mapped_drives(self) -> list[dict]:
        try:
            net_out = _run_net_use()
            sub_out = _run_subst()
            logger.debug('[net use raw]: %s', net_out)
            logger.debug('[subst raw]: %s', sub_out)
            return _parse_mapped_drives(net_out, sub_out)
        except Exception:
            return []
