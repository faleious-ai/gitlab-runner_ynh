# Protocolo de rodada de IA

Identificador: `RND-YYYYMMDD-NNN`.

## START

1. confirmar repositório e `master`;
2. resolver `baseline_head` e reconciliar remoto;
3. verificar árvore limpa;
4. ler `AGENTS.md`, `HANDOFF_CURRENT.md` e `STATUS.md`;
5. carregar somente o contexto roteado;
6. declarar escopo, fora de escopo, critérios, riscos e validações.

## EXECUTE

- manter superfície de mudança delimitada;
- usar tentativa-erro-aprendizado e testes quando aplicável;
- registrar fatos em arquivos canônicos;
- não usar tokens reais em testes persistidos;
- tratar Runner/helper images como conjunto;
- não confundir download bem-sucedido com lifecycle validado.

## VALIDATE

Aplicar conforme o escopo:

- schema/lint;
- integridade e hashes;
- determinismo/idempotência;
- install/service;
- registration com segredo efêmero/redigido;
- executor Docker e helper image;
- upgrade;
- backup/restore;
- remove;
- falhas negativas;
- diff e ausência de segredo.

## PERSIST

No mesmo commit:

- código/docs da unidade;
- `STATUS.md`;
- `HANDOFF_CURRENT.md`;
- decisões/ADRs alterados;
- novo round record;
- `EVIDENCE_INDEX.md`.

Reconciliar novamente HEAD antes de criar o commit. Nunca force.

## COMMIT

Exatamente um commit por rodada neste repositório.

```text
<type>(<scope>): <resultado observável>

Round-ID: RND-YYYYMMDD-NNN
Work-Package: WP-XX
Evidence: EVD-...
```

Trabalho cross-repo repete o mesmo Round-ID no outro repositório.

## END

Termina somente com commit em `master`, estado limpo, evidência indexada e próximo passo explícito.

`result_commit: SELF` designa o commit que contém o registro, evitando commit adicional apenas para registrar SHA.

## BLOCKED

Registrar condição, evidência, tentativas, alternativas, ação humana exata e estado seguro. Tarefa longa, teste falhando e primeira estratégia malsucedida não são bloqueios.