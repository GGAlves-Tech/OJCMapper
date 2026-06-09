import './style.css';
import { getSession } from './state.js';
import { renderLogin, bindLogin } from './pages/login.js';
import { renderDashboard, bindDashboard } from './pages/dashboard.js';
import { renderDeletar, bindDeletar } from './pages/deletar.js';
import { renderUsuarios, bindUsuarios } from './pages/usuarios.js';
import { renderConfigurar, bindConfigurar } from './pages/configurar.js';
import { renderRelatorios, bindRelatorios } from './pages/relatorios.js';
import { canAccess } from './components/layout.js';
import { showToast } from './components/toast.js';

const app = document.getElementById('app');
let loginError = '';

function render() {
  const hash = location.hash || '#/login';
  const session = getSession();

  if (!session && hash !== '#/login') {
    location.hash = '#/login';
    return;
  }

  if (hash === '#/login' || !session) {
    app.innerHTML = renderLogin(loginError);
    bindLogin((msg) => {
      loginError = msg;
      render();
    });
    loginError = '';
    return;
  }

  if (!canAccess(hash, session.role)) {
    showToast('Acesso negado para este perfil.', 'error');
    location.hash = '#/dashboard';
    return;
  }

  switch (hash) {
    case '#/dashboard':
      app.innerHTML = renderDashboard();
      bindDashboard();
      break;
    case '#/deletar':
      app.innerHTML = renderDeletar();
      bindDeletar();
      break;
    case '#/usuarios':
      app.innerHTML = renderUsuarios();
      bindUsuarios();
      break;
    case '#/configurar':
      app.innerHTML = renderConfigurar();
      bindConfigurar();
      break;
    case '#/relatorios':
      app.innerHTML = renderRelatorios();
      bindRelatorios();
      break;
    default:
      location.hash = '#/dashboard';
  }
}

window.addEventListener('hashchange', render);
render();
