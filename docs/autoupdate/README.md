# Atualizador determinístico do GitLab Runner

O updater separa snapshot offline, descoberta corrente, confiança dos checksums e cópia candidata do manifest. Nenhum caminho usa `latest` e nenhum comando promove o manifest rastreado.

## Descoberta corrente

```bash
python3 scripts/autoupdate.py discover \
  --manifest manifest.toml \
  --report evidence/wp02-online-discovery.json
```

O comando pagina a Releases API oficial, escolhe a release estável mais recente, valida origem/redirects, baixa apenas os metadados `release.sha256`/`.asc`, consulta tamanhos por `HEAD` e registra a observação. A release corrente observada nesta rodada é `v19.2.0`; isso não altera `manifest.toml`.

## Verificar a fixture offline

```bash
python3 scripts/autoupdate.py check \
  --fixture scripts/autoupdate/fixtures/release-v19.0.1.json \
  --manifest manifest.toml \
  --report evidence/wp02-candidate-report.json
```

A fixture é um `offline-release-snapshot` versionado. O updater confronta os quatro hashes do catálogo com a tabela registrada do `release.sha256`; `--verify-files` também verifica arquivos locais opcionais por tamanho e SHA256.

## Gerar a cópia candidata completa

```bash
python3 scripts/autoupdate.py generate \
  --fixture scripts/autoupdate/fixtures/release-v19.0.1.json \
  --manifest manifest.toml \
  --output /tmp/gitlab-runner-manifest.candidate.toml \
  --report evidence/wp02-manifest-diff.json \
  --write
```

O destino é explícito, fora do manifest e de arquivos rastreados. O diff machine-readable só permite `version`, URLs e hashes dos sources Runner/helper. Sem `--write`, o comando é dry-run e imprime a candidata sem criar arquivo.

## Registro administrativo

YunoHost >= 12.1.17 usa a action `main.registration.register` de `config_panel.toml`, implementada em `scripts/config`. Install, restore e action chamam `scripts/_register.sh`, que:

- valida cardinalidade e todos os valores antes do primeiro subprocesso;
- passa URL/token por `CI_SERVER_URL`, `CI_SERVER_TOKEN` e `REGISTER_NON_INTERACTIVE`;
- mantém URL/token fora de `argv` e redige token em diagnósticos;
- nunca grava o token em arquivo ou saída de teste.

O placeholder em `tests.toml` é deliberadamente não funcional. O gate `HG-RUN-SEC-01` permanece aberto para confirmação externa sobre o valor histórico removido.
