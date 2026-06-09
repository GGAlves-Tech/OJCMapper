import { renderLayout, bindLayout } from '../components/layout.js';
import { showToast } from '../components/toast.js';
import { fetchSettings, saveSettings } from '../mocks/api.js';
import { SETTINGS_LABELS } from '../mocks/data.js';

export function renderConfigurar() {
  const content = `
    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden p-8">
      <div class="max-w-2xl">
        <h3 class="text-lg font-semibold text-slate-900 mb-4">Configurações do Sistema</h3>
        <p class="text-slate-500 mb-6">Ajuste os parâmetros globais de mapeamento e diretórios.</p>
        <form id="form-config" class="space-y-6">
          <div id="settings-fields" class="grid grid-cols-1 gap-y-6">
            <p class="text-slate-400 italic text-sm">Carregando...</p>
          </div>
          <div class="pt-4 flex justify-end">
            <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500">
              Salvar Configurações
            </button>
          </div>
        </form>
      </div>
    </div>`;

  return renderLayout(content, 'configurar');
}

export function bindConfigurar() {
  bindLayout();

  async function load() {
    const settings = await fetchSettings();
    const container = document.getElementById('settings-fields');
    container.innerHTML = Object.entries(settings).map(([key, value]) => `
      <div>
        <label class="block text-sm font-medium text-slate-700">${SETTINGS_LABELS[key] ?? key}</label>
        <input type="text" name="${key}" value="${value}"
          class="mt-1 block w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:ring-blue-500 focus:border-blue-500">
      </div>`).join('');
  }

  document.getElementById('form-config')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const data = Object.fromEntries(fd.entries());
    const result = await saveSettings(data);
    showToast(result.message, result.success ? 'success' : 'error');
  });

  load();
}
