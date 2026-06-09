import { getSession } from '../state.js';
import { saveUser } from '../mocks/api.js';
import { showToast } from './toast.js';

let mode = 'create';
let onSaved = null;

const MODAL_HTML = `
<div id="modal-usuario" class="hidden fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
  <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
    <div class="p-6 border-b border-slate-100">
      <h3 id="modal-title" class="text-lg font-bold text-slate-800">Novo Usuário</h3>
    </div>
    <div class="p-6 space-y-4 text-left">
      <div>
        <label class="block text-sm font-medium text-slate-700 mb-1">Usuário</label>
        <input type="text" id="input-username" class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:ring-blue-500 focus:border-blue-500" placeholder="Nome de usuário">
      </div>
      <div>
        <label class="block text-sm font-medium text-slate-700 mb-1">Perfil</label>
        <select id="select-role" class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:ring-blue-500 focus:border-blue-500">
          <option value="">Selecione um perfil...</option>
          <option value="Gerente">Gerente</option>
          <option value="Editor">Editor</option>
          <option value="Default">Default</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-slate-700 mb-1">Senha Inicial</label>
        <input type="password" id="input-password" class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:ring-blue-500 focus:border-blue-500" placeholder="Senha">
      </div>
    </div>
    <div class="p-6 bg-slate-50 flex gap-3 justify-end text-sm">
      <button id="btn-cancel-user" class="px-4 py-2 rounded-lg font-semibold text-slate-600 hover:bg-slate-200">Cancelar</button>
      <button id="btn-salvar-usuario" disabled class="bg-blue-600 text-white px-6 py-2 rounded-lg font-bold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed">Salvar</button>
    </div>
  </div>
</div>`;

function ensureModal() {
  if (!document.getElementById('modal-usuario')) {
    document.body.insertAdjacentHTML('beforeend', MODAL_HTML);
    document.getElementById('btn-cancel-user')?.addEventListener('click', closeUserModal);
    document.getElementById('btn-salvar-usuario')?.addEventListener('click', handleSave);
    ['input-username', 'select-role', 'input-password'].forEach((id) => {
      document.getElementById(id)?.addEventListener('input', validateForm);
      document.getElementById(id)?.addEventListener('change', validateForm);
    });
  }
}

function validateForm() {
  const u = document.getElementById('input-username')?.value.trim();
  const r = document.getElementById('select-role')?.value;
  const p = document.getElementById('input-password')?.value.trim();
  const btn = document.getElementById('btn-salvar-usuario');
  if (btn) btn.disabled = !(u && r && p);
}

export function openUserModal(openMode, user = null, callback = null) {
  ensureModal();
  mode = openMode;
  onSaved = callback;
  const session = getSession();
  const isEditor = session?.role === 'Editor';

  const title = document.getElementById('modal-title');
  const inputUser = document.getElementById('input-username');
  const selectRole = document.getElementById('select-role');
  const inputPass = document.getElementById('input-password');

  if (openMode === 'create') {
    title.textContent = 'Novo Usuário';
    inputUser.value = '';
    inputUser.disabled = false;
    selectRole.value = '';
    selectRole.disabled = false;
    inputPass.value = '';
  } else {
    title.textContent = isEditor ? 'Alterar Minha Senha' : 'Editar Usuário';
    inputUser.value = user?.username ?? '';
    inputUser.disabled = true;
    selectRole.value = user?.role ?? '';
    selectRole.disabled = isEditor;
    inputPass.value = '';
  }

  validateForm();
  document.getElementById('modal-usuario').classList.remove('hidden');
}

export function closeUserModal() {
  document.getElementById('modal-usuario')?.classList.add('hidden');
}

async function handleSave() {
  const username = document.getElementById('input-username').value.trim();
  const role = document.getElementById('select-role').value;
  const password = document.getElementById('input-password').value.trim();
  const session = getSession();

  if (session?.role === 'Editor' && (mode === 'create' || username !== session.username)) {
    showToast('Acesso negado. Editores só podem alterar a própria senha.', 'error');
    return;
  }

  const data = await saveUser(mode, username, password, role);
  showToast(data.message, data.success ? 'success' : 'error');
  if (data.success) {
    closeUserModal();
    onSaved?.();
  }
}
