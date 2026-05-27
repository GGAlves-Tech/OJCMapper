from flask import Blueprint, render_template, redirect, url_for, session, current_app, jsonify, request
from ..decorators import role_required
from domain.value_objects import ProjectType
import os
from datetime import datetime

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/usuarios')
@role_required(['Gerente', 'Editor'])
def usuarios():
    if session.get('role') == 'Editor':
        return redirect(url_for('project.dashboard', change_password=1))

    users = current_app.auth_service.get_all_users()
    return render_template('usuarios.html', users=users)


@admin_bp.route('/usuarios/save', methods=['POST'])
@role_required(['Gerente', 'Editor'])
def save_usuario():
    data = request.get_json()
    mode = data.get('mode')
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    current_user = session.get('username')
    current_role = session.get('role')

    if current_role == 'Editor':
        if mode == 'create' or username != current_user:
            return jsonify({'success': False, 'message': 'Acesso negado. Editores só podem alterar a própria senha.'})
        role = current_role

    try:
        if mode == 'create':
            current_app.auth_service.create_user(username, password, role)
            return jsonify({'success': True, 'message': 'Usuário criado com sucesso.'})
        else:
            current_app.auth_service.update_user(username, password, role)
            return jsonify({'success': True, 'message': 'Usuário atualizado com sucesso.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@admin_bp.route('/usuarios/delete', methods=['POST'])
@role_required(['Gerente'])
def delete_usuario():
    data = request.get_json()
    username = data.get('username')

    if username == session.get('username'):
        return jsonify({'success': False, 'message': 'Você não pode excluir sua própria conta.'})

    try:
        current_app.auth_service.delete_user(username)
        return jsonify({'success': True, 'message': 'Usuário removido com sucesso.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@admin_bp.route('/deletar')
@role_required(['Gerente', 'Editor'])
def deletar():
    return render_template('deletar.html')


@admin_bp.route('/deletar/projetos')
@role_required(['Gerente', 'Editor'])
def deletar_projetos():
    scope = ProjectType(request.args.get('scope', 'ONLINE'))
    projects = current_app.project_service.list_projects_by_type(scope)
    return jsonify({'projects': [{'name': p.name, 'path': p.path} for p in projects]})


@admin_bp.route('/deletar/executar', methods=['POST'])
@role_required(['Gerente', 'Editor'])
def deletar_executar():
    data = request.get_json()
    names = data.get('projetos', [])
    scope = ProjectType(data.get('scope', 'ONLINE'))
    result = current_app.delete_service.delete_projects(names, scope)
    return jsonify(result)


@admin_bp.route('/engavetar', methods=['POST'])
@role_required(['Gerente', 'Editor'])
def engavetar():
    data = request.get_json()
    names = data.get('projetos', [])
    result = current_app.delete_service.engavetar_projects(names)
    return jsonify(result)


@admin_bp.route('/exportar-lista', methods=['POST'])
@role_required(['Gerente', 'Editor'])
def exportar_lista():
    result = current_app.export_service.export_media_list()
    return jsonify(result)


@admin_bp.route('/configurar', methods=['GET'])
@role_required(['Gerente'])
def configurar():
    settings = current_app.settings_service.get_settings()
    return render_template('configurar.html', settings=settings)


@admin_bp.route('/configurar/save', methods=['POST'])
@role_required(['Gerente'])
def save_configurar():
    current_app.settings_service.update_all(request.form.to_dict())
    return redirect(url_for('admin.configurar'))
