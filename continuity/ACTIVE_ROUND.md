# Rodada ativa

Charter-ID: `CHR-WP02-003`  
Estado: `READY`  
Preparado em: 2026-07-16  
Orquestrador: ChatGPT com o Maestro Diretor  
Executor principal: Codex  
Unidade: `WP-02 Correção final — action, trust fail-closed e lifecycle seguro`

## Autorização

`Leia AGENTS.md e continue` autoriza a execução integral deste charter. Atribua novo `Round-ID`, conclua todas as frentes não bloqueadas e publique exatamente um commit em `origin/master` por repositório afetado, usando o mesmo identificador.

## Revisão anterior

`CHR-WP02-002`, executado em `RND-20260716-007`, recebeu `CORRECTION_REQUIRED`. Registro: `continuity/reviews/REV-RND-20260716-007.md`.

Preserve descoberta paginada, allowlists de origem, parser de checksums, manifest candidato completo, diff allowlist, transporte principal por ambiente, SHA pins do workflow e ausência de promoção.

## Objetivo

Tornar a action realmente executável pelo YunoHost, eliminar interfaces legadas de credencial, corrigir backup/restore sem depender de senha não persistida, fechar a verificação criptográfica diante de assinatura ou chave inválida e reconciliar evidência e CI canônicos.

## Escopo

### A — Config panel e registro

- implementar `run__register()` em `scripts/config` conforme o contrato atual do YunoHost;
- declarar na seção da action todas as entradas efêmeras necessárias, incluindo a credencial como `password` com `bind = "null"`;
- definir URL e imagem como entradas efêmeras ou valores prepopulados por getters/settings, com rationale;
- testar o controlador real, não apenas procurar strings;
- manter `scripts/_register.sh` como único helper;
- remover `scripts/actions/register` e referências associadas;
- garantir que nenhum entry point do pacote receba credencial por argumento de processo.

### B — Backup, restore e identidade

- aplicar o contrato packaging v2 para preservar `/etc/gitlab-runner/config.toml` e a identidade registrada;
- não persistir credencial de registro como setting;
- remover re-registro do restore;
- corrigir `scripts/backup` e `scripts/restore` para restaurar configuração e identidade de forma segura;
- preservar install como registro inicial automático e upgrade sem regenerar identidade;
- testar ausência de variável de credencial no restore, paths de backup e não re-registro.

### C — Assinatura e chave fail-closed

- distinguir ausência de ferramenta de falha criptográfica;
- com GPG/GPGV disponível, abortar em retorno não zero, fingerprint incorreto, assinatura inválida, expirada ou revogada, e chave expirada ou revogada;
- validar fingerprint como campo exato de `VALIDSIG`;
- registrar validade observada da chave;
- permitir `unverified-environment` somente quando a ferramenta realmente não existir e sem classificar trust como `VERIFIED`;
- `generate --refresh` deve falhar sem trust elegível;
- adicionar testes determinísticos para assinatura inválida, fingerprint incorreto, chave expirada/revogada e ferramenta ausente.

### D — Self-link e redirects

- validar o self-link canônico retornado pela API para projeto e tag exatos;
- provar disponibilidade e origem da release por API ou page probe oficial;
- aplicar limite explícito de redirects ou mecanismo equivalente comprovado;
- testar excesso de redirects, destino não permitido e tag divergente.

### E — Evidência e CI

- atualizar somente `evidence/EVIDENCE_INDEX.md` como índice funcional canônico;
- remover `continuity/EVIDENCE_INDEX.md`;
- não marcar action, trust ou CI como `VERIFIED` sem demonstração;
- remover paths absolutos locais dos relatórios;
- ampliar testes do controlador, lifecycle, assinatura e origem;
- manter workflow read-only e actions por SHA;
- remover validação do script legado excluído;
- após push, confirmar run remoto associado ao SHA e resultado final;
- se Actions estiver desabilitado ou sem permissão, concluir todo o restante e registrar bloqueio exato sem alegar verificação.

## DAG paralelo

Onda 1:
- Frente A: config panel/controlador e remoção legada;
- Frente B: backup/restore/identidade;
- Frente C: assinatura/chave;
- Frente D: self-link/redirects;
- Frente E: evidência/testes/CI.

Subagentes não fazem commit. Integração, arquivos canônicos, validação e commit pertencem ao executor principal.

Gate de integração:
- reconciliar config panel, helper, install, backup, restore e testes;
- confirmar ausência de credenciais em argumentos, logs, fixtures e relatórios;
- executar suíte completa e diff de segurança;
- reconciliar o índice canônico.

Onda 2:
- atualizar ADR e documentação;
- repetir descoberta/fixture/diff sem promover versão;
- publicar síntese cross-repo;
- sincronizar remotamente conforme `ROUND_PROTOCOL.md`;
- observar CI do SHA publicado.

## Fora de escopo

- promover qualquer candidata;
- registrar Runner real;
- usar ou testar a credencial histórica;
- reescrever histórico, force push, branch, PR ou worktree;
- executar unregister destrutivo;
- alterar ruleset, visibilidade ou licença.

## Definition of Done

- botão YunoHost chama `run__register()` e recebe credencial efêmera;
- nenhum entry point restante recebe credencial em argumentos;
- backup/restore preservam configuração e identidade sem re-registro;
- assinatura ou chave inválida, expirada, revogada ou com fingerprint incorreto falha fechada;
- self-link, origem e redirects são comprovados e testados;
- manifest permanece `18.6.2~ynh1`;
- `evidence/EVIDENCE_INDEX.md` é o único índice funcional;
- relatórios não persistem paths locais absolutos;
- checks locais passam;
- CI remoto conclui com sucesso, ou bloqueio objetivo é registrado sem claim excessivo;
- um commit publicado por repositório, mesmo `Round-ID`;
- saída `EXECUTED_AWAITING_REVIEW`, ou bloqueio válido após concluir todo o restante.

## Pacote de revisão

Entregar SHAs completos, matriz tarefa-output-evidência, testes, diff de segurança, prova do controlador, modelo de backup/restore, matriz de status GPG, origem/redirects, índice canônico, run remoto de CI ou bloqueio preciso e estado de `HG-RUN-SEC-01`. Não declarar `ACCEPTED`.