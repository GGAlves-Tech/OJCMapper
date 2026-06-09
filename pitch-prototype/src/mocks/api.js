import {
  ONLINE_PROJECTS,
  GAVETA_PROJECTS,
  DEFAULT_SETTINGS,
} from './data.js';

const LETTERS = 'FGHIJKLMNOPQRSTUVWXYZ'.split('');

let mappedDrives = [];
let onlineProjects = [...ONLINE_PROJECTS];
let gavetaProjects = [...GAVETA_PROJECTS];
let users = [
  { username: 'admin', role: 'Gerente' },
  { username: 'editor', role: 'Editor' },
  { username: 'user', role: 'Default' },
];
let settings = { ...DEFAULT_SETTINGS };

const delay = (ms) => new Promise((r) => setTimeout(r, ms));

function nextLetter() {
  const used = new Set(mappedDrives.map((d) => d.letter));
  return LETTERS.find((l) => !used.has(l)) ?? null;
}

function projectsByScope(scope) {
  return scope === 'ONLINE' || scope === 'online' ? onlineProjects : gavetaProjects;
}

export async function fetchProjects(scope) {
  await delay(300);
  const key = scope === 'online' ? 'online' : 'gaveta';
  return key === 'online' ? [...onlineProjects] : [...gavetaProjects];
}

export async function fetchDeleteProjects(scope) {
  await delay(400);
  return { projects: projectsByScope(scope).map((p) => ({ ...p })) };
}

export async function deleteProjects(names, scope) {
  await delay(800);
  const list = projectsByScope(scope);
  const done = [];
  const failed = [];
  names.forEach((name) => {
    const idx = list.findIndex((p) => p.name === name);
    if (idx >= 0) {
      list.splice(idx, 1);
      done.push(name);
      mappedDrives = mappedDrives.filter((d) => d.projectName !== name);
    } else {
      failed.push(name);
    }
  });
  return {
    success: failed.length === 0,
    message: failed.length
      ? `Excluídos: ${done.length}. Falhas: ${failed.join(', ')}`
      : `${done.length} projeto(s) excluído(s) permanentemente.`,
    done,
    failed,
  };
}

export async function engavetarProjects(names) {
  await delay(800);
  const done = [];
  const failed = [];
  names.forEach((name) => {
    const idx = onlineProjects.findIndex((p) => p.name === name);
    if (idx >= 0) {
      const [p] = onlineProjects.splice(idx, 1);
      gavetaProjects.push({ name: p.name, path: `GAVETA/${p.name}` });
      done.push(name);
    } else {
      failed.push(name);
    }
  });
  return {
    success: failed.length === 0,
    message: failed.length
      ? `Engavetados: ${done.length}. Falhas: ${failed.join(', ')}`
      : `${done.length} projeto(s) movido(s) para Gaveta.`,
    done,
    failed,
  };
}

export async function exportList() {
  await delay(600);
  const lines = onlineProjects.map((p) => p.name);
  return {
    success: true,
    message: `Lista exportada: ${lines.length} projetos Online → W:/Lists/projetos_online.txt`,
  };
}

export async function mapProject(name) {
  await delay(900);
  if (!name) return { success: false, message: 'Nome do projeto não informado.', letter: '' };

  const letter = nextLetter();
  if (!letter) return { success: false, message: 'Nenhuma letra de unidade disponível.', letter: '' };

  const already = mappedDrives.find((d) => d.projectName === name);
  if (already) {
    return { success: false, message: `Projeto já mapeado em ${already.letter}:`, letter: '' };
  }

  const path = `${settings.av_medias_a_path}\\${name}`.replace(/\//g, '\\');
  mappedDrives.push({ letter, path, projectName: name, type: 'local', status: 'OK' });

  return {
    success: true,
    message: `Unidade ${letter}: mapeada → ${path}`,
    letter: `${letter}:`,
  };
}

export async function unmapDrive(letter) {
  await delay(500);
  const clean = letter.replace(':', '');
  const idx = mappedDrives.findIndex((d) => d.letter === clean);
  if (idx === -1) return { success: false, message: 'Unidade não encontrada.' };

  mappedDrives.splice(idx, 1);
  return { success: true, message: `Unidade ${clean}: desmontada (subst).` };
}

export async function fetchDrives() {
  await delay(200);
  return mappedDrives.map((d) => ({ ...d }));
}

export async function unmapAll() {
  await delay(700);
  const count = mappedDrives.length;
  mappedDrives = [];
  return { success: true, message: `${count} unidade(s) desconectada(s).` };
}

export async function fetchUsers() {
  await delay(300);
  return users.map((u) => ({ ...u }));
}

export async function saveUser(mode, username, password, role) {
  await delay(500);
  if (mode === 'create') {
    if (users.some((u) => u.username === username)) {
      return { success: false, message: 'Usuário já existe.' };
    }
    users.push({ username, role });
    return { success: true, message: 'Usuário criado com sucesso.' };
  }
  const user = users.find((u) => u.username === username);
  if (!user) return { success: false, message: 'Usuário não encontrado.' };
  user.role = role;
  return { success: true, message: 'Usuário atualizado com sucesso.' };
}

export async function deleteUser(username) {
  await delay(500);
  const idx = users.findIndex((u) => u.username === username);
  if (idx === -1) return { success: false, message: 'Usuário não encontrado.' };
  users.splice(idx, 1);
  return { success: true, message: 'Usuário removido com sucesso.' };
}

export async function fetchSettings() {
  await delay(200);
  return { ...settings };
}

export async function saveSettings(data) {
  await delay(500);
  settings = { ...settings, ...data };
  return { success: true, message: 'Configurações salvas com sucesso.' };
}

export function resetDemo() {
  mappedDrives = [];
  onlineProjects = [...ONLINE_PROJECTS];
  gavetaProjects = [...GAVETA_PROJECTS];
  users = [
    { username: 'admin', role: 'Gerente' },
    { username: 'editor', role: 'Editor' },
    { username: 'user', role: 'Default' },
  ];
  settings = { ...DEFAULT_SETTINGS };
}
