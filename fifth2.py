w = float(input("Enter your weight in KG: "))
h = float(input("Enter your hight in meter: "))

bmi = w / h ** 2

print("Your BMI is:",round(bmi,2))

if bmi < 18.5:
    print("You are underweight. Please gain some weight. ")
elif 18.5 <= bmi <= 24.4:
    print("You are normal in weight. Keep it up!")
elif 25 <= bmi <= 29.9:
    print("You are overweight. Please loose some weight.")
elif 30 <= bmi <= 34.9:
    print("You are obese. Loosing weight is emergency.")
else:
    print("You are extremly obese. Please visit the doctor as soon as possible.")