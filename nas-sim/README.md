# NAS Simulado — TV Anhanguera (demo/pitch)

Estrutura local que imita o Storage Quantum para desenvolvimento e gravação do pitch, sem depender da rede da emissora.

## Estrutura

```text
nas-sim/
├── Online/     ← projetos ativos (listagem aba Online)
├── Gaveta/     ← projetos arquivados (aba Gaveta)
├── Media/      ← destino do mapeamento (subst/net use)
└── Lists/      ← exportação de relatórios .txt
```

## Configurar

```bash
python scripts/setup_pitch_env.py
```

## Usar com o app real

```bash
python run_pitch.py
```

Abra `http://127.0.0.1:5000` — login `admin` / `admin`.

O mapeamento usa `subst` nas pastas locais de `Media/`, funcionando no Windows sem NAS físico.
