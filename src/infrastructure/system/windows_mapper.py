import subprocess
import platform
import re
from .interfaces import DriveMapper

# Letters available for drive mapping (avoid system drives A-E)
_CANDIDATE_LETTERS = 'FGHIJKLMNOPQRSTUVWXYZ'


def _run_net_use() -> str:
    """Runs 'net use' and returns stdout, trying multiple encodings."""
    for enc in ('cp850', 'cp1252', 'utf-8'):
        try:
            result = subprocess.run(
                ['net', 'use'], capture_output=True, text=True, encoding=enc
            )
            return result.stdout
        except Exception:
            continue
    return ''


def _parse_mapped_drives(output: str) -> list[dict]:
    """
    Parses 'net use' output.
    Handles lines like:
      OK           Z:        \\server\share    Microsoft Windows Network
      Desconectado Z:        \\server\share    Microsoft Windows Network
    """
    drives = []
    for line in output.splitlines():
        # Match any non-space status, then a drive letter, then a UNC path
        match = re.search(r'(\S+)\s+([A-Z]):\s+(\\\\[^\s]+)', line)
        if match:
            drives.append({
                'status': match.group(1),
                'letter': match.group(2),
                'path': match.group(3),
            })
    return drives


class WindowsDriveMapper(DriveMapper):

    def get_available_letter(self) -> str | None:
        """Returns the first drive letter not currently in use."""
        try:
            output = _run_net_use()
            used = set(d['letter'] for d in _parse_mapped_drives(output))
            # Also catch any letter followed by colon in the raw output
            used |= set(re.findall(r'\b([A-Z]):', output))
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
            cmd = ['net', 'use', f'{drive_letter}:', network_path, '/persistent:no']
            print(f'Mapeando: {cmd}')
            result = subprocess.run(
                cmd, capture_output=True, text=True, encoding='cp850', timeout=10
            )
            if result.returncode == 0:
                return True, f'Unidade {drive_letter}: mapeada → {network_path}'
            error = result.stderr.strip() or result.stdout.strip()
            return False, f'Erro ao mapear: {error}'
        except subprocess.TimeoutExpired:
            return False, 'Timeout: servidor não respondeu.'
        except Exception as e:
            return False, f'Erro inesperado: {str(e)}'

    def unmap_drive(self, drive_letter: str) -> tuple[bool, str]:
        try:
            cmd = ['net', 'use', f'{drive_letter}:', '/delete', '/y']
            subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='cp850')
            return True, f'Unidade {drive_letter}: desmontada.'
        except subprocess.CalledProcessError as e:
            return False, f'Erro ao desconectar: {e.stderr}'
        except Exception as e:
            return False, f'Erro inesperado: {str(e)}'

    def get_mapped_drives(self) -> list[dict]:
        """Returns [{'letter': 'Z', 'path': '\\\\srv\\proj', 'status': 'OK'}]"""
        try:
            output = _run_net_use()
            print(f'[net use raw]:\n{output}')  # debug
            return _parse_mapped_drives(output)
        except Exception:
            return []
