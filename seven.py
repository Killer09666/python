amount = int(input("Enter the amount: "))

note1000 = amount // 1000
print("1000 TAKA note:", note1000)
amount = amount % 1000

note500 = amount // 500
print("500 TAKA note:", note500)
amount = amount % 500

note200 = amount // 200
print("200 TAKA note:", note200)
amount = amount % 200

note100 = amount // 100
print("100 TAKA note:", note100)
amount = amount % 100

note50 = amount // 50
print("50 TAKA note:", note50)

note20 = amount // 20
print("20 TAKA note:", note20)
amount = amount % 20

note10 = amount // 10
print("10 TAKA note:", note10)
amount = amount % 10

note5 = amount // 5
print("5 TAKA note:", note5)
amount = amount % 5

note2 = amount // 2
print("2 TAKA note:", note2)
amount = amount % 2

note1 = amount // 1
print("1 TAKA note:", note1)
amount = amount % 1
