# APIE - Adaptive Process Intelligence Engine

APIE e uma plataforma para capturar acoes do usuario no Windows, armazenar eventos em PostgreSQL e reconstruir processos automaticamente a partir desses rastros operacionais.

## Objetivos

- Capturar eventos do Windows, como janela ativa, aplicacao, teclado, mouse e atividades do usuario.
- Expor uma API REST para ingestao, consulta e reconstrucao de processos.
- Persistir eventos e processos reconstruidos em PostgreSQL.
- Exibir eventos e processos em um dashboard web React.
- Manter o backend em Clean Architecture para facilitar evolucao, testes e troca de infraestrutura.

## Stack

- Backend: Python, FastAPI, SQLAlchemy.
- Banco de dados: PostgreSQL.
- Frontend: React, Vite.
- Infraestrutura local: Docker Compose.

## Estrutura

```text
APIE/
  backend/
    app/
      domain/
        entities/
        repositories/
      application/
        use_cases/
        dto/
      infrastructure/
        database/
        repositories/
        windows_capture/
      interfaces/
        api/
          routes/
          schemas/
      main.py
      config.py
    tests/
    Dockerfile
    requirements.txt
  frontend/
    src/
      components/
      pages/
      services/
      styles/
    Dockerfile
    package.json
    index.html
  database/
    migrations/
    init.sql
  docker/
  docs/
  docker-compose.yml
  .env.example
```

## Modelo de dados inicial

### `events`

Armazena cada acao capturada.

- `id`: identificador UUID.
- `event_type`: tipo do evento (`keyboard`, `mouse`, `window`, `application`, `system`).
- `source`: origem do evento, inicialmente `windows`.
- `user_id`: usuario do sistema operacional.
- `session_id`: sessao de captura usada para agrupar eventos.
- `process_name`: nome do processo ou aplicacao.
- `window_title`: titulo da janela ativa.
- `activity`: atividade normalizada.
- `event_metadata`: dados extras em JSONB.
- `occurred_at`: data/hora real do evento.
- `created_at`: data/hora de gravacao.

### `processes`

Representa processos reconstruidos.

- `id`: identificador UUID.
- `name`: nome inferido do processo.
- `status`: estado do processo (`discovered`, `reviewed`, `archived`).
- `confidence_score`: confianca da reconstrucao.
- `created_at`: data/hora de criacao.

### `process_steps`

Representa etapas do processo reconstruido.

- `id`: identificador UUID.
- `process_id`: processo relacionado.
- `name`: nome da etapa.
- `order`: ordem da etapa.
- `application`: aplicacao relacionada.
- `step_metadata`: dados extras em JSONB.

## Endpoints iniciais

- `GET /health`: verifica saude da API.
- `POST /api/v1/events`: registra um evento capturado.
- `GET /api/v1/events`: lista eventos recentes.
- `GET /api/v1/events/{event_id}`: busca um evento por ID.
- `GET /api/v1/processes`: lista processos reconstruidos.
- `GET /api/v1/processes/{process_id}`: busca um processo por ID.
- `POST /api/v1/processes/reconstruct`: reconstrui processos a partir dos eventos armazenados.
- `POST /api/v1/processes/discover`: descobre fluxos com PM4Py e salva processos reconstruidos.
- `POST /api/v1/flowcharts`: gera fluxograma em Mermaid, SVG e PNG Base64.
- `POST /api/v1/sops`: gera POP em PDF a partir de uma sequencia de atividades.
- `POST /api/v1/sops/processes/{process_id}`: gera POP em PDF a partir de um processo descoberto.
- `POST /api/v1/narratives/flow`: transforma fluxo em linguagem natural com Ollama.

## Executando com Docker

```bash
docker compose up --build
```

Servicos:

- API: `http://localhost:8000`
- Swagger/OpenAPI: `http://localhost:8000/docs`
- Dashboard: `http://localhost:5173`
- PostgreSQL: `localhost:5432`

## Exemplo de evento

```bash
curl -X POST http://localhost:8000/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "window",
    "source": "windows",
    "user_id": "sarat",
    "session_id": "demo-session",
    "process_name": "chrome.exe",
    "window_title": "Sistema ERP",
    "activity": "Consultar pedido",
    "metadata": {"url": "https://erp.local/pedidos"}
  }'
```

## Desenvolvimento local do backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Configure `DATABASE_URL` se estiver usando um PostgreSQL fora do Docker.

## Desenvolvimento local do frontend

```bash
cd frontend
npm install
npm run dev
```

## Captura de eventos Windows

A pasta `backend/app/infrastructure/windows_capture` contem o agente de captura.

O modulo registra:

- Clique do mouse.
- Movimento do mouse.
- Tecla pressionada.
- Janela ativa.
- Horario da acao em `occurred_at`.

Por padrao, o agente envia eventos para a API, que salva no PostgreSQL:

```bash
cd backend
python -m app.infrastructure.windows_capture.agent --sink api --api-url http://localhost:8000/api/v1/events
```

Tambem e possivel gravar diretamente no PostgreSQL usando `DATABASE_URL`:

```bash
cd backend
python -m app.infrastructure.windows_capture.agent --sink postgres
```

Arquivos principais:

- `collector.py`: transforma callbacks do Windows em eventos de dominio.
- `monitor.py`: conecta listeners de mouse/teclado e polling de janela ativa.
- `active_window.py`: le janela ativa com `pywin32` e `psutil`.
- `sinks.py`: salva via API ou diretamente no PostgreSQL.

Proximos incrementos recomendados:

- Criar filtro de dados sensiveis antes de persistir eventos.
- Adicionar buffer local para funcionamento offline.
- Assinar ou autenticar o agente antes de aceitar eventos na API.

## Clean Architecture

O backend evita dependencias de framework dentro do dominio:

- Entidades de negocio ficam em `domain/entities`.
- Contratos ficam em `domain/repositories`.
- Casos de uso ficam em `application/use_cases`.
- SQLAlchemy e PostgreSQL ficam em `infrastructure`.
- FastAPI fica em `interfaces`.

Essa separacao permite trocar PostgreSQL, API ou mecanismo de captura sem reescrever as regras centrais.

## Descoberta de processos com PM4Py

O motor inicial fica em `backend/app/infrastructure/process_mining`.

Ele transforma eventos capturados em traces por `session_id`, usa PM4Py para formatar o log de eventos e calcula:

- Sequencias repetidas de atividades.
- Variantes de execucao agrupadas por sequencia.
- Frequencia de cada variante.
- Fluxo logico com transicoes entre atividades.
- Proximas etapas provaveis em `process_steps.step_metadata.next_steps`.

Exemplo:

```bash
curl -X POST http://localhost:8000/api/v1/processes/discover
```

O resultado e persistido em `processes` e `process_steps`.

## Geracao de fluxogramas

O gerador recebe uma sequencia de atividades e devolve automaticamente:

- Mermaid.
- SVG.
- PNG em Base64.

Exemplo:

```bash
curl -X POST http://localhost:8000/api/v1/flowcharts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Fluxo de pedido",
    "activities": ["Login", "Consultar pedido", "Validar estoque", "Salvar"]
  }'
```

Resposta:

```json
{
  "mermaid": "flowchart TD\n    A1[\"Login\"]\n    A2[\"Consultar pedido\"]\n    A1 --> A2",
  "svg": "<svg ...",
  "png_base64": "iVBORw0KGgo...",
  "png_mime_type": "image/png",
  "svg_mime_type": "image/svg+xml"
}
```

## Geracao de POP em PDF

O gerador de Procedimento Operacional Padrao recebe um fluxo descoberto e monta automaticamente:

- Objetivo.
- Responsaveis.
- Pre-requisitos.
- Etapas.
- Resultado esperado.

Gerar a partir de atividades:

```bash
curl -X POST http://localhost:8000/api/v1/sops \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Fluxo de pedido",
    "activities": ["Login", "Consultar pedido", "Validar estoque", "Salvar"]
  }'
```

Gerar a partir de um processo descoberto:

```bash
curl -X POST http://localhost:8000/api/v1/sops/processes/{process_id} \
  -H "Content-Type: application/json" \
  -d '{
    "responsible_roles": ["Analista operacional", "Gestor do processo"],
    "prerequisites": ["Acesso ao ERP", "Pedido cadastrado"]
  }'
```

Resposta:

```json
{
  "filename": "fluxo-de-pedido.pdf",
  "pdf_base64": "JVBERi0x...",
  "mime_type": "application/pdf"
}
```

## Linguagem natural com Ollama

O APIE integra com Ollama para transformar fluxos descobertos em frases em portugues.

Modelos recomendados:

- `llama3`
- `mistral`

Subir Ollama pelo Docker Compose:

```bash
docker compose --profile llm up -d ollama
docker exec -it apie-ollama ollama pull llama3
```

Tambem e possivel usar Mistral:

```bash
docker exec -it apie-ollama ollama pull mistral
```

Exemplo:

```bash
curl -X POST http://localhost:8000/api/v1/narratives/flow \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3",
    "activities": ["ERP", "Compras", "Cadastro", "Salvar"]
  }'
```

Resposta:

```json
{
  "text": "O usuario acessa o ERP, navega ate o modulo de compras, realiza o cadastro e salva as informacoes.",
  "model": "llama3",
  "provider": "ollama",
  "used_fallback": false
}
```

Se o Ollama estiver indisponivel, a API retorna uma narrativa local simples e marca `used_fallback` como `true`.

## Roadmap sugerido

1. Autenticacao de usuarios e agentes.
2. Alembic para versionamento formal de migrations.
3. Captura real de janela ativa, teclado e mouse no Windows.
4. Normalizacao de eventos e mascaramento de dados sensiveis.
5. Algoritmos de process mining, como descoberta de variantes e frequencia de caminhos.
6. Visualizacao de fluxos em grafo no dashboard.
7. Fila de ingestao para alto volume de eventos.
8. Observabilidade com logs estruturados, metricas e traces.
