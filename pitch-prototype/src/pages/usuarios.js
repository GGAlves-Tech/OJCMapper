import { renderLayout, bindLayout } from '../components/layout.js';
import { getSession } from '../state.js';
import { showToast } from '../components/toast.js';
import { fetchUsers, deleteUser } from '../mocks/api.js';
import { openUserModal } from '../components/userModal.js';

function roleBadge(role) {
  const r = role.toLowerCase();
  if (r === 'gerente') return 'bg-purple-100 text-purple-800 border border-purple-200';
  if (r === 'editor') return 'bg-emerald-100 text-emerald-800 border border-emerald-200';
  return 'bg-slate-100 text-slate-800 border border-slate-200';
}

function userRows(users, session) {
  return users.map((user) => {
    const isSelf = user.username === session.username;
    const isEditor = session.role === 'Editor';

    let actions = '';
    if (isSelf) {
      if (!isEditor) {
        actions = `<button disabled class="text-slate-400 font-medium cursor-not-allowed opacity-50 text-sm">Editar</button>
          <button disabled class="text-slate-400 font-medium cursor-not-allowed opacity-50 text-sm">Deletar</button>`;
      } else {
        actions = `<button data-edit="${user.username}" data-role="${user.role}" class="btn-edit text-blue-600 font-medium hover:underline text-sm">Editar</button>
          <button disabled class="text-slate-400 font-medium cursor-not-allowed opacity-50 text-sm">Deletar</button>`;
      }
    } else {
      actions = `<button data-edit="${user.username}" data-role="${user.role}" class="btn-edit text-blue-600 font-medium hover:underline text-sm">Editar</button>
        <button data-delete="${user.username}" class="btn-delete text-red-600 font-medium hover:underline text-sm">Deletar</button>`;
    }

    return `
      <tr class="hover:bg-blue-50/30 transition-colors">
        <td class="px-6 py-4 font-medium text-slate-800">${user.username}</td>
        <td class="px-6 py-4">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${roleBadge(user.role)}">${user.role}</span>
        </td>
        <td class="px-6 py-4 text-right flex justify-end gap-3">${actions}</td>
      </tr>`;
  }).join('');
}

export function renderUsuarios() {
  const session = getSession();
  const isEditor = session.role === 'Editor';

  const content = isEditor ? `
    <div class="flex flex-col items-center justify-center py-12 text-slate-500">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mb-4 opacity-20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
      </svg>
      <p class="text-lg font-medium">Área de Autogerenciamento</p>
      <p class="text-sm mb-6">Utilize o botão abaixo para atualizar sua senha.</p>
      <button id="btn-edit-self" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-blue-700 text-sm">Alterar Minha Senha</button>
    </div>` : `
    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      <div class="px-6 py-4 border-b border-slate-200 bg-slate-50/50 flex items-center justify-between">
        <h3 class="font-semibold text-slate-800">Gestão de Usuários</h3>
        <button id="btn-novo-usuario" class="bg-blue-600 text-white px-3 py-1.5 rounded-lg text-sm font-semibold hover:bg-blue-700 shadow-sm">+ Novo Usuário</button>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="bg-slate-50 text-slate-500 font-medium border-b border-slate-200">
            <tr>
              <th class="px-6 py-3">Usuário</th>
              <th class="px-6 py-3">Perfil</th>
              <th class="px-6 py-3 text-right">Ação</th>
            </tr>
          </thead>
          <tbody id="users-tbody" class="divide-y divide-slate-100">
            <tr><td colspan="3" class="px-6 py-8 text-center text-slate-400 italic">Carregando...</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <div id="modal-confirm-delete" class="hidden fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[110] flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm overflow-hidden">
        <div class="p-6 text-center">
          <h3 class="text-lg font-bold text-slate-800 mb-2">Remover Usuário</h3>
          <p class="text-sm text-slate-500">Remover <span id="span-delete-user" class="font-bold text-slate-800"></span>? Irreversível.</p>
        </div>
        <div class="p-4 bg-slate-50 flex gap-2 justify-center">
          <button id="btn-cancel-delete" class="px-4 py-2 rounded-lg font-semibold text-slate-600 hover:bg-slate-200">Cancelar</button>
          <button id="btn-confirm-delete" class="bg-red-600 text-white px-6 py-2 rounded-lg font-bold hover:bg-red-700">Remover</button>
        </div>
      </div>
    </div>`;

  return renderLayout(content, 'usuarios');
}

export function bindUsuarios() {
  bindLayout();
  const session = getSession();
  let userToDelete = null;

  async function refresh() {
    if (session.role === 'Editor') return;
    const users = await fetchUsers();
    document.getElementById('users-tbody').innerHTML = userRows(users, session);
    bindTableActions();
  }

  function bindTableActions() {
    document.querySelectorAll('.btn-edit').forEach((btn) => {
      btn.addEventListener('click', () => {
        openUserModal('edit', { username: btn.dataset.edit, role: btn.dataset.role }, refresh);
      });
    });
    document.querySelectorAll('.btn-delete').forEach((btn) => {
      btn.addEventListener('click', () => {
        userToDelete = btn.dataset.delete;
        document.getElementById('span-delete-user').textContent = userToDelete;
        document.getElementById('modal-confirm-delete').classList.remove('hidden');
      });
    });
  }

  document.getElementById('btn-novo-usuario')?.addEventListener('click', () => {
    openUserModal('create', null, refresh);
  });

  document.getElementById('btn-edit-self')?.addEventListener('click', () => {
    openUserModal('edit', { username: session.username, role: session.role });
  });

  document.getElementById('btn-cancel-delete')?.addEventListener('click', () => {
    document.getElementById('modal-confirm-delete')?.classList.add('hidden');
  });

  document.getElementById('btn-confirm-delete')?.addEventListener('click', async () => {
    if (userToDelete === session.username) {
      showToast('Você não pode excluir sua própria conta.', 'error');
      return;
    }
    const data = await deleteUser(userToDelete);
    showToast(data.message, data.success ? 'success' : 'error');
    document.getElementById('modal-confirm-delete')?.classList.add('hidden');
    if (data.success) refresh();
  });

  refresh();
}
