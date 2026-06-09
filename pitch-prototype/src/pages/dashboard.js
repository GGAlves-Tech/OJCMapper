import { renderLayout, bindLayout } from '../components/layout.js';
import { showToast } from '../components/toast.js';
import { fetchDrives, mapProject, unmapDrive, unmapAll } from '../mocks/api.js';
import { fetchProjects as fetchProjectsApi } from '../mocks/api.js';

let onlineCache = [];
let gavetaCache = [];

function projectRows(projects) {
  if (!projects.length) {
    return '<tr><td colspan="3" class="px-6 py-12 text-center text-slate-400 italic">Nenhum projeto encontrado.</td></tr>';
  }
  return projects.map((p) => `
    <tr class="hover:bg-blue-50/30 transition-colors">
      <td class="px-6 py-4 font-medium text-slate-800">${p.name}</td>
      <td class="px-6 py-4 text-xs font-mono text-slate-400">${p.path}</td>
      <td class="px-6 py-4 text-right">
        <button data-name="${p.name}" data-path="${p.path}" class="btn-map text-blue-600 font-medium hover:underline">Mapear</button>
      </td>
    </tr>`).join('');
}

export function renderDashboard() {
  const content = `
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <section class="lg:col-span-2">
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden flex flex-col h-full">
          <div class="px-6 border-b border-slate-200 bg-slate-50/50">
            <nav class="-mb-px flex space-x-8">
              <button id="tab-online" class="border-blue-500 text-blue-600 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2">
                Online <span id="count-online" class="bg-blue-100 text-blue-600 py-0.5 px-2 rounded-full text-xs font-bold">0</span>
              </button>
              <button id="tab-gaveta" class="border-transparent text-slate-500 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2">
                Gaveta <span id="count-gaveta" class="bg-slate-100 text-slate-500 py-0.5 px-2 rounded-full text-xs font-bold">0</span>
              </button>
            </nav>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm">
              <thead class="bg-slate-50/50 text-slate-500 font-medium border-b border-slate-200">
                <tr><th class="px-6 py-3">Nome</th><th class="px-6 py-3">Caminho</th><th class="px-6 py-3 text-right">Ação</th></tr>
              </thead>
              <tbody id="projects-tbody" class="divide-y divide-slate-100">
                <tr><td colspan="3" class="px-6 py-8 text-center text-slate-400 italic">Carregando...</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section class="lg:col-span-1">
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden glass">
          <div class="px-6 py-4 border-b border-slate-200 bg-slate-50/50 flex items-center justify-between">
            <h3 class="font-semibold text-slate-800">Unidades Ativas</h3>
            <div class="flex items-center gap-3">
              <button id="btn-refresh" class="text-xs text-slate-400 hover:text-slate-600">↻ Atualizar</button>
              <button id="btn-disconnect-all" class="text-xs text-red-400 hover:text-red-600 font-medium">✕ Desconectar Todas</button>
            </div>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm">
              <thead class="bg-slate-50/50 text-slate-500 font-medium border-b border-slate-200">
                <tr>
                  <th class="px-4 py-3">Letra</th>
                  <th class="px-4 py-3">Caminho</th>
                  <th class="px-4 py-3 text-right">Ação</th>
                </tr>
              </thead>
              <tbody id="unidades-list" class="divide-y divide-slate-100">
                <tr><td colspan="3" class="px-4 py-8 text-center text-slate-400 italic">Carregando...</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>`;

  return renderLayout(content, 'conectar');
}

export function bindDashboard() {
  bindLayout();
  let currentScope = 'online';
  const letterToButton = {};

  async function loadProjectLists() {
    onlineCache = await fetchProjectsApi('online');
    gavetaCache = await fetchProjectsApi('gaveta');
    document.getElementById('count-online').textContent = onlineCache.length;
    document.getElementById('count-gaveta').textContent = gavetaCache.length;
    switchTab(currentScope);
  }

  function switchTab(scope) {
    currentScope = scope;
    const online = scope === 'online';
    document.getElementById('tab-online').className = online
      ? 'border-blue-500 text-blue-600 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2'
      : 'border-transparent text-slate-500 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2';
    document.getElementById('tab-gaveta').className = !online
      ? 'border-blue-500 text-blue-600 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2'
      : 'border-transparent text-slate-500 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2';
    document.getElementById('projects-tbody').innerHTML = projectRows(online ? onlineCache : gavetaCache);
    bindMapButtons();
    syncButtonsWithDrives();
  }

  async function loadDrives() {
    const container = document.getElementById('unidades-list');
    try {
      const drives = await fetchDrives();
      Object.keys(letterToButton).forEach((k) => delete letterToButton[k]);

      if (!drives.length) {
        container.innerHTML = '<tr><td colspan="3" class="px-4 py-8 text-center text-slate-400 italic">Nenhuma unidade mapeada no momento.</td></tr>';
        return;
      }

      container.innerHTML = drives.map((d) => {
        const btn = document.querySelector(`.btn-map[data-name="${d.projectName}"]`);
        const displayPath = btn ? btn.dataset.path : d.path;
        return `
        <tr class="hover:bg-blue-50/30 transition-colors">
          <td class="px-4 py-3 font-bold text-slate-800 whitespace-nowrap">${d.letter}:</td>
          <td class="px-4 py-3 text-xs font-mono text-slate-400 break-all">${displayPath}</td>
          <td class="px-4 py-3 text-right whitespace-nowrap">
            <button data-letter="${d.letter}" class="btn-unmap text-xs text-red-500 font-medium hover:underline">Desconectar</button>
          </td>
        </tr>`;
      }).join('');

      drives.forEach((d) => {
        const btn = document.querySelector(`.btn-map[data-name="${d.projectName}"]`);
        if (btn) {
          btn.disabled = true;
          btn.textContent = `✓ ${d.letter}:`;
          btn.classList.replace('text-blue-600', 'text-green-600');
          letterToButton[`${d.letter}:`] = btn;
        }
      });

      document.querySelectorAll('.btn-unmap').forEach((btn) => {
        btn.addEventListener('click', async () => {
          const letter = btn.dataset.letter;
          btn.disabled = true;
          const data = await unmapDrive(letter);
          showToast(data.message, data.success ? 'success' : 'error');
          if (data.success) {
            const projectBtn = letterToButton[`${letter}:`];
            if (projectBtn) {
              projectBtn.disabled = false;
              projectBtn.textContent = 'Mapear';
              projectBtn.classList.replace('text-green-600', 'text-blue-600');
              delete letterToButton[`${letter}:`];
            }
          }
          loadDrives();
        });
      });
    } catch {
      container.innerHTML = '<tr><td colspan="3" class="px-4 py-8 text-center text-red-400 text-sm">Erro ao carregar unidades.</td></tr>';
    }
  }

  function syncButtonsWithDrives() {
    loadDrives();
  }

  function bindMapButtons() {
    document.querySelectorAll('.btn-map').forEach((btn) => {
      btn.addEventListener('click', async () => {
        const name = btn.dataset.name;
        btn.disabled = true;
        btn.textContent = 'Conectando...';
        const data = await mapProject(name);
        if (data.success) {
          btn.textContent = `✓ ${data.letter}`;
          btn.classList.replace('text-blue-600', 'text-green-600');
          letterToButton[data.letter] = btn;
          showToast(data.message, 'success');
          loadDrives();
        } else {
          btn.disabled = false;
          btn.textContent = 'Mapear';
          showToast(data.message, 'error');
        }
      });
    });
  }

  document.getElementById('tab-online')?.addEventListener('click', () => switchTab('online'));
  document.getElementById('tab-gaveta')?.addEventListener('click', () => switchTab('gaveta'));
  document.getElementById('btn-refresh')?.addEventListener('click', loadDrives);

  let confirmAll = false;
  document.getElementById('btn-disconnect-all')?.addEventListener('click', async (e) => {
    const btn = e.currentTarget;
    if (!confirmAll) {
      confirmAll = true;
      btn.textContent = '⚠ Confirmar?';
      btn.classList.add('text-red-600');
      setTimeout(() => {
        confirmAll = false;
        btn.textContent = '✕ Desconectar Todas';
        btn.classList.remove('text-red-600');
      }, 3000);
      return;
    }
    confirmAll = false;
    const data = await unmapAll();
    showToast(data.message, 'success');
    document.querySelectorAll('.btn-map').forEach((b) => {
      b.disabled = false;
      b.textContent = 'Mapear';
      b.classList.remove('text-green-600');
      b.classList.add('text-blue-600');
    });
    loadDrives();
  });

  bindMapButtons();
  loadProjectLists();
  loadDrives();
}
