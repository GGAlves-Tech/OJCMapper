import os
from domain import ProjectRepository, SettingsRepository, Project

class ProjectUseCase:
    def __init__(self, project_repo: ProjectRepository, settings_repo: SettingsRepository):
        self.project_repo = project_repo
        self.settings_repo = settings_repo

    def list_projects_by_type(self, project_type: str):
        settings = self.settings_repo.get_all_settings()
        
        path_key = 'online_path' if project_type == 'ONLINE' else 'gaveta_path'
        base_path = settings.get(path_key)
        
        if not base_path or not os.path.exists(base_path):
            return []
            
        projects = []
        try:
            for item in os.listdir(base_path):
                full_path = os.path.join(base_path, item)
                if os.path.isdir(full_path):
                    # Caminho exibido para o usuário: ONLINE/NomeProjeto
                    display_path = f"{project_type}/{item}"
                    projects.append(Project(
                        id=None,
                        name=item,
                        type=project_type,
                        path=display_path
                    ))
        except Exception:
            # Handle permission errors or other IO issues
            return []
            
        return projects
