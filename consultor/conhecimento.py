"""Base de conhecimento declarativa: trilhas, perguntas da entrevista e catálogo de regras.

As regras executáveis ficam em ``motor.py``; o catálogo ``REGRAS`` abaixo é a versão
legível (SE/ENTÃO) usada pela interface e pela documentação (docs/matriz_decisao.md).
"""

# --------------------------------------------------------------------------- #
# As 10 trilhas de carreira (a ordem também é o critério final de desempate)
# --------------------------------------------------------------------------- #
TRILHAS = {
    "backend": {
        "nome": "Desenvolvimento Back-end",
        "icone": "🧩",
        "descricao": "Lógica de servidores, construção de APIs, regras de negócio e bancos de dados.",
        "passos": [
            "Domine uma linguagem de servidor (Java, C#, Python ou Go)",
            "SQL e modelagem de bancos relacionais",
            "APIs REST, autenticação (JWT/OAuth) e arquitetura em camadas",
            "Um framework: Spring Boot, .NET, Django ou FastAPI",
        ],
    },
    "frontend": {
        "nome": "Desenvolvimento Front-end & UI/UX",
        "icone": "🎨",
        "descricao": "Interfaces web responsivas, experiência do usuário e frameworks reativos.",
        "passos": [
            "HTML semântico, CSS moderno (Flexbox/Grid) e responsividade",
            "JavaScript/TypeScript em profundidade",
            "Um framework reativo: React, Vue ou Angular",
            "Fundamentos de UI/UX, acessibilidade e Figma",
        ],
    },
    "dados_ml": {
        "nome": "Ciência de Dados e Machine Learning",
        "icone": "🧠",
        "descricao": "Estatística, modelagem preditiva, análise de grandes massas de dados e IA.",
        "passos": [
            "Estatística, probabilidade e álgebra linear",
            "Python com Pandas, NumPy e visualização (Matplotlib/Seaborn)",
            "Machine Learning com scikit-learn",
            "Deep Learning (PyTorch/TensorFlow) e avaliação de modelos",
        ],
    },
    "eng_dados": {
        "nome": "Engenharia de Dados",
        "icone": "🛢️",
        "descricao": "Arquitetura de dados, pipelines ETL/ELT e infraestrutura para Data Lakes.",
        "passos": [
            "SQL avançado e modelagem dimensional (Data Warehouse)",
            "Python para ETL e orquestração (Airflow, Prefect)",
            "Processamento distribuído: Spark, Kafka",
            "Data Lakes / Lakehouse na nuvem (S3, BigQuery, Databricks)",
        ],
    },
    "seguranca": {
        "nome": "Cibersegurança (Security / Pentesting)",
        "icone": "🛡️",
        "descricao": "Defesa cibernética, análise de vulnerabilidades, criptografia e redes seguras.",
        "passos": [
            "Redes (TCP/IP, DNS, firewalls) e Linux",
            "OWASP Top 10 e análise de vulnerabilidades",
            "Ferramentas: Nmap, Burp Suite, Wireshark, Metasploit",
            "Certificações de entrada: Security+, eJPT; prática em CTFs",
        ],
    },
    "devops": {
        "nome": "DevOps & SRE",
        "icone": "⚙️",
        "descricao": "Automação de processos, integração e entrega contínua (CI/CD) e contêineres.",
        "passos": [
            "Linux, shell script e Git",
            "Contêineres com Docker e orquestração com Kubernetes",
            "Pipelines de CI/CD (GitHub Actions, GitLab CI, Jenkins)",
            "Infraestrutura como código (Terraform, Ansible) e observabilidade",
        ],
    },
    "cloud": {
        "nome": "Computação em Nuvem (Cloud Architecture)",
        "icone": "☁️",
        "descricao": "Planejamento, migração e gestão de infraestruturas escaláveis (AWS/Azure/GCP).",
        "passos": [
            "Fundamentos de redes, Linux e virtualização",
            "Serviços centrais de um provedor (computação, rede, armazenamento, IAM)",
            "Arquitetura escalável, alta disponibilidade e gestão de custos (FinOps)",
            "Certificações: AWS Solutions Architect, AZ-104/AZ-305, GCP ACE",
        ],
    },
    "mobile": {
        "nome": "Desenvolvimento Mobile",
        "icone": "📱",
        "descricao": "Ecossistema de dispositivos móveis, nativo ou multiplataforma (Flutter/React Native).",
        "passos": [
            "Escolha um caminho: nativo (Kotlin/Swift) ou multiplataforma (Flutter/React Native)",
            "Ciclo de vida de apps, navegação e gerenciamento de estado",
            "Consumo de APIs, armazenamento local e notificações",
            "Publicação nas lojas (Google Play / App Store)",
        ],
    },
    "qa": {
        "nome": "Engenharia de Qualidade e Testes (QA)",
        "icone": "🔍",
        "descricao": "Testes automatizados, confiabilidade de software e processos de qualidade.",
        "passos": [
            "Fundamentos de teste: técnicas, níveis e tipos (ISTQB CTFL)",
            "Automação de testes com Selenium, Cypress ou Playwright",
            "Testes de API (Postman, REST Assured) e testes unitários (pytest/JUnit)",
            "Integração dos testes em pipelines de CI",
        ],
    },
    "produto": {
        "nome": "Gestão de Produtos (Product Management)",
        "icone": "📊",
        "descricao": "Ponte entre negócio, design e desenvolvimento, métodos ágeis e priorização.",
        "passos": [
            "Métodos ágeis: Scrum, Kanban e OKRs",
            "Discovery de produto, entrevistas com usuários e prototipação",
            "Priorização (RICE, MoSCoW) e gestão de backlog",
            "Métricas de produto e noções de dados (SQL básico, analytics)",
        ],
    },
}

# --------------------------------------------------------------------------- #
# Perguntas da entrevista (chave -> opções {valor: rótulo})
# --------------------------------------------------------------------------- #
PERGUNTAS = [
    {
        "chave": "matematica",
        "pergunta": "Qual é a sua afinidade com matemática e estatística?",
        "opcoes": {"baixa": "Baixa", "media": "Média", "alta": "Alta"},
    },
    {
        "chave": "atividade",
        "pergunta": "No dia a dia, o que você mais gostaria de fazer?",
        "opcoes": {
            "algoritmos": "Escrever algoritmos e lógica de programação",
            "layouts": "Criar layouts e interfaces visuais",
            "servidores": "Lidar com servidores, redes e sistemas operacionais",
            "dados": "Analisar dados brutos",
            "seguranca": "Garantir a segurança de sistemas",
            "testes": "Encontrar falhas e testar software",
            "negocio": "Conversar com pessoas, organizar prioridades e decidir o que construir",
        },
    },
    {
        "chave": "ferramenta",
        "pergunta": "Com qual linguagem/ferramenta você tem mais afinidade hoje?",
        "opcoes": {
            "python": "Python",
            "javascript": "JavaScript / TypeScript",
            "java_csharp": "Java / C#",
            "sql": "SQL / Bancos de dados",
            "linux_redes": "Linux / Redes",
            "mobile": "Kotlin / Swift / Dart (Flutter)",
            "nenhuma": "Nenhuma / Sou iniciante",
        },
    },
    {
        "chave": "entrega",
        "pergunta": "Que tipo de entrega de valor mais te motiva?",
        "opcoes": {
            "produto_usuario": "O produto final que o usuário vê e usa",
            "regras_negocio": "A lógica e as APIs que fazem o sistema funcionar por trás",
            "infraestrutura": "A infraestrutura que sustenta o sistema",
            "seguranca": "A proteção contra invasões e vazamentos",
            "dados": "Informações e insights extraídos de dados",
            "qualidade": "A garantia de que o software funciona sem falhas",
            "estrategia": "A estratégia e a visão do produto para o negócio",
        },
    },
    {
        "chave": "dados_foco",
        "pergunta": "Diante de uma grande massa de dados, o que mais te atrai?",
        "opcoes": {
            "modelar": "Descobrir padrões e criar modelos que fazem previsões",
            "pipelines": "Organizar, transportar e armazenar os dados de forma confiável",
            "nenhum": "Trabalhar com dados não me atrai muito",
        },
    },
    {
        "chave": "plataforma",
        "pergunta": "Em qual plataforma você prefere que seu trabalho rode?",
        "opcoes": {
            "web": "Navegadores (aplicações web)",
            "mobile": "Celulares e tablets",
            "nuvem": "Plataformas de nuvem (AWS, Azure, GCP)",
            "indiferente": "Indiferente",
        },
    },
    {
        "chave": "automacao",
        "pergunta": "Quanto você gosta de automatizar tarefas repetitivas (scripts, pipelines, CI/CD)?",
        "opcoes": {"baixa": "Pouco", "media": "Moderadamente", "alta": "Muito"},
    },
    {
        "chave": "comunicacao",
        "pergunta": "Quanto você gosta de negociar, apresentar ideias e lidar com clientes e equipes?",
        "opcoes": {"baixa": "Pouco", "media": "Moderadamente", "alta": "Muito"},
    },
]

# --------------------------------------------------------------------------- #
# Catálogo legível das regras (espelha motor.py)
# tipo: "caracteristica" (fato intermediário), "afinidade", "decisiva" (peso 3),
#       "suporte" (peso 1-2), "desambiguacao" (peso negativo), "diagnostico"
# --------------------------------------------------------------------------- #
REGRAS = {
    # Nível 1 — características derivadas (encadeamento para frente)
    "R01": ("caracteristica", "SE matemática = alta E (atividade = dados OU ferramenta = Python) ENTÃO perfil ANALÍTICO"),
    "R02": ("caracteristica", "SE atividade = layouts ENTÃO perfil VISUAL"),
    "R03": ("caracteristica", "SE atividade = servidores OU ferramenta = Linux/Redes OU entrega = infraestrutura ENTÃO perfil INFRA"),
    "R04": ("caracteristica", "SE atividade = algoritmos OU ferramenta = Java/C# ENTÃO perfil CONSTRUTOR"),
    "R05": ("caracteristica", "SE atividade = segurança OU entrega = segurança ENTÃO perfil DEFENSIVO"),
    "R06": ("caracteristica", "SE automação = alta ENTÃO perfil AUTOMATIZADOR"),
    "R07": ("caracteristica", "SE atividade = testes OU entrega = qualidade ENTÃO perfil DETALHISTA"),
    "R08": ("caracteristica", "SE comunicação = alta E (atividade = negócio OU entrega = estratégia) ENTÃO perfil NEGÓCIOS"),
    "R09": ("afinidade", "SE atividade preferida = X ENTÃO +1 na trilha associada a X"),
    # Back-end
    "R10": ("decisiva", "SE CONSTRUTOR E ferramenta ∈ {Java/C#, Python, SQL} E plataforma ∈ {web, indiferente} ENTÃO Back-end +3"),
    "R11": ("suporte", "SE CONSTRUTOR E entrega = regras de negócio/APIs ENTÃO Back-end +2"),
    "R12": ("suporte", "SE ferramenta = SQL E foco em dados = nenhum ENTÃO Back-end +1"),
    # Front-end
    "R13": ("decisiva", "SE VISUAL E ferramenta = JavaScript ENTÃO Front-end +3"),
    "R14": ("suporte", "SE VISUAL E plataforma = web ENTÃO Front-end +2"),
    "R15": ("suporte", "SE entrega = produto final E plataforma = web E ferramenta = JavaScript ENTÃO Front-end +1"),
    # Ciência de Dados
    "R16": ("decisiva", "SE ANALÍTICO E foco em dados = modelar/prever ENTÃO Ciência de Dados +3"),
    "R17": ("suporte", "SE matemática = alta E entrega = insights de dados ENTÃO Ciência de Dados +2"),
    "R18": ("desambiguacao", "SE foco em dados = modelar E matemática = baixa ENTÃO Ciência de Dados −2"),
    # Engenharia de Dados
    "R19": ("decisiva", "SE foco em dados = pipelines E ferramenta ∈ {Python, SQL} ENTÃO Engenharia de Dados +3"),
    "R20": ("suporte", "SE foco em dados = pipelines E entrega ∈ {dados, infraestrutura} ENTÃO Engenharia de Dados +2"),
    "R21": ("desambiguacao", "SE foco em dados = pipelines ENTÃO Ciência de Dados −2 (DS × DE)"),
    "R22": ("desambiguacao", "SE foco em dados = modelar ENTÃO Engenharia de Dados −2 (DS × DE)"),
    # Segurança
    "R23": ("decisiva", "SE DEFENSIVO E ferramenta = Linux/Redes ENTÃO Cibersegurança +3"),
    "R24": ("suporte", "SE atividade = segurança E entrega = segurança ENTÃO Cibersegurança +2"),
    "R25": ("suporte", "SE DEFENSIVO E matemática ∈ {média, alta} ENTÃO Cibersegurança +1 (criptografia)"),
    # DevOps
    "R26": ("decisiva", "SE INFRA E AUTOMATIZADOR ENTÃO DevOps +3"),
    "R27": ("suporte", "SE AUTOMATIZADOR E entrega = infraestrutura ENTÃO DevOps +2"),
    "R28": ("desambiguacao", "SE plataforma = nuvem E automação ∈ {baixa, média} ENTÃO DevOps −1 (DevOps × Cloud)"),
    # Cloud
    "R29": ("decisiva", "SE INFRA E plataforma = nuvem ENTÃO Cloud +3"),
    "R30": ("suporte", "SE entrega = infraestrutura E plataforma = nuvem ENTÃO Cloud +2"),
    "R31": ("suporte", "SE plataforma = nuvem E comunicação ∈ {média, alta} ENTÃO Cloud +1 (arquitetura com stakeholders)"),
    "R32": ("desambiguacao", "SE AUTOMATIZADOR E plataforma ≠ nuvem ENTÃO Cloud −1 (DevOps × Cloud)"),
    # Mobile
    "R33": ("decisiva", "SE plataforma = mobile E ferramenta ∈ {Kotlin/Swift/Dart, JavaScript} ENTÃO Mobile +3"),
    "R34": ("suporte", "SE plataforma = mobile E entrega = produto final ENTÃO Mobile +2"),
    "R35": ("desambiguacao", "SE plataforma = mobile ENTÃO Front-end −1 (Front × Mobile)"),
    # QA
    "R36": ("decisiva", "SE DETALHISTA E AUTOMATIZADOR ENTÃO QA +3 (testes automatizados)"),
    "R37": ("suporte", "SE atividade = testes E entrega = qualidade ENTÃO QA +2"),
    "R38": ("suporte", "SE DETALHISTA E ferramenta ∈ {Python, JavaScript, Java/C#} ENTÃO QA +1"),
    # Produto
    "R39": ("decisiva", "SE NEGÓCIOS ENTÃO Gestão de Produtos +3"),
    "R40": ("suporte", "SE comunicação = alta E entrega ∈ {produto final, estratégia} ENTÃO Gestão de Produtos +1"),
    "R41": ("suporte", "SE ferramenta = nenhuma E comunicação = alta ENTÃO Gestão de Produtos +1"),
    "R42": ("desambiguacao", "SE comunicação = baixa ENTÃO Gestão de Produtos −2"),
    # Conclusão
    "R99": ("diagnostico", "SE todas as regras anteriores já dispararam ENTÃO recomendar a trilha de maior pontuação "
                           "(desempate: mais regras decisivas, depois ordem da lista)"),
}
