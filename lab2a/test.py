import math
from math import *
from random import randint
# 2.1 Виводжу вбудованні константи за допомогою команд:
print("True: ", True)
print("False: ", False)
print("Pi: ",pi)
# 2.2 Виводжу результат роботи вбудованих функцій за допомогою команд:
print("Заокруглення у вищу сторону",ceil(11.1))
print("Число 13 в 16-ві системі числення:", hex(13))
print("2 в 5 степені =", pow(2,5))
print("Максимальне число:",max(1,2,3,4,5))

# 2.3 Виводжу результат роботи циклу і розгалужень за допомогою команд:
statement1 = False
statement2 = True
if statement1 is True:
    print("statement1 is True")
    pass
elif statement2 is True:
    print("statement2 is True")
    pass
else:
    print("statements isn't True")
    pass
# 2.4 Виводжу результат роботи конструкції `try`->`except`->`finally` за допомогою команд:
A = 0
try:
    s = input("Введіть шось")
    s = s + 5
except Exception as e:
    print(e)
finally:
    print("Помилка")
# 2.5 Виводжу результат роботи контекст-менеджера `with` за допомогою команд:    
i=1
with open("README.md", "r") as file:
    for line in file:
        print("Рядок " + str(i) + ": " + line)
        i=i+1

# 2.6 Виводжу результат роботи з `lambdas` за допомогою команд:
Point = lambda x,y:(f'Точка:{x},{y}')
print(Point(1,5))
