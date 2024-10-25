from abc import ABC
from functools import singledispatchmethod
import io
from dataclasses import dataclass, field
from cutspy_dom import (
    RenderableElement,
    AbstractRender,
    TypedDict,
    Stock,
    StocksList,
    Part,
    PartsList,
    Cut,
    PatternsList,
    AbstractObjective,
    MinimumCostObjective,
    MaximizeIncomeObjective,
    MinimizeScrapObjective,
    AbstractMultiObjectiveList,
    MultiObjectiveList,
    CSPModel
)

@dataclass
class TextModelRender(AbstractRender):
    def __init__(self):
        super().__init__()
        _objectiveBuffer: io.StringIO = field(default_factory=io.StringIO)
        _restricctions: io.StringIO = field(default_factory=io.StringIO)

    @singledispatchmethod
    def render(self, element: RenderableElement):
        raise NotImplementedError("Render is not implemented.")
    
    @render.register
    def _(self, element: Stock):
        pass

    @render.register
    def _(self, element: StocksList):
        pass

    @render.register
    def _(self, element: Part):
        pass

    @render.register
    def _(self, element: PartsList):
        pass

    @render.register
    def _(self, element: Cut):
        pass

    @render.register
    def _(self, element: PatternsList):
        pass

    @render.register
    def _(self, element: MinimumCostObjective):
        pass

    @render.register
    def _(self, element: MaximizeIncomeObjective):
        pass

    @render.register
    def _(self, element: MinimizeScrapObjective):
        pass

    @render.register
    def _(self, element: MultiObjectiveList):
        pass

