n = float(input("Enter first number: "))
n1 = float(input("Enter second number: "))
n2 = float(input("Enter third number: "))

if n >= n1 and n >= n2:
    print("The biggest number is:",n)
elif n1 >= n and n1 >= n2:
    print("The biggest number is:",n1)
else:
    print("The biggest number is:",n2)

    