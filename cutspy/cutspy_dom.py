from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Generic, Type, TypeVar


class RenderableElement:
    pass


class AbstractRender(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def render(self, element: RenderableElement):
        raise NotImplementedError("Render is not implemented.")


class RenderableElement:
    def __init__(self):
        pass

    def accept(self, v: AbstractRender):
        v.render(self)


T = TypeVar("T")


@dataclass
class TypedDict(Generic[T]):
    _data: Dict[str, T] = field(default_factory=dict, init=False)
    _item_type: Type[T] = field(init=False)

    def __post_init__(self):
        self._item_type = self.__class__.__orig_bases__[0].__args__[0]

    def __getitem__(self, key: str) -> T:
        return self._data[key]

    def __setitem__(self, key: str, value: T) -> None:
        if not isinstance(value, self._item_type):
            raise TypeError(
                f"Expected value of type {self._item_type.__name__}, "
                f"but got {type(value).__name__}."
            )
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"TypedDict({self._data})"

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()


@dataclass(frozen=True)
class Stock(RenderableElement):
    name: str
    lenght: float
    cost: float
    stock: int


@dataclass
class StocksList(TypedDict[Stock], RenderableElement):
    def append(self, value):
        self[value.name] = value


@dataclass(frozen=True)
class Part(RenderableElement):
    name: str
    lenght: float
    demand: int
    price: float


@dataclass
class PartsList(TypedDict[Part], RenderableElement):
    def append(self, value):
        self[value.name] = value


@dataclass(frozen=True)
class Cut(RenderableElement):
    part_name: str
    num_parts: int


@dataclass(frozen=True)
class Pattern(RenderableElement):
    _name_counter: int = field(init=False, default=0, repr=False)

    name: str = field(init=False)
    stock_name: str
    cuts: list[Cut] = field(default_factory=list)

    def __post_init__(self):
        type(self)._name_counter += 1
        object.__setattr__(self, "name", type(self)._name_counter)


@dataclass
class PatternsList(TypedDict[Pattern], RenderableElement):
    def append(self, value):
        if not isinstance(value, Pattern):
            raise TypeError(
                f"The value must be a Pattern instance, "
                f"but it is {type(value)}."
            )
        self[value.stock_name] = value


@dataclass(frozen=True)
class AbstractObjective(RenderableElement):
    pass


@dataclass(frozen=True)
class MinimumCostObjective(AbstractObjective):
    pass


@dataclass(frozen=True)
class MaximizeIncomeObjective(AbstractObjective):
    pass


@dataclass(frozen=True)
class MinimizeScrapObjective(AbstractObjective):
    pass


@dataclass(frozen=True)
class AbstractMultiObjectiveList(list, RenderableElement):
    pass


@dataclass()
class MultiObjectiveList:
    def append(self, value):
        if not isinstance(value, AbstractObjective):
            raise TypeError(
                f"The value must be an AbstractObjective instance, "
                f"but it is {type(value)}."
            )
        if len(self) == 0:
            super.append(value)
        else:
            raise ValueError("Not implemented multiobjective version.")


@dataclass(frozen=True)
class CSPModel(AbstractObjective):
    objetives: MultiObjectiveList = field(default_factory=MultiObjectiveList)
    stocks: StocksList = field(default_factory=StocksList)
    parts: PartsList = field(default_factory=PartsList)
    patterns: PatternsList = field(default_factory=PatternsList)

    def add_stock(
        self,
        name: str,
        lenght: float,
        cost: float = 0,
        stock: int = 0,
    ):
        s = Stock(name=name, lenght=lenght, cost=cost, stock=stock)
        self.stocks.append(s)

    def add_part(
        self, name: str, lenght: float, demand: int, price: float = 0
    ):
        p = Part(name=name, lenght=lenght, demand=demand, price=price)
        self.parts.append(p)

    def add_pattern(self, stock_name: str, cuts: list[Cut]):
        p = Pattern(stock_name=stock_name, cuts=cuts)

    def make_patterns(self):
        patterns = []
        for f in self.parts.values():
            feasible = False
            for s in self.stocks.values():
                num_cuts = int(s.lenght / f.lenght)

                if num_cuts > 0:
                    feasible = True
                    cuts_dict = {key: 0 for key in self.parts.keys()}
                    cuts_dict[f.name] = num_cuts
                    patterns.append({"stock": s.name, "cuts": cuts_dict})

            if not feasible:
                print(f"No feasible pattern was found for {f.name}")
                patterns = []
        return patterns

    def accept(self, v: AbstractRender):
        v.render(self)
        v.render(self.stocks)
        v.render(self.parts)
        v.render(self.patterns)
        v.render(self.objetives)


@dataclass(frozen=True)
class BasicCSPModel(CSPModel):
    pass
