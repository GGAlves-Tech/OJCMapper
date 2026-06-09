import { renderLayout, bindLayout } from '../components/layout.js';
import { showToast } from '../components/toast.js';
import {
  fetchDeleteProjects,
  deleteProjects,
  engavetarProjects,
  exportList,
} from '../mocks/api.js';

export function renderDeletar() {
  const content = `
    <div class="flex justify-between items-center mb-4 flex-wrap gap-3">
      <div class="flex gap-2 p-1 bg-slate-100 rounded-xl">
        <button id="tab-online" class="px-6 py-2 rounded-lg text-sm font-semibold transition-all bg-white text-blue-600 shadow-sm">ONLINE</button>
        <button id="tab-gaveta" class="px-6 py-2 rounded-lg text-sm font-semibold transition-all text-slate-500 hover:text-slate-700">GAVETA</button>
      </div>
      <button id="btn-exportar" class="bg-emerald-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-emerald-700 transition-all shadow-sm flex items-center gap-2 text-sm">
        Exportar Relatório
      </button>
    </div>

    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      <div class="p-6 border-b border-slate-200 bg-slate-50/50 flex flex-wrap justify-between items-center gap-4">
        <div>
          <h3 class="font-semibold text-slate-800">Gerenciar Projetos</h3>
          <p class="text-sm text-slate-500">Selecione projetos para deletar (permanente) ou engavetar.</p>
        </div>
        <div class="flex gap-3">
          <button id="btn-engavetar" disabled class="bg-amber-500 text-white px-4 py-2 rounded-lg font-semibold hover:bg-amber-600 transition-all shadow-sm text-sm disabled:opacity-50 disabled:cursor-not-allowed">
            Engavetar <span id="count-engavetar"></span>
          </button>
          <button id="btn-deletar-modal" disabled class="bg-red-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-red-700 transition-all shadow-sm text-sm disabled:opacity-50 disabled:cursor-not-allowed">
            Deletar <span id="count-deletar"></span>
          </button>
        </div>
      </div>

      <div class="overflow-x-auto min-h-[400px] relative">
        <table class="min-w-full divide-y divide-slate-200">
          <thead class="bg-slate-50/50">
            <tr>
              <th class="px-6 py-3 text-left">
                <input type="checkbox" id="select-all" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500 h-4 w-4">
              </th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase">Projeto</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase">Caminho</th>
            </tr>
          </thead>
          <tbody id="lista-corpo" class="bg-white divide-y divide-slate-100"></tbody>
        </table>
        <div id="loading-list" class="hidden py-24 text-center absolute inset-0 bg-white/80">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-slate-200 border-t-blue-600"></div>
          <p class="mt-4 text-slate-500">Buscando projetos...</p>
        </div>
        <div id="empty-list" class="hidden py-24 text-center">
          <p class="text-slate-500">Nenhum projeto encontrado neste escopo.</p>
        </div>
      </div>
    </div>

    <div id="modal-deletar" class="hidden fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden">
        <div class="p-6 border-b border-slate-100 bg-red-50">
          <h3 class="text-lg font-bold text-red-700">Confirmar Exclusão Permanente</h3>
        </div>
        <div class="p-6">
          <p class="text-slate-600 mb-4">Você está prestes a excluir os seguintes projetos permanentemente:</p>
          <div id="modal-list-names" class="max-h-48 overflow-y-auto bg-slate-50 rounded-xl p-4 border border-slate-200 mb-4"></div>
          <p class="text-sm font-bold text-red-600">Esta ação não pode ser desfeita!</p>
        </div>
        <div class="p-6 bg-slate-50 flex gap-3 justify-end">
          <button id="btn-cancel-modal" class="px-6 py-2 rounded-lg font-semibold text-slate-700 hover:bg-slate-200">Cancelar</button>
          <button id="btn-confirmar-delecao" class="bg-red-600 text-white px-6 py-2 rounded-lg font-bold hover:bg-red-700">Confirmar e Deletar</button>
        </div>
      </div>
    </div>`;

  return renderLayout(content, 'deletar');
}

export function bindDeletar() {
  bindLayout();
  let currentScope = 'ONLINE';
  let selectedNames = [];

  async function loadProjetos() {
    const tbody = document.getElementById('lista-corpo');
    const loading = document.getElementById('loading-list');
    const empty = document.getElementById('empty-list');
    const selectAll = document.getElementById('select-all');

    tbody.innerHTML = '';
    loading.classList.remove('hidden');
    empty.classList.add('hidden');
    selectAll.checked = false;
    selectedNames = [];
    updateButtons();

    const data = await fetchDeleteProjects(currentScope);
    loading.classList.add('hidden');

    if (!data.projects?.length) {
      empty.classList.remove('hidden');
      return;
    }

    tbody.innerHTML = data.projects.map((p) => `
      <tr class="hover:bg-slate-50/50 transition-colors cursor-pointer project-row" data-name="${p.name}">
        <td class="px-6 py-4 whitespace-nowrap">
          <input type="checkbox" class="project-check rounded border-slate-300 text-blue-600 h-4 w-4" value="${p.name}">
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-800">${p.name}</td>
        <td class="px-6 py-4 whitespace-nowrap text-xs font-mono text-slate-500">${p.path}</td>
      </tr>`).join('');

    document.querySelectorAll('.project-row').forEach((row) => {
      row.addEventListener('click', (e) => {
        if (e.target.tagName === 'INPUT') return;
        const check = row.querySelector('.project-check');
        check.checked = !check.checked;
        syncSelection();
      });
    });
    document.querySelectorAll('.project-check').forEach((c) => {
      c.addEventListener('change', syncSelection);
      c.addEventListener('click', (e) => e.stopPropagation());
    });
  }

  function syncSelection() {
    selectedNames = [...document.querySelectorAll('.project-check:checked')].map((c) => c.value);
    updateButtons();
  }

  function updateButtons() {
    const count = selectedNames.length;
    document.getElementById('btn-deletar-modal').disabled = count === 0;
    document.getElementById('btn-engavetar').disabled = count === 0;
    document.getElementById('count-deletar').textContent = count > 0 ? `(${count})` : '';
    document.getElementById('count-engavetar').textContent = count > 0 ? `(${count})` : '';
  }

  function setScope(scope) {
    currentScope = scope;
    const active = 'px-6 py-2 rounded-lg text-sm font-semibold transition-all bg-white text-blue-600 shadow-sm';
    const inactive = 'px-6 py-2 rounded-lg text-sm font-semibold transition-all text-slate-500 hover:text-slate-700';
    document.getElementById('tab-online').className = scope === 'ONLINE' ? active : inactive;
    document.getElementById('tab-gaveta').className = scope === 'GAVETA' ? active : inactive;
    document.getElementById('btn-engavetar').classList.toggle('hidden', scope !== 'ONLINE');
    loadProjetos();
  }

  document.getElementById('tab-online')?.addEventListener('click', () => setScope('ONLINE'));
  document.getElementById('tab-gaveta')?.addEventListener('click', () => setScope('GAVETA'));

  document.getElementById('select-all')?.addEventListener('change', (e) => {
    document.querySelectorAll('.project-check').forEach((c) => { c.checked = e.target.checked; });
    syncSelection();
  });

  document.getElementById('btn-exportar')?.addEventListener('click', async (e) => {
    const btn = e.currentTarget;
    btn.disabled = true;
    const data = await exportList();
    showToast(data.message, data.success ? 'success' : 'error');
    btn.disabled = false;
  });

  document.getElementById('btn-deletar-modal')?.addEventListener('click', () => {
    document.getElementById('modal-list-names').innerHTML = selectedNames
      .map((n) => `<div class="py-1 text-sm text-slate-700 font-medium border-b border-slate-200 last:border-0">${n}</div>`)
      .join('');
    document.getElementById('modal-deletar').classList.remove('hidden');
  });

  document.getElementById('btn-cancel-modal')?.addEventListener('click', () => {
    document.getElementById('modal-deletar').classList.add('hidden');
  });

  document.getElementById('btn-confirmar-delecao')?.addEventListener('click', async (e) => {
    const btn = e.currentTarget;
    btn.disabled = true;
    const data = await deleteProjects(selectedNames, currentScope);
    document.getElementById('modal-deletar').classList.add('hidden');
    showToast(data.message, data.success ? 'success' : 'error');
    btn.disabled = false;
    loadProjetos();
  });

  document.getElementById('btn-engavetar')?.addEventListener('click', async (e) => {
    const btn = e.currentTarget;
    btn.disabled = true;
    const data = await engavetarProjects(selectedNames);
    showToast(data.message, data.success ? 'success' : 'error');
    btn.disabled = false;
    loadProjetos();
  });

  setScope('ONLINE');
}
