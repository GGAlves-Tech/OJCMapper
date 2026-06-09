import { DEMO_USERS } from '../mocks/data.js';
import { setSession } from '../state.js';
import { showToast } from '../components/toast.js';

export function renderLogin(error = '') {
  return `
    <div class="min-h-[70vh] flex flex-col justify-center py-12">
      <div class="sm:mx-auto sm:w-full sm:max-w-md">
        <div class="w-12 h-12 bg-blue-600 rounded-xl mx-auto flex items-center justify-center shadow-lg shadow-blue-200">
          <span class="text-white font-bold text-xl uppercase">M</span>
        </div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-slate-900">Acesso ao Sistema</h2>
        <p class="mt-2 text-center text-sm text-slate-600">Protótipo para apresentação — credenciais de demo</p>
      </div>

      <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div class="bg-white py-8 px-4 shadow-xl shadow-slate-200 sm:rounded-2xl sm:px-10 border border-slate-100">
          ${error ? `<div class="mb-4 bg-red-50 border-l-4 border-red-400 p-4 rounded-md text-sm text-red-700">${error}</div>` : ''}
          <form id="login-form" class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-slate-700">Usuário</label>
              <input type="text" name="username" required value="admin"
                class="mt-1 block w-full px-3 py-2 border border-slate-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="admin, editor ou user">
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700">Senha</label>
              <input type="password" name="password" required value="admin"
                class="mt-1 block w-full px-3 py-2 border border-slate-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="••••••••">
            </div>
            <button type="submit"
              class="w-full py-2.5 px-4 rounded-lg shadow-sm text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-all active:scale-95">
              Acessar Painel
            </button>
          </form>
          <p class="mt-6 text-center text-xs text-slate-400">admin/admin · editor/editor · user/user</p>
        </div>
      </div>
    </div>`;
}

export function bindLogin(onError) {
  document.getElementById('login-form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const username = fd.get('username').trim();
    const password = fd.get('password');

    const account = DEMO_USERS[username];
    if (!account || account.password !== password) {
      onError('Credenciais inválidas. Use admin/admin para a demo.');
      showToast('Credenciais inválidas.', 'error');
      return;
    }

    setSession({ username, role: account.role });
    showToast(`Bem-vindo, ${username}!`, 'success');
    location.hash = '#/dashboard';
  });
}
