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
        
        # 1. Get projects from Database
        db_projects = self.project_repo.get_projects_by_type(project_type)
        projects_map = {p.name: p for p in db_projects}
            
        # 2. Scan Filesystem (Optional/Fallback)
        if base_path and os.path.exists(base_path):
            try:
                for item in os.listdir(base_path):
                    full_path = os.path.join(base_path, item)
                    if os.path.isdir(full_path):
                        if item not in projects_map:
                            # Add from FS if not in DB
                            display_path = f"{project_type}/{item}"
                            projects_map[item] = Project(
                                id=None,
                                name=item,
                                type=project_type,
                                path=display_path
                            )
            except Exception:
                pass
            
        # Return sorted list
        return sorted(projects_map.values(), key=lambda x: x.name)

