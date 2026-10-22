"""Consultor Inteligente de Carreiras em TI — Sistema Especialista baseado em regras."""

from .conhecimento import PERGUNTAS, REGRAS, TRILHAS
from .motor import ConsultorCarreira, Resultado, diagnosticar

__all__ = ["PERGUNTAS", "REGRAS", "TRILHAS", "ConsultorCarreira", "Resultado", "diagnosticar"]
