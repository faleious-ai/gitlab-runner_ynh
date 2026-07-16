# HG-RUN-SEC-01 — Credencial histórica do package_check

Estado: `UNRESOLVED_NO_AUTHORITY`  
Atualizado em: 2026-07-16  
Decisão humana registrada em: `RND-20260716-005`

## Condição

A fixture pública `tests.toml` contém um literal com formato de token de GitLab Runner e aponta para o projeto externo `gitlab.com/kay0u/gitlab-runner_ynh`, usado pelo package_check upstream.

## Resposta do Maestro Diretor

O Maestro Diretor confirmou que não possui acesso administrativo ao projeto GitLab.com indicado. A instância Asimovart não é o destino identificado pela fixture; portanto, não há ação útil a executar nela para resolver esta exposição.

## Consequência

- Não é possível confirmar revogação, rotação ou expiração do valor histórico.
- O valor deve continuar tratado como potencialmente exposto.
- Nenhum agente está autorizado a testar sua validade ou autenticar com ele.
- A árvore atual deve remover o literal e impedir recorrência.
- A ausência de autoridade externa não bloqueia S1, S2, U1, U2, U3 ou A1 do charter `CHR-WP02-001`.

## Resolução possível

Somente um mantenedor ou administrador do projeto externo pode confirmar expiração ou revogar/rotacionar a credencial. Até isso ocorrer, o risco histórico permanece aberto e deve ser citado no pacote de revisão e em qualquer decisão de release.

## Regra de parada

O Codex não deve parar agora. Deve concluir todo o trabalho técnico independente e encerrar em `EXECUTED_AWAITING_REVIEW`, registrando este gate como risco residual externo. Não declarar `BLOCKED_HUMAN` apenas porque o usuário não possui autoridade sobre o projeto upstream.
