import io
from abc import ABC
from dataclasses import dataclass, field
from functools import singledispatchmethod

from cutspy_dom import (AbstractMultiObjectiveList, AbstractObjective,
                        AbstractRender, CSPModel, Cut, MaximizeIncomeObjective,
                        MinimizeScrapObjective, MinimumCostObjective,
                        MultiObjectiveList, Part, PartsList, PatternsList,
                        RenderableElement, Stock, StocksList, TypedDict)


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
