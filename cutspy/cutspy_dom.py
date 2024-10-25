from dataclasses import dataclass, field
from typing import TypeVar, Generic, Dict, Type
from abc import ABC, abstractmethod

class RenderableElement():...
        
class AbstractRender(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def render_element_starts(self, element: RenderableElement):
        raise NotImplementedError("Render is not implemented.")
        
    @abstractmethod
    def render_element_childs(self, element: RenderableElement):
        raise NotImplementedError("Render is not implemented.")
        
    @abstractmethod
    def render_element_ends(self, element: RenderableElement):
        raise NotImplementedError("Render is not implemented.")

class RenderableElement():
    def __init__(self):
        pass

    def accept(self, v: AbstractRender):
        v.render(self)


T = TypeVar('T')

@dataclass
class TypedDict(Generic[T]):
    _data: Dict[str, T] = field(default_factory=dict, init=False)
    _item_type: Type[T] = field(init=False)

    def __post_init__(self):
        self._item_type = self.__class__.__orig_bases__[0].__args__[0]
        print(self.__class__.__orig_bases__[0].__args__[0])

    def __getitem__(self, key: str) -> T:
        return self._data[key]
    
    def __setitem__(self, key: str, value: T) -> None:
        print(f" ============ {self._item_type}")
        if not isinstance(value, self._item_type):
            raise TypeError(f"Expected value of type {self._item_type.__name__}, but got {type(value).__name__}.")
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

@dataclass(frozen=True)
class Stock(RenderableElement):
    id: str
    lenght: float 
    cost: float
    stock: int 

@dataclass
class StocksList(TypedDict[Stock], RenderableElement):
    def append(self, value):
        self[value.id] = value

@dataclass(frozen=True)
class Part(RenderableElement):
    id: str
    lenght: float
    demand: int
    price: float

@dataclass
class PartsList(TypedDict[Part], RenderableElement):
    def append(self, value):
        if not isinstance(value, Part):
            raise TypeError(f"The value must be a Part instance, but it is {type(value)}.")
        self[value.id] = value

@dataclass(frozen=True)
class Cut(RenderableElement):
    part_id: str
    num_parts: int

@dataclass(frozen=True)
class Pattern(RenderableElement):
    _id_counter: int = field(init=False, default=0, repr=False)

    id: str = field(init=False)
    stock_id: str
    cuts: list[Cut] = field(default_factory=list)

    def __post_init__(self):
        type(self)._id_counter += 1
        object.__setattr__(self, "id", type(self)._id_counter)

@dataclass
class PatternsList(TypedDict[Pattern], RenderableElement):
    def append(self, value):
        if not isinstance(value, Pattern):
            raise TypeError(f"The value must be a Pattern instance, but it is {type(value)}.")
        self[value.stock_id] = value

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
class MultiObjectiveList():
    def append(self, value):
        if not isinstance(value, AbstractObjective):
            raise TypeError(f"The value must be an AbstractObjective instance, but it is {type(value)}.")
        if len(self) == 0:
            super.append(value)
        else:
            raise ValueError(f"Not implemented multiobjective version.")

@dataclass(frozen=True)
class CSPModel(AbstractObjective):
    objetives: MultiObjectiveList = field(default_factory=MultiObjectiveList)
    stocks: StocksList = field(default_factory=StocksList)
    parts: PartsList = field(default_factory=PartsList)
    Patterns: PatternsList = field(default_factory=PatternsList)

    def add_stock(self, id: str, lenght: float, cost: float=0, stock: int=0):
        s = Stock(id=id, lenght=lenght, cost=cost, stock=stock)
        self.stocks.append(s)

    def add_part(self, id: str, lenght: float, demand: int, price: float):
        p = Part(id=id, lenght=lenght, demand=demand, price=price)
        self.parts.append(p)

    def add_pattern(self, stock_id: str, cuts: list[Cut]):
        p = Pattern(stock_id=stock_id, cuts=cuts)

    def make_patterns(self):
        for i in self.parts:
            feasible = False
            for s in self.stocks:
                num_cuts = int(self.stocks[s])

@dataclass(frozen=True)
class BasicCSPModel(CSPModel):
    pass
