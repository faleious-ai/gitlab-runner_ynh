# ADR-0006 — Proveniência e resolução do release Runner/helper

Status: `ACCEPTED`
Data: 2026-07-16
Round-ID: `RND-20260716-005`

## Decisão

O updater usa como fonte oficial o endpoint de releases do projeto `gitlab-org/gitlab-runner` e os assets versionados publicados no bucket oficial de downloads:

- API de releases: <https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab-runner/releases>;
- release page: <https://gitlab.com/gitlab-org/gitlab-runner/-/releases>;
- downloads/checksums: `https://gitlab-runner-downloads.s3.amazonaws.com/{tag}/`.

O snapshot offline em `scripts/autoupdate/fixtures/` é uma cópia versionada de metadados oficiais, adequada para CI sem rede. Ele não é autoridade para alterar o manifest sozinho.

## Critérios de elegibilidade

1. somente releases estáveis; pre-releases são ignoradas;
2. exatamente um DEB Runner para `amd64`, `arm64` e `armhf`;
3. exatamente um `gitlab-runner-helper-images.deb` com a mesma tag do Runner;
4. URL HTTPS em host oficial, sem `latest`, com tag no caminho;
5. SHA256 de 64 caracteres e tamanho positivo em todas as células;
6. ausência, duplicidade, arquitetura inesperada, mismatch ou metadado inválido aborta antes de qualquer escrita.

## Operação e limites

- metadados de rede usam timeout de 10 segundos e duas tentativas após a primeira, com limite de 1 MiB;
- arquivos locais de fixture podem ser verificados por tamanho e SHA256; downloads de assets não são feitos pelo CI;
- `check` é dry-run e produz relatório JSON; `generate` só escreve com `--write` explícito;
- a escrita usa staging no mesmo diretório e `os.replace` após validação completa;
- o generator cria uma candidata separada e não modifica `manifest.toml` nesta rodada.

## Candidata observada

`v19.0.1` foi registrada em `evidence/wp02-candidate-report.json` com os hashes e tamanhos observados no release oficial. É evidência de resolução, não promoção de versão.

## Rationale

A documentação oficial do GitLab Runner exige instalar `gitlab-runner-helper-images` na mesma versão do pacote Runner para instalações versionadas. Tratar os dois como conjunto evita um estado parcialmente compatível.
