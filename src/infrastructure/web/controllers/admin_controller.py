from flask import Blueprint, render_template, redirect, url_for, session, current_app, jsonify, request
from ..decorators import role_required
import os
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/usuarios')
@role_required(['Gerente', 'Editor'])
def usuarios():
    if session.get('role') == 'Editor':
        return redirect(url_for('project.dashboard', change_password=1))
    
    repo = current_app.repo
    users = repo.get_all_users()
    return render_template('usuarios.html', users=users)

@admin_bp.route('/usuarios/save', methods=['POST'])
@role_required(['Gerente', 'Editor'])
def save_usuario():
    data = request.get_json()
    mode = data.get('mode') # 'create' or 'edit'
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    
    current_user = session.get('username')
    current_role = session.get('role')

    # Restrições de segurança
    if current_role == 'Editor':
        # Editor só pode editar a si mesmo e não pode criar usuários
        if mode == 'create' or username != current_user:
            return jsonify({'success': False, 'message': 'Acesso negado. Editores só podem alterar a própria senha.'})
        # Forçar o papel a não mudar
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
@role_required(['Gerente']) # Só Gerente pode deletar
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
    scope = request.args.get('scope', 'ONLINE')
    projects = current_app.project_service.list_projects_by_type(scope)
    return jsonify({'projects': [{'name': p.name, 'path': p.path} for p in projects]})

@admin_bp.route('/deletar/executar', methods=['POST'])
@role_required(['Gerente', 'Editor'])
def deletar_executar():
    data = request.get_json()
    names = data.get('projetos', [])
    scope = data.get('scope', 'ONLINE')
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
    repo = current_app.repo
    settings = repo.get_all_settings()
    av_path = settings.get('av_medias_a_path', '').strip()
    lista_path = settings.get('lista_path', '').strip()

    if not av_path or not os.path.isdir(av_path):
        return jsonify({'success': False, 'message': f'Caminho av_medias_a_path não configurado ou inválido: "{av_path}"'})

    if not lista_path or not os.path.isdir(lista_path):
        return jsonify({'success': False, 'message': f'Caminho de Listas (lista_path) não configurado ou inválido: "{lista_path}"'})

    try:
        items = sorted([
            item for item in os.listdir(av_path)
            if os.path.isdir(os.path.join(av_path, item))
        ])
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro ao listar diretório: {e}'})

    date_str = datetime.now().strftime('%d-%m-%y')
    filename = f'lista_delete_{date_str}.txt'
    output_path = os.path.join(lista_path, filename)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f'Lista de projetos em: {av_path}\n')
            f.write(f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n')
            f.write(f'Total: {len(items)} projeto(s)\n')
            f.write('-' * 60 + '\n')
            for item in items:
                f.write(f'{item}\n')
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro ao gravar arquivo: {e}'})

    return jsonify({'success': True, 'message': f'{len(items)} projeto(s) exportado(s) → {filename}'})

@admin_bp.route('/configurar', methods=['GET'])
@role_required(['Gerente'])
def configurar():
    repo = current_app.repo
    settings = repo.get_all_settings()
    return render_template('configurar.html', settings=settings)

@admin_bp.route('/configurar/save', methods=['POST'])
@role_required(['Gerente'])
def save_configurar():
    repo = current_app.repo

    for key, value in request.form.items():

        repo.update_setting(key, value)

    return redirect(url_for('admin.configurar'))
