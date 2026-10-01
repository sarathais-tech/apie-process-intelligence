# APiE — Adaptive Process Intelligence Engine

**Documentação técnica e de projeto**  
**Especificação, implementação e validação**

**Autores:** Sara Thais dos Santos Graciano e Gabriel Henrique de Medeiros Penha  
**Instituição:** UNIGOIÁS — Engenharia de Software  
**Local:** Goiânia — 2026

> Versão organizada para leitura direta no GitHub, baseada na documentação técnica entregue ao professor em 01/10/2026.

---

## Sumário

1. [Introdução](#1-introdução)
2. [Plano de projeto](#2-plano-de-projeto)
3. [Estado da solução e fluxo](#3-estado-da-solução-e-fluxo)
4. [Requisitos e regras de sistema](#4-requisitos-e-regras-de-sistema)
5. [Casos de uso e cenário de referência](#5-casos-de-uso-e-cenário-de-referência)
6. [Arquitetura e código](#6-arquitetura-e-código)
7. [Banco de dados e diagrama relacional](#7-banco-de-dados-e-diagrama-relacional)
8. [Cenários de teste e evidências](#8-cenários-de-teste-e-evidências)
9. [Resultados e discussão](#9-resultados-e-discussão)
10. [Conclusão e próximos passos](#10-conclusão-e-próximos-passos)
11. [Referências](#referências)

---

## Critério de leitura

| Marcação | Significado |
|---|---|
| **Implementado no código** | Existe implementação identificável na branch `main`; isso não implica teste ponta a ponta. |
| **Demonstrado** | Há registro visual de execução com resposta observável na demonstração disponível. |
| **Modelo proposto** | Consta em diagrama, dicionário ou requisito, mas não no esquema/fluxo executável atual. |
| **Trabalho futuro** | Depende de desenvolvimento ou verificação antes de ser apresentado como concluído. |

### Siglas e termos

- **APiE** — Adaptive Process Intelligence Engine
- **API** — Interface de Programação de Aplicações
- **DER** — Diagrama Entidade Relacionamento
- **ERP** — Sistema de Gestão Empresarial
- **FK** — Chave estrangeira
- **PK** — Chave primária
- **POP** — Procedimento Operacional Padrão
- **UUID** — Identificador universal único

---

# 1 Introdução

O mapeamento manual de rotinas depende de entrevistas, observação e documentação posterior. O APiE investiga como registros de atividades em ambiente digital podem apoiar a identificação de sequências de trabalho e a elaboração de fluxogramas, descrições e Procedimentos Operacionais Padrão (POPs).

A intenção é reduzir o esforço de levantamento e facilitar a transferência de conhecimento quando um responsável por uma rotina se afasta ou precisa treinar outra pessoa.

O recorte experimental utiliza eventos agrupados por sessão. Uma execução de cadastro de fornecedor em um ERP serve como cenário de referência para a especificação. A demonstração gravada em junho usa cadastro de cliente; os dois cenários são exemplos distintos e não devem ser apresentados como um mesmo teste.

## 1.1 Objetivo e limites

O objetivo geral é desenvolver e avaliar um protótipo capaz de:

- registrar eventos;
- reconstruir um fluxo;
- produzir documentação;
- gerar fluxograma;
- gerar POP;
- produzir descrição textual;
- solicitar validação humana do resultado.

O ambiente demonstrado é local. Ainda não há avaliação em empresa, medição comparativa com mapeamento manual nem comprovação de extração semântica confiável de todas as ações de um ERP.

---

# 2 Plano de projeto

A pesquisa é aplicada e utiliza prototipação e experimentação em cenário controlado. O plano contempla definição do problema, requisitos, arquitetura, captura, reconstrução, geração de artefatos, testes e análise.

A equipe é formada por **Sara Thais dos Santos Graciano** e **Gabriel Henrique de Medeiros Penha**.

| Fase | Período planejado | Horas previstas | Horas realizadas | Progresso registrado |
|---|---:|---:|---:|---:|
| Requisitos | 10/03 a 25/04/2026 | 88 | 82 | 93% |
| Projeto | 26/04 a 31/05/2026 | 60 | 52 | 87% |
| Implementação | 01/06 a 31/08/2026 | 175 | 125 | 71% |
| Testes | 01/09 a 20/10/2026 | 86 | 20 | 23% |
| **Total** | 10/03 a 20/10/2026 | **409** | **279** | **68%** |

Os valores representam acompanhamento do planejamento e não uma avaliação independente da completude funcional.

## 2.1 Recursos, riscos e critérios de sucesso

| Tema | Planejamento e tratamento |
|---|---|
| Recursos | Computadores pessoais, conectividade, Python/FastAPI, PostgreSQL, Docker, GitHub e ferramentas de documentação. |
| Dados incompletos | Definir evento mínimo válido, testar ausência e ordenação, registrar falhas e impedir conclusões não sustentadas. |
| Privacidade da captura | Limitar testes a ambiente controlado, reduzir coleta de teclas e mascarar dados sensíveis antes de uso real. |
| Inferência incorreta | Exigir revisão final de responsável pelo processo antes de validar a documentação. |
| Prazo e integração | Separar protótipo demonstrável de funcionalidades futuras; acompanhar testes e evidências por entrega. |

## 2.2 Escopo, premissas e restrições

O plano delimita um protótipo desenvolvido por duas pessoas, com dados fictícios e execução em ambiente controlado.

O escopo inclui levantamento bibliográfico e de requisitos, arquitetura, captura e organização de eventos, descoberta de sequências, geração de fluxograma, POP e narrativa, integração dos módulos, testes e documentação.

A revisão humana posterior à geração integra a evolução do fluxo e deverá ser implementada e testada antes de ser considerada entrega funcional.

## 2.3 Registro de riscos

| Risco | I × P | Resposta |
|---|---:|---|
| Algoritmos de análise e reconstrução | 5 × 4 = 20 | Usar sessões com sequência de referência e comparar variantes e etapas produzidas. |
| Atraso por complexidade do desenvolvimento | 5 × 4 = 20 | Acompanhar entregas por fase e reservar tempo para integração/testes. |
| Captura imprecisa dos eventos | 5 × 3 = 15 | Revisar completude dos eventos e repetir captura em cenário controlado. |
| Fluxo reconstruído inconsistente | 4 × 3 = 12 | Conferir ordem, ações ausentes e decisões com pessoa conhecedora da rotina. |
| Fluxograma incompreensível / integração | 4 × 3 = 12 | Verificar artefatos contra a sequência e executar fluxo ponta a ponta. |
| Dados de validação insuficientes | 4 × 2 = 8 | Preparar cenários variados e preservar entradas, saídas e evidências. |

---

# 3 Estado da solução e fluxo

| Função | Situação | Evidência / limite |
|---|---|---|
| Agente de captura Windows | Implementado no código | Listeners de mouse/teclado e consulta de janela; execução real ainda precisa de evidência física. |
| API de eventos e PostgreSQL | Implementado no código | Consulta de eventos demonstrada. |
| Reconstrução e variantes | Implementado no código | Endpoint de descoberta/reconstrução retorna etapas e frequência. |
| Fluxograma Mermaid, SVG e PNG | Implementado no código | Endpoint retorna representações do fluxograma. |
| POP em PDF | Implementado no código | Endpoint retorna PDF codificado em Base64. |
| Narrativa | Implementado no código | Integração Ollama com alternativa local. |
| Painel React | Implementado no código | Exibe eventos/processos e aciona reconstrução. |
| Solicitação automática de validação | Modelo proposto | Ainda não existem endpoint, tabela ou tela de revisão/aprovação. |

## 3.1 Sequência operacional

### Fluxo implementado

Agente Windows ou cliente da API → POST de evento → tabela `events` → consulta de eventos → reconstrução de variantes por sessão → tabelas `processes` e `process_steps` → geração de fluxograma, POP ou narrativa.

### Fluxo completo proposto

Após gerar o mapeamento e os artefatos, o APiE deverá:

1. criar uma solicitação de validação;
2. apresentar processo, fluxograma, POP e descrição;
3. manter a versão como pendente;
4. aguardar revisão da pessoa responsável;
5. registrar aprovação ou pedido de correção;
6. gerar nova versão quando houver ajustes;
7. considerar final apenas uma versão aprovada.

---

# 4 Requisitos e regras de sistema

## 4.1 Requisitos funcionais

| ID | Requisito | Situação |
|---|---|---|
| RF01 | Registrar evento com tipo, origem, data/hora, sessão e metadados. | Implementado |
| RF02 | Consultar eventos e recuperar registro pelo identificador. | Implementado |
| RF03 | Agrupar eventos por sessão, ordenar e obter variantes/transições. | Implementado |
| RF04 | Persistir processo descoberto e suas etapas. | Implementado |
| RF05 | Gerar fluxograma a partir de sequência de atividades. | Implementado |
| RF06 | Gerar POP em PDF a partir de atividades ou processo descoberto. | Implementado |
| RF07 | Gerar descrição textual por Ollama ou alternativa local. | Implementado |
| RF08 | Capturar mouse, teclado e janela ativa por agente Windows. | Implementado; execução física pendente de evidência |
| RF09 | Solicitar automaticamente validação após geração dos artefatos. | Modelo proposto |
| RF10 | Permitir aprovação ou solicitação de correção com justificativa. | Modelo proposto |
| RF11 | Registrar solicitação, revisor, data, versão e decisão. | Modelo proposto |
| RF12 | Gerar nova versão e pedir nova validação após correção. | Modelo proposto |
| RF13 | Restringir documentação final à versão aprovada. | Modelo proposto |

## 4.2 Requisitos não funcionais e regras

| ID | Requisito | Avaliação atual |
|---|---|---|
| RNF01 | Rastrear evento por identificador e carimbo temporal. | Campos presentes |
| RNF02 | Preservar integridade entre processos e etapas. | FK e ON DELETE CASCADE |
| RNF03 | Evitar exposição de teclas/dados pessoais capturados. | Proteção e mascaramento são próximos incrementos |
| RNF04 | Autenticar agente e usuários. | Ainda não implementado |
| RS01 | Rejeitar dados ausentes ou formato incorreto. | Schemas e respostas 422 |
| RS02 | Verificar sequência e coerência semântica. | Ainda não demonstrado por completo |
| RS03 | Registrar logs de falhas, revisões e geração. | Trilha completa pendente |

A geração dos artefatos não equivale à aprovação. No fluxo pretendido, somente uma pessoa designada decide se a versão representa corretamente a rotina.

---

# 5 Casos de uso e cenário de referência

O cenário de referência utiliza **Maria**, funcionária do financeiro, executando o cadastro de fornecedor em um ERP.

O APiE registra a sessão e os eventos, reconstrói o processo e gera os artefatos. O ERP é tratado como sistema externo.

| Caso | Ator / pré-condição | Fluxo principal | Alternativa |
|---|---|---|---|
| UC01 Capturar rotina | Operadora; agente e API disponíveis | Inicia sessão, executa rotina e encerra coleta | Falha de envio/autorização |
| UC02 Reconstruir processo | Operadora; eventos existentes | Agrupa, ordena, identifica sequência e salva processo | Sem eventos úteis |
| UC03 Gerar artefatos | Operadora; fluxo disponível | Gera fluxograma, POP e narrativa | Erro 422 ou fallback de narrativa |
| UC04 Validar documentação | Responsável; artefatos gerados | Analisa, aprova ou solicita ajustes | Nova versão e nova validação |

## 5.1 Caso de uso geral — UC05

**Objetivo:** obter uma versão revisada do processo executado, acompanhada de fluxograma, POP e descrição textual.

**Ator principal:** operador que executa uma rotina no sistema externo e autoriza a captura.

**Atores secundários:** responsável por conferir o processo e o sistema empresarial observado, como um ERP.

**Gatilho:** o operador inicia uma execução destinada ao mapeamento.

**Pré-condições:** APiE e banco disponíveis; operador/responsável definidos; captura autorizada; rotina e limites conhecidos.

**Pós-condição de sucesso (futura):** versão do processo e documentos aprovada, com decisão, responsável, data e histórico associados.

### Etapas

1. Operador inicia a captura.
2. Operador realiza atividades no ERP.
3. APiE registra e persiste os eventos.
4. APiE ordena eventos, agrupa sessões e persiste etapas.
5. APiE gera fluxograma, POP e descrição.
6. APiE cria solicitação de validação.
7. Responsável aprova ou solicita correção.
8. Se aprovada, a versão é identificada como final; se corrigida, uma nova revisão é solicitada.

---

# 6 Arquitetura e código

A branch `main` organiza o backend em:

- `domain` — entidades e contratos;
- `application` — casos de uso;
- `infrastructure` — SQLAlchemy, captura Windows, descoberta e geração;
- `interfaces` — rotas e schemas FastAPI.

O frontend React/Vite consulta a API e apresenta contagens, eventos e processos.

O Docker Compose define backend, frontend e PostgreSQL; Ollama aparece como integração opcional.

| Componente | Arquivo / rota | Papel |
|---|---|---|
| Eventos | `app/interfaces/api/routes/events.py` | POST/GET de eventos e busca por UUID |
| Reconstrução | `app/application/use_cases/reconstruct_processes.py` | Lê eventos, obtém variantes e grava processos |
| Descoberta | `app/infrastructure/process_mining/pm4py_discovery_engine.py` | Agrupa por sessão, ordena, compacta e calcula frequências/transições |
| Captura | `app/infrastructure/windows_capture/` | Listeners, contexto da janela e envio |
| Documentos | `app/infrastructure/flowcharts/` e `documents/` | Gera fluxo visual e PDF |
| Narrativa | `app/infrastructure/llm/ollama_flow_narrator.py` | Consulta Ollama e fallback local |
| Interface | `frontend/src/App.jsx` | Exibe eventos/processos e reconstrução |

## 6.1 Contrato resumido da API

| Método e rota | Uso |
|---|---|
| `GET /health` | Verificar disponibilidade |
| `POST /api/v1/events` | Registrar evento |
| `GET /api/v1/events` | Listar eventos |
| `GET /api/v1/events/{event_id}` | Consultar evento |
| `GET /api/v1/processes` | Listar processos |
| `GET /api/v1/processes/{process_id}` | Consultar processo |
| `POST /api/v1/processes/discover` | Descobrir variantes |
| `POST /api/v1/processes/reconstruct` | Reconstruir variantes |
| `POST /api/v1/flowcharts` | Gerar fluxograma |
| `POST /api/v1/sops` | Gerar POP |
| `POST /api/v1/sops/processes/{process_id}` | Gerar POP de processo |
| `POST /api/v1/narratives/flow` | Gerar narrativa |

Na instalação local documentada, a interface Swagger fica em:

`http://localhost:8000/docs`

### Exemplo de evento

```json
{
  "event_type": "mouse",
  "source": "windows",
  "session_id": "sessao-exemplo",
  "activity": "Abrir cadastro",
  "occurred_at": "2026-06-16T10:00:00Z"
}
```

### Exemplo de fluxograma

```json
{
  "title": "Cadastro de fornecedor",
  "activities": [
    "Abrir cadastro",
    "Preencher dados",
    "Salvar cadastro"
  ]
}
```

## 6.2 Tecnologias utilizadas

| Tecnologia / ferramenta | Papel no projeto |
|---|---|
| **Python** | Backend, agente de captura e componentes de processamento/documentação |
| **FastAPI** | Disponibiliza endpoints HTTP |
| **Uvicorn** | Executa a aplicação FastAPI |
| **PostgreSQL 16** | Armazena eventos, processos e etapas |
| **SQLAlchemy** | ORM/acesso ao banco |
| **Psycopg** | Conexão Python ↔ PostgreSQL |
| **JavaScript / React** | Interface web do painel |
| **Vite** | Desenvolvimento e build do frontend |
| **Docker / Docker Compose** | Orquestra backend, frontend, PostgreSQL e integração opcional com Ollama |
| **OpenAPI / Swagger UI** | Documentação interativa da API |
| **pandas** | Estrutura eventos em DataFrame |
| **PM4Py** | Participa da formatação/processamento de dados de Process Mining |
| **Mermaid** | Representação textual dos fluxos |
| **SVG / PNG** | Formatos de saída dos fluxogramas |
| **Ollama / llama3** | Integração opcional para geração de narrativa |
| **Git / GitHub** | Versionamento e hospedagem do projeto |
| **Windows** | Ambiente local e do agente de captura |

> A pontuação de confiança do protótipo é uma heurística interna; não deve ser interpretada como probabilidade estatisticamente validada.

---

# 7 Banco de dados e diagrama relacional

Existem dois níveis de modelagem:

1. **Esquema executável atual**, com três tabelas principais.
2. **Modelo conceitual de evolução**, ampliado para usuários, sessões, artefatos e validação.

## 7.1 Esquema implementado

### EVENTS

Principais campos:

- `id UUID PK`
- `event_type VARCHAR(50)`
- `source VARCHAR(100)`
- `user_id VARCHAR(120)` opcional
- `session_id VARCHAR(120)` opcional
- `process_name VARCHAR(255)`
- `window_title TEXT`
- `activity VARCHAR(255)`
- `event_metadata JSONB`
- `occurred_at TIMESTAMPTZ`
- `created_at TIMESTAMPTZ`

### PROCESSES

- `id UUID PK`
- `name VARCHAR(255)`
- `status VARCHAR(50)`
- `confidence_score DOUBLE PRECISION`
- `created_at TIMESTAMPTZ`

### PROCESS_STEPS

- `id UUID PK`
- `process_id UUID FK`
- `name VARCHAR(255)`
- `order INTEGER`
- `application VARCHAR(255)`
- `step_metadata JSONB`

A relação física formal atual é:

`PROCESSES 1:N PROCESS_STEPS`

## 7.2 Modelo conceitual de evolução

| Entidade | Papel |
|---|---|
| USERS | Identificar a pessoa que executa a rotina |
| CAPTURE_SESSIONS | Delimitar uma execução capturada |
| EVENTS | Guardar ações e contexto cronológico |
| PROCESSES | Representar o processo identificado |
| PROCESS_STEPS | Ordenar etapas de cada processo |
| FLOWCHARTS | Guardar representações do fluxo |
| SOPS | Guardar POP e PDF |
| NARRATIVES | Guardar descrição textual |

Para sustentar validação humana, a evolução prevê também histórico de versões e decisões de revisão.

---

# 8 Cenários de teste e evidências

| ID | Cenário | Resultado esperado | Situação |
|---|---|---|---|
| CT01 | Registro válido | 201, UUID e evento consultável | Parcialmente evidenciado |
| CT02 | Campo obrigatório ausente | 422 e nenhum novo evento | Pendente |
| CT03 | Ordem temporal | Etapas ordenadas por `occurred_at` | Lógica implementada; integração pendente |
| CT04 | Variantes repetidas | Frequências corretas | Teste unitário no repositório |
| CT05 | Descoberta | 201 e sequência de etapas | Demonstrado |
| CT06 | Fluxograma | 201 + Mermaid/SVG/PNG | Demonstrado |
| CT07 | POP | 201 + arquivo/PDF Base64 | Demonstrado |
| CT08 | Narrativa com IA | provider Ollama, fallback false | Pendente |
| CT09 | Narrativa alternativa | provider local-template, fallback true | Implementado; integração pendente |
| CT10 | Captura Windows | Eventos com sessão/atividade/horário | Execução física pendente |
| CT11 | Pedido de validação | Solicitação criada e versão pendente | Futuro |
| CT12 | Aprovação humana | Decisão, autor, data e versão gravados | Futuro |
| CT13 | Correção | Nova versão e nova solicitação | Futuro |
| CT14 | Sem aprovação | Impedir marcação como final | Futuro |

## 8.1 Protocolo para testes pendentes

- usar base descartável;
- anotar commit e configuração;
- usar dados fictícios;
- registrar requisição e resposta completas;
- consultar banco após operações de persistência;
- salvar evidências com identificação do teste;
- executar testes de aprovação somente após implementação.

---

# 9 Resultados e discussão

O protótipo implementa:

- API de ingestão;
- persistência de eventos, processos e etapas;
- reconstrução de variantes por sessão;
- geração de fluxograma;
- geração de POP;
- geração de narrativa;
- agente separado de captura Windows.

A demonstração disponível registra respostas positivas para descoberta, fluxograma e POP.

O código atual ainda não prova que cliques e teclas, sem contexto adicional, se convertem corretamente em atividades de negócio de maior nível semântico, como “validar fornecedor”. Esse é um limite central da interpretação automática.

A integração opcional com Ollama pode produzir texto em linguagem natural. Quando o serviço não está disponível, existe alternativa local. A resposta deve indicar o método utilizado.

A confiança numérica do processo é uma heurística do protótipo e não substitui a avaliação de uma pessoa responsável pela rotina.

---

# 10 Conclusão e próximos passos

O código e a demonstração sustentam a existência de um protótipo funcional por componentes e uma execução controlada de parte do fluxo.

O modelo de evolução amplia a persistência e inclui solicitação automática de validação humana.

### Próximos marcos

1. alinhar DER e dicionário ao esquema físico;
2. implementar revisão humana;
3. implementar histórico de versões;
4. testar o agente Windows em execução real;
5. registrar os resultados dos cenários pendentes;
6. avaliar a qualidade dos documentos com responsáveis pela rotina;
7. impedir que versões não revisadas sejam marcadas como finais.

---

# Referências

- EQUIPE APiE. **Plano de Projeto**. Documento de planejamento.
- EQUIPE APiE. **Regras de Sistema para Captura, Descoberta e Documentação Automática de Processos**.
- EQUIPE APiE. **Cronograma do Projeto**.
- EQUIPE APiE. **Dicionário de Dados do APiE**.
- EQUIPE APiE. **Diagrama de Caso de Uso do Cadastro de Fornecedor**.
- EQUIPE APiE. **Diagrama Geral de Casos de Uso do APiE**.
- EQUIPE APiE. **Modelo Conceitual de Dados do APiE**.
- EQUIPE APiE. **Demonstração da API no Swagger**, registro audiovisual de 16/06/2026.
- EQUIPE APiE. **Código-fonte do APiE** — repositório `sarathais-tech/apie-process-intelligence`.
- PostgreSQL Global Development Group. **PostgreSQL 16 Documentation**.

---

## Índice dos componentes documentados

| Componente | Localização |
|---|---|
| Cenários de teste | Capítulo 8 |
| Requisitos | Capítulo 4 |
| Plano de projeto | Capítulo 2 |
| Casos de uso | Capítulo 5 |
| Diagrama/modelagem relacional | Capítulo 7 |
| Dicionário de dados | Capítulo 7 |
| Repositório e código | Capítulo 6 |
| Fluxo operacional | Capítulo 3 |
| Tecnologias utilizadas | Capítulo 6.2 |

---

**APiE | Documentação técnica e de projeto | UNIGOIÁS — Engenharia de Software**
