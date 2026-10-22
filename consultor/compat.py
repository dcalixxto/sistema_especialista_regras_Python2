"""Compatibilidade do Experta com Python 3.10+.

O Experta 1.9.4 depende do ``frozendict==1.2``, que usa ``collections.Mapping``.
Esses aliases foram removidos do módulo ``collections`` no Python 3.10 (eles
vivem em ``collections.abc``). Este módulo restaura os aliases e precisa ser
importado ANTES do ``experta``.
"""

import collections
import collections.abc

for _nome in ("Mapping", "MutableMapping", "Sequence", "Iterable", "Hashable", "Callable"):
    if not hasattr(collections, _nome):
        setattr(collections, _nome, getattr(collections.abc, _nome))
