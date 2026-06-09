import { renderLayout, bindLayout } from '../components/layout.js';
import { showToast } from '../components/toast.js';
import { exportList } from '../mocks/api.js';

export function renderRelatorios() {
  const content = `
    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden p-8">
      <div class="flex items-center justify-between mb-8 flex-wrap gap-4">
        <div>
          <h3 class="text-lg font-semibold text-slate-900">Relatórios de Projetos</h3>
          <p class="text-slate-500 text-sm">Gere listas exportáveis dos projetos cadastrados no sistema.</p>
        </div>
        <button id="btn-export-csv" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-blue-700 shadow-sm flex items-center gap-2 text-sm">
          Exportar TXT
        </button>
      </div>
      <div id="relatorio-preview" class="p-12 border-2 border-dashed border-slate-200 rounded-2xl text-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 2v-6m-8 13h12a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-slate-900">Nenhum relatório gerado</h3>
        <p class="mt-1 text-sm text-slate-500">Clique para exportar os dados consolidados.</p>
      </div>
    </div>`;

  return renderLayout(content, 'relatorios');
}

export function bindRelatorios() {
  bindLayout();
  document.getElementById('btn-export-csv')?.addEventListener('click', async (e) => {
    const btn = e.currentTarget;
    btn.disabled = true;
    const data = await exportList();
    showToast(data.message, 'success');
    document.getElementById('relatorio-preview').innerHTML = `
      <div class="text-left max-w-lg mx-auto">
        <p class="text-sm font-semibold text-emerald-700 mb-2">Última exportação</p>
        <p class="text-xs font-mono text-slate-600 bg-slate-50 p-4 rounded-lg border">${data.message}</p>
      </div>`;
    btn.disabled = false;
  });
}
