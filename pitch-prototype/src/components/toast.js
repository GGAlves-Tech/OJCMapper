export function showToast(message, type = 'success') {
  const toast = document.createElement('div');
  const bg = type === 'success' ? 'bg-green-600' : 'bg-red-600';
  toast.className = `fixed bottom-6 right-6 ${bg} text-white text-sm font-medium px-4 py-3 rounded-xl shadow-lg z-[200] transition-all`;
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 4500);
}
