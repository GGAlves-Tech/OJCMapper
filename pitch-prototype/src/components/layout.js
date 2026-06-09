import { getSession, clearSession } from '../state.js';

export function renderLayout(contentHtml, activeTab = 'conectar') {
  const user = getSession();
  const tabs = [
    { id: 'conectar', label: 'Conectar', hash: '#/dashboard' },
    { id: 'deletar', label: 'Deletar', hash: '#/deletar', roles: ['Gerente', 'Editor'] },
    { id: 'usuarios', label: 'Usuários', hash: '#/usuarios', roles: ['Gerente', 'Editor'] },
    { id: 'configurar', label: 'Configurar', hash: '#/configurar', roles: ['Gerente'] },
    { id: 'relatorios', label: 'Relatórios', hash: '#/relatorios', roles: ['Gerente', 'Editor'] },
  ];

  const visibleTabs = tabs.filter((t) => !t.roles || t.roles.includes(user.role));

  return `
    <div class="h-full flex flex-col">
      <header class="sticky top-0 z-50 glass shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16 items-center">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-lg shadow-sm bg-blue-600 flex items-center justify-center text-white font-bold text-sm">M</div>
              <h1 class="text-xl font-bold tracking-tight text-slate-900">
                MAPPER <span class="text-blue-600">OJC</span>
                <span class="ml-2 text-[10px] font-semibold uppercase tracking-wider text-amber-600 bg-amber-50 px-2 py-0.5 rounded-full border border-amber-100">Pitch</span>
              </h1>
            </div>
            <div class="flex items-center gap-3 sm:gap-4">
              <div class="text-sm text-slate-600 flex items-center gap-2">
                <span class="font-semibold text-slate-900">${user.username}</span>
                <span class="bg-blue-50 text-blue-700 px-2.5 py-0.5 rounded-full text-[10px] font-bold border border-blue-100 uppercase tracking-wider">${user.role}</span>
              </div>
              <div class="h-4 w-px bg-slate-200"></div>
              <button id="btn-logout" class="text-slate-400 hover:text-red-500 transition-colors text-xs font-medium hover:underline">Sair</button>
            </div>
          </div>
        </div>
      </header>

      <main class="flex-grow">
        <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <div class="mb-6 border-b border-slate-200">
            <nav class="-mb-px flex space-x-4 sm:space-x-8 overflow-x-auto">
              ${visibleTabs.map((t) => `
                <a href="${t.hash}" data-tab="${t.id}"
                  class="${activeTab === t.id ? 'border-blue-500 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'} whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-all">
                  ${t.label}
                </a>`).join('')}
            </nav>
          </div>
          ${contentHtml}
        </div>
      </main>

      <footer class="bg-white border-t border-slate-200 py-6">
        <div class="max-w-7xl mx-auto px-4 text-center text-sm text-slate-500">
          <p>&copy; 2026 MAPPER — Protótipo Pitch · TV Anhanguera / UNITINS</p>
        </div>
      </footer>
    </div>`;
}

export function bindLayout() {
  document.getElementById('btn-logout')?.addEventListener('click', () => {
    clearSession();
    location.hash = '#/login';
  });
}

export function canAccess(route, role) {
  const rules = {
    '#/dashboard': () => true,
    '#/deletar': () => ['Gerente', 'Editor'].includes(role),
    '#/usuarios': () => ['Gerente', 'Editor'].includes(role),
    '#/configurar': () => role === 'Gerente',
    '#/relatorios': () => ['Gerente', 'Editor'].includes(role),
  };
  return rules[route]?.() ?? false;
}
