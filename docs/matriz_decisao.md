# Fase 1: Engenharia de Conhecimento e Matriz de Decisão

## 1. Dimensões da entrevista

| # | Dimensão (`chave`) | Pergunta | Valores possíveis |
|---|---|---|---|
| 1 | `matematica` | Afinidade com matemática e estatística | baixa, media, alta |
| 2 | `atividade` | Preferência de atuação diária | algoritmos, layouts, servidores, dados, seguranca, testes, negocio |
| 3 | `ferramenta` | Linguagem/ferramenta de maior afinidade | python, javascript, java_csharp, sql, linux_redes, mobile, nenhuma |
| 4 | `entrega` | Tipo de entrega de valor preferida | produto_usuario, regras_negocio, infraestrutura, seguranca, dados, qualidade, estrategia |
| 5 | `dados_foco` | O que atrai diante de grandes volumes de dados | modelar, pipelines, nenhum |
| 6 | `plataforma` | Onde prefere que o trabalho rode | web, mobile, nuvem, indiferente |
| 7 | `automacao` | Gosto por automatizar tarefas | baixa, media, alta |
| 8 | `comunicacao` | Gosto por negociar e lidar com pessoas | baixa, media, alta |

As dimensões 5 a 8 existem para **desambiguar** trilhas parecidas:

- `dados_foco` separa Ciência de Dados de Engenharia de Dados.
- `plataforma` separa Front-end de Mobile e DevOps de Cloud.
- `automacao` separa DevOps de Cloud e reforça QA.
- `comunicacao` identifica o perfil de Gestão de Produtos.

## 2. Estratégia de inferência (encadeamento para frente)

```
Respostas ──► Perfil (fato)
                 │
                 ├─► R01–R08: Caracteristica (fatos intermediários)
                 │       ANALÍTICO, VISUAL, INFRA, CONSTRUTOR,
                 │       DEFENSIVO, AUTOMATIZADOR, DETALHISTA, NEGÓCIOS
                 │
                 ├─► R09–R42: Indicio(trilha, peso, motivo)
                 │       decisivas (+3), suporte (+1/+2), desambiguação (−1/−2)
                 │
                 └─► R99 (salience −100): soma os pesos ──► Diagnostico
```

**Critério de decisão (R99):** vence a trilha com a maior soma de pesos. Em caso de empate, vence a que tiver mais regras decisivas; persistindo o empate, vale a ordem da lista de trilhas.

## 3. Características derivadas (nível 1)

| Regra | SE | ENTÃO |
|---|---|---|
| R01 | matemática = alta **E** (atividade = dados **OU** ferramenta = Python) | ANALÍTICO |
| R02 | atividade = layouts | VISUAL |
| R03 | atividade = servidores **OU** ferramenta = Linux/Redes **OU** entrega = infraestrutura | INFRA |
| R04 | atividade = algoritmos **OU** ferramenta = Java/C# | CONSTRUTOR |
| R05 | atividade = segurança **OU** entrega = segurança | DEFENSIVO |
| R06 | automação = alta | AUTOMATIZADOR |
| R07 | atividade = testes **OU** entrega = qualidade | DETALHISTA |
| R08 | comunicação = alta **E** (atividade = negócio **OU** entrega = estratégia) | NEGÓCIOS |

## 4. Matriz de decisão por trilha (nível 2)

A **R09** (afinidade direta) soma +1 à trilha ligada à atividade preferida: algoritmos → Back-end, layouts → Front-end, servidores → DevOps, dados → Ciência de Dados, segurança → Cibersegurança, testes → QA, negócio → Produto.

| Trilha | Regra decisiva (+3) | Regras de suporte (+1/+2) | Desambiguação (negativas) |
|---|---|---|---|
| **1. Back-end** | R10: CONSTRUTOR, ferramenta ∈ {Java/C#, Python, SQL} e plataforma ∈ {web, indiferente} | R11 (+2): CONSTRUTOR e entrega = regras de negócio · R12 (+1): SQL e sem interesse em dados | — |
| **2. Front-end & UI/UX** | R13: VISUAL e JavaScript | R14 (+2): VISUAL e web · R15 (+1): produto final + web + JS | R35 (−1): plataforma = mobile |
| **3. Ciência de Dados / ML** | R16: ANALÍTICO e foco = modelar | R17 (+2): matemática alta e entrega = dados | R18 (−2): modelar com matemática baixa · R21 (−2): foco = pipelines |
| **4. Engenharia de Dados** | R19: foco = pipelines e ferramenta ∈ {Python, SQL} | R20 (+2): pipelines e entrega ∈ {dados, infraestrutura} | R22 (−2): foco = modelar |
| **5. Cibersegurança** | R23: DEFENSIVO e Linux/Redes | R24 (+2): atividade e entrega = segurança · R25 (+1): DEFENSIVO e matemática ≥ média | — |
| **6. DevOps & SRE** | R26: INFRA e AUTOMATIZADOR | R27 (+2): AUTOMATIZADOR e entrega = infraestrutura | R28 (−1): nuvem com automação ≤ média |
| **7. Cloud Architecture** | R29: INFRA e plataforma = nuvem | R30 (+2): entrega = infraestrutura e nuvem · R31 (+1): nuvem e comunicação ≥ média | R32 (−1): AUTOMATIZADOR fora da nuvem |
| **8. Mobile** | R33: plataforma = mobile e ferramenta ∈ {Kotlin/Swift/Dart, JS} | R34 (+2): mobile e entrega = produto final | — |
| **9. QA** | R36: DETALHISTA e AUTOMATIZADOR | R37 (+2): atividade = testes e entrega = qualidade · R38 (+1): DETALHISTA e linguagem de teste | — |
| **10. Gestão de Produtos** | R39: NEGÓCIOS | R40 (+1): comunicação alta e entrega ∈ {produto, estratégia} · R41 (+1): iniciante com comunicação alta | R42 (−2): comunicação baixa |

Ao todo são **43 regras**: R01 a R42 e R99.

## 5. Pares ambíguos e como são separados

| Par ambíguo | Dimensão decisiva | Regras envolvidas |
|---|---|---|
| Ciência de Dados × Engenharia de Dados | `dados_foco` (modelar × pipelines) e `matematica` | R16, R17, R18 × R19, R20; cruzadas R21 e R22 |
| DevOps × Cloud | `automacao` e `plataforma = nuvem` | R26, R27 × R29, R30, R31; cruzadas R28 e R32 |
| Front-end × Mobile | `plataforma` (web × mobile) | R13, R14 × R33, R34; R35 |
| Back-end × QA | `entrega` (regras de negócio × qualidade) | R10, R11 × R36, R37 |
| Produto × demais | `comunicacao` | R39, R40, R41; R42 |

## 6. Validação (Fase 4): personas de teste

| Persona | Respostas-chave | Esperado | Pontos | Regras decisivas |
|---|---|---|---|---|
| Ana (analítico) | mat. alta, dados, Python, modelar | Ciência de Dados | 6 | R16 |
| Bruno (dados/infra) | dados, SQL, pipelines, com. baixa | Eng. de Dados | 5 | R19 |
| Carla (infra/segurança) | segurança, Linux/Redes | Cibersegurança | 7 | R23 |
| Diego (visual) | layouts, JavaScript, web | Front-end | 7 | R13 |
| Elisa (negócios) | negócio, estratégia, com. alta | Produto | 6 | R39 |
| Fábio (lógico) | algoritmos, Java/C#, regras de negócio | Back-end | 6 | R10 |
| Gabriel (automação) | servidores, Linux, automação alta | DevOps | 6 | R26 |
| Helena (nuvem) | servidores, Linux, nuvem, com. alta | Cloud | 6 | R29 |
| Igor (mobile) | layouts, Kotlin/Swift/Dart, mobile | Mobile | 5 | R33 |
| Júlia (qualidade) | testes, Python, qualidade, automação alta | QA | 7 | R36 |

Resultado: **10/10 acertos**, verificados automaticamente em `tests/test_personas.py`.
