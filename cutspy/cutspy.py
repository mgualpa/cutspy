from cutspy_dom import CSPModel
import cutspy_dom

m = CSPModel()

t = cutspy_dom.TypedDict[cutspy_dom.Stock]()
t = cutspy_dom.StocksList()

s1 = cutspy_dom.Stock("A", 10.0, 100.0, 3)
t[s1.id] = s1

m.add_stock("b", 30.0, 100.0, 20)

s2 = cutspy_dom.Part("A", 2.0, 3, 50.0)
m.stocks.append(s2)
#t[s2.id] = s2


