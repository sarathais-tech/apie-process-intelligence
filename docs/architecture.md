# Arquitetura APIE

O APIE segue Clean Architecture para manter regras de negocio independentes de frameworks.

## Camadas

- `domain`: entidades e contratos de repositorio.
- `application`: casos de uso que orquestram regras de negocio.
- `infrastructure`: banco de dados, repositorios concretos e captura Windows.
- `interfaces`: API REST, schemas e dependencias de FastAPI.
- `frontend`: dashboard React para acompanhamento operacional.

## Fluxo inicial

1. Um agente Windows captura eventos de janela, teclado, mouse ou aplicacao.
2. O agente envia eventos para `POST /api/v1/events`.
3. A API persiste eventos no PostgreSQL.
4. `POST /api/v1/processes/reconstruct` agrupa eventos por sessao e gera processos reconstruidos.
5. O dashboard consulta eventos e processos pela API REST.
