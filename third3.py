amount = int(input("Enter the amount: "))

note1000 = amount // 1000
print("1000 TAKA note:",note1000)
amount = amount % 1000

note500 = amount // 500
print("500 TAKA note:",note500)
amount = amount % 500

note200 = amount // 200
print("200 TAKA note:",note200)
amounr = amount % 200