from typing import Sequence, Callable, List, Any, overload, override

from mods_base import BaseOption

type LoaderFunc = Callable[[], List[BaseOption]]


class LazyLoadedOptionSequence(Sequence):
    _loader_func: LoaderFunc | None
    _list: List[Any] | None

    def __init__(self, loader_func: LoaderFunc):
        self._loader_func = loader_func
        self._list = None

    def _lazy_load(self):
        if self._list is not None:
            return
        self._list = self._loader_func()
        self._loader_func = None

    @override
    def __len__(self):
        self._lazy_load()
        return len(self._list)

    @overload
    def __getitem__(self, index: int) -> BaseOption: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[BaseOption]: ...

    def __getitem__(self, index):
        self._lazy_load()
        return self._list.__getitem__(index)
