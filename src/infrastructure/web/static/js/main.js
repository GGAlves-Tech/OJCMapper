function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const template = document.getElementById('toast-template');

    if (!container || !template) return;

    const toast = template.content.cloneNode(true).querySelector('.toast-item');
    const iconBg = toast.querySelector('#toast-icon-bg');
    const icon = toast.querySelector('#toast-icon');
    const msgEl = toast.querySelector('#toast-message');

    msgEl.innerText = message;

    if (type === 'success') {
        iconBg.classList.add('bg-green-100', 'text-green-500');
        icon.innerHTML = '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>';
    } else if (type === 'error') {
        iconBg.classList.add('bg-red-100', 'text-red-500');
        icon.innerHTML = '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>';
    } else {
        iconBg.classList.add('bg-blue-100', 'text-blue-500');
        icon.innerHTML = '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>';
    }

    container.appendChild(toast);
    setTimeout(() => { toast.classList.remove('translate-y-10', 'opacity-0'); }, 10);
    setTimeout(() => {
        toast.classList.add('translate-y-10', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('OJCMapper Hexagonal - UI Inicializada');
});
