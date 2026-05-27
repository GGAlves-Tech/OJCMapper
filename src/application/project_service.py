import os
from domain import ProjectRepository, SettingsRepository, Project, FileSystemPort, ProjectType


class ProjectUseCase:
    def __init__(self, project_repo: ProjectRepository, settings_repo: SettingsRepository, fs: FileSystemPort):
        self.project_repo = project_repo
        self.settings_repo = settings_repo
        self.fs = fs

    def list_projects_by_type(self, project_type: ProjectType) -> list[Project]:
        settings = self.settings_repo.get_all_settings()
        path_key = 'online_path' if project_type == ProjectType.ONLINE else 'gaveta_path'
        base_path = settings.get(path_key)

        if not base_path or not self.fs.directory_exists(base_path):
            return []

        return [
            Project(id=None, name=item, type=project_type, path=f"{project_type.value}/{item}")
            for item in self.fs.list_directories(base_path)
        ]

    def export_projects_to_txt(self, project_type: ProjectType) -> str:
        projects = self.list_projects_by_type(project_type)
        header = f"RELATÓRIO DE PROJETOS - ESCOPO: {project_type.value}\n"
        header += "=" * 50 + "\n"
        header += f"{'NOME DO PROJETO':<30} | {'CAMINHO':<20}\n"
        header += "-" * 50 + "\n"
        lines = [f"{p.name:<30} | {p.path:<20}" for p in projects]
        footer = "\n" + "=" * 50 + "\n"
        footer += f"Total de projetos: {len(projects)}\n"
        return header + "\n".join(lines) + footer
