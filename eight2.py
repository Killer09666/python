n = int(input("Enter your marks: "))

if n < 33:
    print("Grade: F")
elif 33 <= n <= 39:
    print("Grade: D")
elif 40 <= n <= 49:
    print("Grade: C")
elif 50 <= n <= 59:
    print("Grade: B")
elif 60 <= n <= 69:
    print("Grade: A-")
elif 70 <= n <= 79:
    print("Grade: A")
elif 80 <= n <= 100:
    print("Grade: A+")
else:
    print("Invalid input!")

