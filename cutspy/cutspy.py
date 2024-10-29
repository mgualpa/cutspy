from cutspy_dom import CSPModel

m = CSPModel()

# t = cutspy_dom.StocksList()

# s1 = cutspy_dom.Stock(name="A", lenght=5.0, cost=6, stock=1000)
# t[s1.name] = s1

# m.add_stock("b", 30.0, 100.0, 20)

# s2 = cutspy_dom.Part("A", 2.0, 3, 50.0)
# m.stocks.append(s2)
# t[s2.name] = s2

m.add_stock(name="A", lenght=5.0, cost=6)
m.add_stock(name="B", lenght=6.0, cost=7)
m.add_stock(name="C", lenght=9.0, cost=10)

m.add_part(name="S", lenght=2, demand=20)
m.add_part(name="M", lenght=3, demand=10)
m.add_part(name="L", lenght=4, demand=20)

p = m.make_patterns()
print(p)
print(len(p))
