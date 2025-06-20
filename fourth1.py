buy = float(input("Enter buying price: "))
sell = float(input("Enter selling price:"))

if sell > buy:
    profit = sell - buy
    print("You made a profit of Taka:", profit)
else:
    lose = buy - sell
    print("You made a loss of Taka:", lose)