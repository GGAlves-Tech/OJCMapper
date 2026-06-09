export const ONLINE_PROJECTS = [
  { name: 'Jornal_Tarde_08JUN', path: 'ONLINE/Jornal_Tarde_08JUN' },
  { name: 'VT_Reporter_Campo', path: 'ONLINE/VT_Reporter_Campo' },
  { name: 'Entrevista_Governador_TO', path: 'ONLINE/Entrevista_Governador_TO' },
  { name: 'Materia_Policial_Palmas', path: 'ONLINE/Materia_Policial_Palmas' },
  { name: 'Esporte_No_Ar', path: 'ONLINE/Esporte_No_Ar' },
];

export const GAVETA_PROJECTS = [
  { name: 'Arquivo_2025_Marco', path: 'GAVETA/Arquivo_2025_Marco' },
  { name: 'CEDOC_Eleicoes_2024', path: 'GAVETA/CEDOC_Eleicoes_2024' },
  { name: 'Jornal_Manha_Arquivado', path: 'GAVETA/Jornal_Manha_Arquivado' },
  { name: 'Especial_FestasJuninas_2023', path: 'GAVETA/Especial_FestasJuninas_2023' },
];

export const DEMO_USERS = {
  admin: { password: 'admin', role: 'Gerente' },
  editor: { password: 'editor', role: 'Editor' },
  user: { password: 'user', role: 'Default' },
};

export const DEFAULT_SETTINGS = {
  online_path: 'Z:/Online',
  gaveta_path: 'Y:/Gaveta',
  av_medias_a_path: 'X:/Media',
  lista_path: 'W:/Lists',
  online_gaveta_status: 'ONLINE',
  log_path: './logs',
};

export const SETTINGS_LABELS = {
  online_path: 'Caminho Online',
  gaveta_path: 'Caminho Gaveta',
  av_medias_a_path: 'Caminho de Mídias',
  lista_path: 'Caminho de Listas',
  online_gaveta_status: 'STATUS (Online/Gaveta)',
  log_path: 'Diretório de Logs de Auditoria',
};
