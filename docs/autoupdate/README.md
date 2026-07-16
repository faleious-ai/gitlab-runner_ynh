# Atualizador determinístico do GitLab Runner

O updater é offline-first. A fixture em `scripts/autoupdate/fixtures/` representa uma release oficial e é usada por testes e CI; nenhum script de install/upgrade consulta `latest`.

## Verificar uma candidata

```bash
python3 scripts/autoupdate.py check \
  --fixture scripts/autoupdate/fixtures/release-v19.0.1.json \
  --manifest manifest.toml \
  --report evidence/wp02-candidate-report.json
```

O comando é dry-run, valida Runner e helper images como uma unidade, e informa a candidata sem modificar `manifest.toml`.

## Gerar saída de candidata

```bash
python3 scripts/autoupdate.py generate \
  --fixture scripts/autoupdate/fixtures/release-v19.0.1.json \
  --output /tmp/gitlab-runner-candidate.toml \
  --write
```

`--write` é obrigatório. A saída é um artefato de revisão, não uma promoção automática. A promoção para o manifest requer uma rodada autorizada separada.

## Registro administrativo

`actions.json` chama `scripts/actions/register`. O script e install/restore reutilizam `scripts/_register.sh`, que:

- valida cardinalidade de URL, token e imagem antes do primeiro registro;
- usa o token somente no comando suportado pelo CLI do Runner;
- mantém tracing desligado, captura a saída e redige token em diagnósticos;
- nunca grava o token em arquivo ou saída de teste.

O placeholder em `tests.toml` é deliberadamente não funcional. O gate `HG-RUN-SEC-01` permanece aberto para que o administrador confirme revogação, rotação ou expiração do valor histórico removido.
