"""Motor de inferência (Experta) do Consultor de Carreiras em TI.

Funcionamento (encadeamento para frente):
  1. As respostas da entrevista viram um fato ``Perfil``.
  2. Regras R01–R08 derivam fatos intermediários ``Caracteristica`` (ex.: perfil analítico).
  3. Regras R09–R42 cruzam ``Perfil`` e ``Caracteristica`` e declaram fatos ``Indicio``
     (pontos positivos ou negativos para uma trilha, sempre com o motivo).
  4. A regra R99 (menor prioridade) consolida os indícios e declara o ``Diagnostico``.
"""

from dataclasses import dataclass, field

from . import compat  # noqa: F401  (precisa ser importado antes do experta)
from experta import L, MATCH, NOT, OR, Fact, Field, KnowledgeEngine, P, Rule

from .conhecimento import PERGUNTAS, TRILHAS


def em(*valores):
    """Restrição de campo: o valor do fato pertence ao conjunto informado."""
    return P(lambda v: v in valores)


# --------------------------------------------------------------------------- #
# Fatos
# --------------------------------------------------------------------------- #
class Perfil(Fact):
    """Respostas do usuário à entrevista."""

    matematica = Field(str, mandatory=True)
    atividade = Field(str, mandatory=True)
    ferramenta = Field(str, mandatory=True)
    entrega = Field(str, mandatory=True)
    dados_foco = Field(str, mandatory=True)
    plataforma = Field(str, mandatory=True)
    automacao = Field(str, mandatory=True)
    comunicacao = Field(str, mandatory=True)


class Caracteristica(Fact):
    """Traço de perfil inferido a partir das respostas (fato intermediário)."""

    nome = Field(str, mandatory=True)
    regra = Field(str, mandatory=True)
    motivo = Field(str, mandatory=True)


class Indicio(Fact):
    """Evidência a favor (peso > 0) ou contra (peso < 0) uma trilha."""

    trilha = Field(str, mandatory=True)
    peso = Field(int, mandatory=True)
    regra = Field(str, mandatory=True)
    motivo = Field(str, mandatory=True)


class Diagnostico(Fact):
    """Conclusão final do sistema."""

    trilha = Field(str, mandatory=True)


# Afinidade direta entre a atividade preferida e uma trilha (usada pela R09)
AFINIDADE_ATIVIDADE = {
    "algoritmos": "backend",
    "layouts": "frontend",
    "servidores": "devops",
    "dados": "dados_ml",
    "seguranca": "seguranca",
    "testes": "qa",
    "negocio": "produto",
}


# --------------------------------------------------------------------------- #
# Motor
# --------------------------------------------------------------------------- #
class ConsultorCarreira(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.ranking = []
        self.vencedora = None

    # Helpers ---------------------------------------------------------------- #
    def _caracteristica(self, nome, regra, motivo):
        self.declare(Caracteristica(nome=nome, regra=regra, motivo=motivo))

    def _indicio(self, trilha, peso, regra, motivo):
        self.declare(Indicio(trilha=trilha, peso=peso, regra=regra, motivo=motivo))

    # ======================= Nível 1: características ======================= #
    @Rule(OR(Perfil(matematica="alta", atividade="dados"),
             Perfil(matematica="alta", ferramenta="python")))
    def r01_analitico(self):
        self._caracteristica("analitico", "R01", "Alta afinidade com matemática aliada a dados/Python")

    @Rule(Perfil(atividade="layouts"))
    def r02_visual(self):
        self._caracteristica("visual", "R02", "Prefere criar layouts e interfaces visuais")

    @Rule(OR(Perfil(atividade="servidores"),
             Perfil(ferramenta="linux_redes"),
             Perfil(entrega="infraestrutura")))
    def r03_infra(self):
        self._caracteristica("infra", "R03", "Interesse por servidores, redes ou infraestrutura")

    @Rule(OR(Perfil(atividade="algoritmos"), Perfil(ferramenta="java_csharp")))
    def r04_construtor(self):
        self._caracteristica("construtor", "R04", "Gosta de construir lógica e algoritmos")

    @Rule(OR(Perfil(atividade="seguranca"), Perfil(entrega="seguranca")))
    def r05_defensivo(self):
        self._caracteristica("defensivo", "R05", "Motivação por proteger sistemas")

    @Rule(Perfil(automacao="alta"))
    def r06_automatizador(self):
        self._caracteristica("automatizador", "R06", "Gosta muito de automatizar tarefas")

    @Rule(OR(Perfil(atividade="testes"), Perfil(entrega="qualidade")))
    def r07_detalhista(self):
        self._caracteristica("detalhista", "R07", "Foco em encontrar falhas e garantir qualidade")

    @Rule(OR(Perfil(comunicacao="alta", atividade="negocio"),
             Perfil(comunicacao="alta", entrega="estrategia")))
    def r08_negocios(self):
        self._caracteristica("negocios", "R08", "Comunicação forte com visão de negócio")

    # ======================= Afinidade direta ================================ #
    @Rule(Perfil(atividade=MATCH.atividade))
    def r09_afinidade_atividade(self, atividade):
        rotulo = PERGUNTAS[1]["opcoes"][atividade]
        self._indicio(AFINIDADE_ATIVIDADE[atividade], 1, "R09", f"Atividade preferida: {rotulo.lower()}")

    # ======================= Back-end ======================================== #
    @Rule(Caracteristica(nome="construtor"),
          Perfil(ferramenta=em("java_csharp", "python", "sql"), plataforma=em("web", "indiferente")))
    def r10_backend_decisiva(self):
        self._indicio("backend", 3, "R10", "Perfil construtor com linguagem de servidor, sem foco em mobile/nuvem")

    @Rule(Caracteristica(nome="construtor"), Perfil(entrega="regras_negocio"))
    def r11_backend_regras_negocio(self):
        self._indicio("backend", 2, "R11", "Quer entregar a lógica e as APIs por trás do sistema")

    @Rule(Perfil(ferramenta="sql", dados_foco="nenhum"))
    def r12_backend_sql(self):
        self._indicio("backend", 1, "R12", "Domina SQL, mas com foco em sistemas, não em análise de dados")

    # ======================= Front-end ======================================= #
    @Rule(Caracteristica(nome="visual"), Perfil(ferramenta="javascript"))
    def r13_frontend_decisiva(self):
        self._indicio("frontend", 3, "R13", "Perfil visual aliado a JavaScript")

    @Rule(Caracteristica(nome="visual"), Perfil(plataforma="web"))
    def r14_frontend_web(self):
        self._indicio("frontend", 2, "R14", "Perfil visual com preferência pela web")

    @Rule(Perfil(entrega="produto_usuario", plataforma="web", ferramenta="javascript"))
    def r15_frontend_produto_web(self):
        self._indicio("frontend", 1, "R15", "Quer entregar o produto final na web com JavaScript")

    # ======================= Ciência de Dados ================================ #
    @Rule(Caracteristica(nome="analitico"), Perfil(dados_foco="modelar"))
    def r16_dados_ml_decisiva(self):
        self._indicio("dados_ml", 3, "R16", "Perfil analítico interessado em modelos preditivos")

    @Rule(Perfil(matematica="alta", entrega="dados"))
    def r17_dados_ml_insights(self):
        self._indicio("dados_ml", 2, "R17", "Matemática forte e motivação por gerar insights")

    @Rule(Perfil(dados_foco="modelar", matematica="baixa"))
    def r18_dados_ml_sem_matematica(self):
        self._indicio("dados_ml", -2, "R18", "Modelagem preditiva exige base matemática, que foi declarada baixa")

    # ======================= Engenharia de Dados ============================= #
    @Rule(Perfil(dados_foco="pipelines", ferramenta=em("python", "sql")))
    def r19_eng_dados_decisiva(self):
        self._indicio("eng_dados", 3, "R19", "Quer construir pipelines e domina Python/SQL")

    @Rule(Perfil(dados_foco="pipelines", entrega=em("dados", "infraestrutura")))
    def r20_eng_dados_entrega(self):
        self._indicio("eng_dados", 2, "R20", "Pipelines de dados como entrega de valor")

    @Rule(Perfil(dados_foco="pipelines"))
    def r21_desambigua_ds(self):
        self._indicio("dados_ml", -2, "R21", "Prefere mover/armazenar dados a modelá-los (Engenharia × Ciência)")

    @Rule(Perfil(dados_foco="modelar"))
    def r22_desambigua_de(self):
        self._indicio("eng_dados", -2, "R22", "Prefere modelar dados a construir pipelines (Ciência × Engenharia)")

    # ======================= Cibersegurança ================================== #
    @Rule(Caracteristica(nome="defensivo"), Perfil(ferramenta="linux_redes"))
    def r23_seguranca_decisiva(self):
        self._indicio("seguranca", 3, "R23", "Motivação defensiva com base em Linux/Redes")

    @Rule(Perfil(atividade="seguranca", entrega="seguranca"))
    def r24_seguranca_convicta(self):
        self._indicio("seguranca", 2, "R24", "Atividade e entrega de valor voltadas à segurança")

    @Rule(Caracteristica(nome="defensivo"), Perfil(matematica=em("media", "alta")))
    def r25_seguranca_cripto(self):
        self._indicio("seguranca", 1, "R25", "Base matemática útil para criptografia")

    # ======================= DevOps & SRE ==================================== #
    @Rule(Caracteristica(nome="infra"), Caracteristica(nome="automatizador"))
    def r26_devops_decisiva(self):
        self._indicio("devops", 3, "R26", "Perfil de infraestrutura com forte gosto por automação")

    @Rule(Caracteristica(nome="automatizador"), Perfil(entrega="infraestrutura"))
    def r27_devops_entrega(self):
        self._indicio("devops", 2, "R27", "Quer automatizar a infraestrutura que sustenta o sistema")

    @Rule(Perfil(plataforma="nuvem", automacao=em("baixa", "media")))
    def r28_desambigua_devops(self):
        self._indicio("devops", -1, "R28", "Foco em nuvem sem paixão por automação (Cloud × DevOps)")

    # ======================= Cloud =========================================== #
    @Rule(Caracteristica(nome="infra"), Perfil(plataforma="nuvem"))
    def r29_cloud_decisiva(self):
        self._indicio("cloud", 3, "R29", "Perfil de infraestrutura com preferência por nuvem")

    @Rule(Perfil(entrega="infraestrutura", plataforma="nuvem"))
    def r30_cloud_entrega(self):
        self._indicio("cloud", 2, "R30", "Quer entregar infraestrutura escalável na nuvem")

    @Rule(Perfil(plataforma="nuvem", comunicacao=em("media", "alta")))
    def r31_cloud_arquitetura(self):
        self._indicio("cloud", 1, "R31", "Comunicação para desenhar arquiteturas com stakeholders")

    @Rule(Caracteristica(nome="automatizador"), Perfil(plataforma=~L("nuvem")))
    def r32_desambigua_cloud(self):
        self._indicio("cloud", -1, "R32", "Ama automação, mas não tem a nuvem como foco (DevOps × Cloud)")

    # ======================= Mobile ========================================== #
    @Rule(Perfil(plataforma="mobile", ferramenta=em("mobile", "javascript")))
    def r33_mobile_decisiva(self):
        self._indicio("mobile", 3, "R33", "Prefere dispositivos móveis e domina tecnologia mobile")

    @Rule(Perfil(plataforma="mobile", entrega="produto_usuario"))
    def r34_mobile_produto(self):
        self._indicio("mobile", 2, "R34", "Quer entregar o app que o usuário usa no celular")

    @Rule(Perfil(plataforma="mobile"))
    def r35_desambigua_frontend(self):
        self._indicio("frontend", -1, "R35", "Preferência por celulares em vez de navegadores (Mobile × Front-end)")

    # ======================= QA ============================================== #
    @Rule(Caracteristica(nome="detalhista"), Caracteristica(nome="automatizador"))
    def r36_qa_decisiva(self):
        self._indicio("qa", 3, "R36", "Detalhista que gosta de automação: testes automatizados")

    @Rule(Perfil(atividade="testes", entrega="qualidade"))
    def r37_qa_convicto(self):
        self._indicio("qa", 2, "R37", "Atividade e entrega de valor voltadas à qualidade")

    @Rule(Caracteristica(nome="detalhista"), Perfil(ferramenta=em("python", "javascript", "java_csharp")))
    def r38_qa_linguagem(self):
        self._indicio("qa", 1, "R38", "Domina uma linguagem usada em frameworks de teste")

    # ======================= Gestão de Produtos ============================== #
    @Rule(Caracteristica(nome="negocios"))
    def r39_produto_decisiva(self):
        self._indicio("produto", 3, "R39", "Comunicação forte com visão de negócio")

    @Rule(Perfil(comunicacao="alta", entrega=em("produto_usuario", "estrategia")))
    def r40_produto_visao(self):
        self._indicio("produto", 1, "R40", "Gosta de pessoas e pensa no produto/estratégia")

    @Rule(Perfil(ferramenta="nenhuma", comunicacao="alta"))
    def r41_produto_iniciante(self):
        self._indicio("produto", 1, "R41", "Iniciante técnico com boa comunicação")

    @Rule(Perfil(comunicacao="baixa"))
    def r42_desambigua_produto(self):
        self._indicio("produto", -2, "R42", "Gestão de produto exige muita comunicação, declarada baixa")

    # ======================= Diagnóstico ===================================== #
    @Rule(Perfil(), NOT(Diagnostico()), salience=-100)
    def r99_diagnostico(self):
        indicios = [f for f in self.facts.values() if isinstance(f, Indicio)]
        ordem = list(TRILHAS)
        pontos = {t: 0 for t in TRILHAS}
        decisivas = {t: 0 for t in TRILHAS}
        for ind in indicios:
            pontos[ind["trilha"]] += ind["peso"]
            if ind["peso"] >= 3:
                decisivas[ind["trilha"]] += 1

        self.ranking = sorted(TRILHAS, key=lambda t: (-pontos[t], -decisivas[t], ordem.index(t)))
        self.ranking = [(t, pontos[t]) for t in self.ranking]
        self.vencedora = self.ranking[0][0]
        self.declare(Diagnostico(trilha=self.vencedora))


# --------------------------------------------------------------------------- #
# API de alto nível
# --------------------------------------------------------------------------- #
@dataclass
class Resultado:
    trilha: str
    ranking: list                                       # [(trilha, pontos)] em ordem decrescente
    justificativas: list                                # indícios da trilha vencedora
    caracteristicas: list                               # traços inferidos (nível 1)
    regras_disparadas: list = field(default_factory=list)

    @property
    def info(self):
        return TRILHAS[self.trilha]

    @property
    def pontos(self):
        return self.ranking[0][1]


def diagnosticar(respostas: dict) -> Resultado:
    """Executa o motor de inferência sobre as respostas e devolve o diagnóstico."""
    faltando = [p["chave"] for p in PERGUNTAS if p["chave"] not in respostas]
    if faltando:
        raise ValueError(f"Respostas faltando: {', '.join(faltando)}")
    for p in PERGUNTAS:
        if respostas[p["chave"]] not in p["opcoes"]:
            raise ValueError(f"Valor inválido para '{p['chave']}': {respostas[p['chave']]!r}")

    motor = ConsultorCarreira()
    motor.reset()
    motor.declare(Perfil(**{p["chave"]: respostas[p["chave"]] for p in PERGUNTAS}))
    motor.run()

    fatos = list(motor.facts.values())
    indicios = [dict(f.as_dict()) for f in fatos if isinstance(f, Indicio)]
    caracteristicas = [dict(f.as_dict()) for f in fatos if isinstance(f, Caracteristica)]
    justificativas = sorted(
        (i for i in indicios if i["trilha"] == motor.vencedora),
        key=lambda i: (-i["peso"], i["regra"]),
    )
    regras = sorted({i["regra"] for i in indicios} | {c["regra"] for c in caracteristicas} | {"R99"})

    return Resultado(
        trilha=motor.vencedora,
        ranking=motor.ranking,
        justificativas=justificativas,
        caracteristicas=sorted(caracteristicas, key=lambda c: c["regra"]),
        regras_disparadas=regras,
    )
