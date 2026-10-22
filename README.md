# 🧭 Consultor Inteligente de Carreiras em TI

Sistema Especialista baseado em regras, escrito em Python com **Experta** (motor de inferência com encadeamento para frente) e **Streamlit** (interface web). Ele entrevista o usuário e recomenda uma entre **10 trilhas de carreira em TI**, explicando quais regras levaram à decisão.

> Trabalho da disciplina de Inteligência Artificial, curso de Ciência da Computação, UNIPAC Barbacena.

## Trilhas recomendadas

1. Desenvolvimento Back-end
2. Desenvolvimento Front-end & UI/UX
3. Ciência de Dados e Machine Learning
4. Engenharia de Dados
5. Cibersegurança (Security / Pentesting)
6. DevOps & SRE
7. Computação em Nuvem (Cloud Architecture)
8. Desenvolvimento Mobile
9. Engenharia de Qualidade e Testes (QA)
10. Gestão de Produtos (Product Management)

## Instalação

Requer **Python 3.10 ou superior**.

```bash
git clone https://github.com/dcalixxto/sistema_especialista_regras_Python.git
cd sistema_especialista_regras_Python

python -m venv .venv
# Windows:      .venv\Scripts\activate
# Linux/macOS:  source .venv/bin/activate

pip install -r requirements.txt
```

## Execução

```bash
streamlit run app.py
```

O navegador abre em `http://localhost:8501`. A interface tem três abas:

- **Consultor**: a entrevista com 8 perguntas, a trilha recomendada, as regras que justificam a escolha, as características inferidas, a pontuação de todas as trilhas e os primeiros passos de estudo.
- **Base de conhecimento**: as 43 regras no formato SE … ENTÃO.
- **Validação (personas)**: as personas de teste rodadas ao vivo, com a taxa de acerto.

## Testes (validação com personas)

```bash
python -m pytest -v
```

Os testes conferem:

- as 10 personas, uma por trilha;
- os pares ambíguos (Ciência × Engenharia de Dados, DevOps × Cloud, Front-end × Mobile);
- a sincronia entre o catálogo de regras e o motor;
- 200 entrevistas aleatórias, garantindo que o sistema sempre chega a um diagnóstico.

## Como o sistema funciona

```
Respostas ──► Perfil ──► R01–R08: Características (ANALÍTICO, VISUAL, INFRA, …)
                     └─► R09–R42: Indícios (+3 decisiva, +1/+2 suporte, −1/−2 desambiguação)
                                     └─► R99: Diagnóstico (maior pontuação)
```

1. As respostas viram um fato `Perfil`.
2. As regras **R01 a R08** derivam fatos intermediários `Caracteristica`. Exemplo: matemática alta + dados → perfil **ANALÍTICO**.
3. As regras **R09 a R42** cruzam respostas e características e declaram fatos `Indicio` com peso e motivo. As regras de **desambiguação** têm peso negativo e separam trilhas parecidas. Exemplo: quem prefere *pipelines* perde pontos em Ciência de Dados, e quem prefere *modelar* perde pontos em Engenharia de Dados.
4. A regra **R99**, de menor prioridade (`salience=-100`), soma os indícios e declara o `Diagnostico`. Os indícios da trilha vencedora formam a justificativa mostrada ao usuário.

A matriz de decisão completa (Fase 1) está em [docs/matriz_decisao.md](docs/matriz_decisao.md).

## Estrutura do projeto

```
├── app.py                    # Interface web (Streamlit)
├── consultor/
│   ├── compat.py             # Compatibilidade do Experta com Python 3.10+
│   ├── conhecimento.py       # Trilhas, perguntas e catálogo legível das regras
│   ├── motor.py              # Fatos (Fact) e regras (@Rule) do Experta
│   └── personas.py           # Personas de teste
├── docs/matriz_decisao.md    # Engenharia de conhecimento / tabela de decisão
├── tests/test_personas.py    # Validação automatizada
└── requirements.txt
```

## Observação sobre o Experta no Python 3.10+

O Experta 1.9.4 depende do `frozendict==1.2`, que usa `collections.Mapping`, removido no Python 3.10. O módulo [`consultor/compat.py`](consultor/compat.py) restaura esse alias antes de importar o Experta. Por isso o projeto funciona sem nenhum ajuste manual; foi testado no Python 3.13.
