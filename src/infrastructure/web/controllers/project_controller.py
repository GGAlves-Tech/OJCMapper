import logging
from flask import Blueprint, render_template, session, current_app, request, jsonify
from ..decorators import role_required
from domain import ProjectType

logger = logging.getLogger(__name__)

project_bp = Blueprint('project', __name__)


@project_bp.route('/dashboard')
def dashboard():
    project_service = current_app.project_service
    online_projects = project_service.list_projects_by_type(ProjectType.ONLINE)
    gaveta_projects = project_service.list_projects_by_type(ProjectType.GAVETA)
    return render_template('dashboard.html',
                           online_projects=online_projects,
                           gaveta_projects=gaveta_projects)


@project_bp.route('/mapear', methods=['POST'])
def mapear():
    data = request.get_json()
    project_name = data.get('name', '')
    actor = session.get('username', '')
    success, message, letter = current_app.map_service.map_project(project_name, actor=actor)
    return jsonify({'success': success, 'message': message, 'letter': letter})


@project_bp.route('/desconectar', methods=['POST'])
def desconectar():
    data = request.get_json()
    drive_letter = data.get('letter')
    if not drive_letter:
        return jsonify({'success': False, 'message': 'Letra não informada.'}), 400

    actor = session.get('username', '')
    success, message = current_app.map_service.unmap_project(drive_letter, actor=actor)
    return jsonify({'success': success, 'message': message})


@project_bp.route('/unidades')
def unidades():
    drives = current_app.map_service.get_active_drives()
    return jsonify(drives)


@project_bp.route('/desconectar-todas', methods=['POST'])
def desconectar_todas():
    drives = current_app.map_service.get_active_drives()
    actor = session.get('username', '')
    errors = []
    for drive in drives:
        success, message = current_app.map_service.unmap_project(drive['letter'], actor=actor)
        if not success:
            errors.append(message)
    if errors:
        return jsonify({'success': False, 'message': f'Erros: {"; ".join(errors)}'})
    return jsonify({'success': True, 'message': f'{len(drives)} unidade(s) desconectada(s).'})
