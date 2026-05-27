import os
from domain import ProjectRepository, SettingsRepository, Project
from domain.value_objects import ProjectType


class ProjectUseCase:
    def __init__(self, project_repo: ProjectRepository, settings_repo: SettingsRepository):
        self.project_repo = project_repo
        self.settings_repo = settings_repo

    def list_projects_by_type(self, project_type: ProjectType):
        settings = self.settings_repo.get_all_settings()

        path_key = 'online_path' if project_type == ProjectType.ONLINE else 'gaveta_path'
        base_path = settings.get(path_key)

        if not base_path or not os.path.exists(base_path):
            return []

        projects = []
        try:
            for item in os.listdir(base_path):
                full_path = os.path.join(base_path, item)
                if os.path.isdir(full_path):
                    display_path = f"{project_type.value}/{item}"
                    projects.append(Project(
                        id=None,
                        name=item,
                        type=project_type,
                        path=display_path
                    ))
        except Exception:
            return []

        return projects

    def export_projects_to_txt(self, project_type: ProjectType) -> str:
        projects = self.list_projects_by_type(project_type)
        header = f"RELATÓRIO DE PROJETOS - ESCOPO: {project_type.value}\n"
        header += "="*50 + "\n"
        header += f"{'NOME DO PROJETO':<30} | {'CAMINHO':<20}\n"
        header += "-"*50 + "\n"
        
        lines = []
        for p in projects:
            lines.append(f"{p.name:<30} | {p.path:<20}")
            
        footer = "\n" + "="*50 + "\n"
        footer += f"Total de projetos: {len(projects)}\n"
        
        return header + "\n".join(lines) + footer
