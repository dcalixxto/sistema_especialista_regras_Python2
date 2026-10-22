"""Personas de teste (Fase 4) — uma para cada trilha, com a recomendação esperada."""

PERSONAS = [
    {
        "nome": "Ana — perfil analítico",
        "esperado": "dados_ml",
        "respostas": dict(matematica="alta", atividade="dados", ferramenta="python", entrega="dados",
                          dados_foco="modelar", plataforma="indiferente", automacao="media", comunicacao="media"),
    },
    {
        "nome": "Bruno — perfil de dados/infra",
        "esperado": "eng_dados",
        "respostas": dict(matematica="media", atividade="dados", ferramenta="sql", entrega="dados",
                          dados_foco="pipelines", plataforma="indiferente", automacao="media", comunicacao="baixa"),
    },
    {
        "nome": "Carla — perfil infra/segurança",
        "esperado": "seguranca",
        "respostas": dict(matematica="media", atividade="seguranca", ferramenta="linux_redes", entrega="seguranca",
                          dados_foco="nenhum", plataforma="indiferente", automacao="media", comunicacao="media"),
    },
    {
        "nome": "Diego — perfil visual/front-end",
        "esperado": "frontend",
        "respostas": dict(matematica="baixa", atividade="layouts", ferramenta="javascript", entrega="produto_usuario",
                          dados_foco="nenhum", plataforma="web", automacao="baixa", comunicacao="media"),
    },
    {
        "nome": "Elisa — perfil negócios/produto",
        "esperado": "produto",
        "respostas": dict(matematica="media", atividade="negocio", ferramenta="nenhuma", entrega="estrategia",
                          dados_foco="nenhum", plataforma="indiferente", automacao="baixa", comunicacao="alta"),
    },
    {
        "nome": "Fábio — perfil lógico/back-end",
        "esperado": "backend",
        "respostas": dict(matematica="media", atividade="algoritmos", ferramenta="java_csharp", entrega="regras_negocio",
                          dados_foco="nenhum", plataforma="web", automacao="media", comunicacao="media"),
    },
    {
        "nome": "Gabriel — perfil automação/DevOps",
        "esperado": "devops",
        "respostas": dict(matematica="media", atividade="servidores", ferramenta="linux_redes", entrega="infraestrutura",
                          dados_foco="nenhum", plataforma="indiferente", automacao="alta", comunicacao="media"),
    },
    {
        "nome": "Helena — perfil arquitetura em nuvem",
        "esperado": "cloud",
        "respostas": dict(matematica="media", atividade="servidores", ferramenta="linux_redes", entrega="infraestrutura",
                          dados_foco="nenhum", plataforma="nuvem", automacao="media", comunicacao="alta"),
    },
    {
        "nome": "Igor — perfil mobile",
        "esperado": "mobile",
        "respostas": dict(matematica="media", atividade="layouts", ferramenta="mobile", entrega="produto_usuario",
                          dados_foco="nenhum", plataforma="mobile", automacao="baixa", comunicacao="media"),
    },
    {
        "nome": "Júlia — perfil qualidade/QA",
        "esperado": "qa",
        "respostas": dict(matematica="media", atividade="testes", ferramenta="python", entrega="qualidade",
                          dados_foco="nenhum", plataforma="web", automacao="alta", comunicacao="media"),
    },
]
