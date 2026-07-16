# ADR-0006 — Proveniência e resolução do release Runner/helper

Status: `ACCEPTED_WITH_CORRECTION_ROUND`
Data: 2026-07-16
Round-ID: `RND-20260716-007`

## Decisão

O updater usa exatamente o projeto `gitlab-org/gitlab-runner`, a Releases API oficial e os downloads versionados:

- API: <https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab-runner/releases>;
- página: `https://gitlab.com/gitlab-org/gitlab-runner/-/releases/{tag}`;
- downloads/checksums: `https://gitlab-runner-downloads.s3.amazonaws.com/{tag}/`.

`discover` pagina a API, seleciona semanticamente a release estável mais recente, exige a página e os links de assets oficiais e registra `observed_at`. Redirecionamentos cujo destino não pertence à origem esperada abortam.

## Checksums e assinatura

Para a mesma tag, o updater busca `release.sha256`, interpreta os registros e exige exatamente estes quatro nomes: `gitlab-runner_amd64.deb`, `gitlab-runner_arm64.deb`, `gitlab-runner_armhf.deb` e `gitlab-runner-helper-images.deb`. O catálogo só é aceito quando seus hashes coincidem com essa fonte; ausência, duplicidade, divergência, tag ou filename inesperado aborta antes da escrita.

O documento `.asc` é buscado junto. Quando o ambiente possui GPG e a chave oficial documentada, a assinatura é verificada pelo fingerprint `931D A69C FA3A FEBB C97D AA8C 6C57 C29C 6BA7 5A4E`; quando o ambiente não possui a ferramenta/keyring operacional, o relatório registra `unverified-environment` e a limitação. A estratégia equivalente registrada é HTTPS de origem fixada, digest do documento, parsing completo dos registros necessários e confronto integral catálogo/documento. A chave e o procedimento são os publicados na documentação oficial do GitLab Runner.

## Fixture, candidata e não promoção

A fixture `scripts/autoupdate/fixtures/release-v19.0.1.json` é explicitamente `offline-release-snapshot`; contém o digest do documento oficial e seus quatro registros confrontados. Ela não é confundida com a descoberta corrente, que em 2026-07-16 observou `v19.2.0`.

`check` é dry-run. `generate` lê e valida o `manifest.toml` real, cria uma cópia candidata completa em destino explícito fora dos arquivos rastreados e produz diff determinístico limitado a `version`, URLs e hashes autorizados. `--write` é obrigatório para materializar a cópia; o `manifest.toml` rastreado permanece em `18.6.2~ynh1`.

## Registro e action YunoHost

O GitLab Runner recebe `CI_SERVER_URL`, `CI_SERVER_TOKEN` e `REGISTER_NON_INTERACTIVE` no ambiente, sem URL/token em `argv`. Install, restore e a action compartilham `scripts/_register.sh`.

YunoHost atual executa `app_action_run` através de `ConfigPanel.run_action`; por isso a action foi migrada para `config_panel.toml` e `scripts/config`, com o identificador `main.registration.register`. `actions.json` não é mais a fonte de contrato.
