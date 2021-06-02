import re
import json
import inquirer

# Переменные
city_tmp = []
city = []
pizzeria_adrress = []

# Откр pizza.json
f = open('pizza.json', encoding="utf8")
data = json.load(f)

# Получаем список городов и загоняем в лист city
for x in range(0, 584):
    city_tmp.append(data[x]["AddressDetails"]["LocalityName"])
    for i in city_tmp:
        if i not in city:
            city.append(i)
city.sort()

# МСК и СПб ставим на первые места в списке
city[143], city[0] = city[0], city[143]
city[207], city[1] = city[1], city[207]

# Интерактивный ввод города
print("\n\n\n\n\nДобро пожаловать!")
questions = [inquirer.List('ans', message="Выберите город", choices=city)]
answers = inquirer.prompt(questions) # И ждем ввод

# заполняем адрес пиццерий в массив
for x in range(0, 584):
    if data[x]["AddressDetails"]["LocalityName"] == answers["ans"]:
        pizzeria_adrress.append(data[x]["Address"])

# интерактивный ввод пиццерии
questions = [inquirer.List('ans', message="Выберите пиццерию", choices=pizzeria_adrress)]
answers = inquirer.prompt(questions)

# вывод информации о выбранной  пиццерии
for x in range(0, 584):
    if data[x]["Address"] == answers["ans"]:
        print("Выбранный адрес: " + data[x]["Address"])
        print("Заказы в прямом эфире: https://orderstatusboard.dodois.io/boards?PizzeriaId=" + data[x]["UUId"])
        
        # Попытка найти камеру
        try:
            p1 = re.search(r'(?<=open.ivideon.com/embed/v2/\?server\=).*?(?=amp)', data[x]["WebCameraUrl"])[0]
            p2 = re.findall(r'camera=\d{,}', data[x]["WebCameraUrl"])[0]
            print("Камера на кухне: https://open.ivideon.com/embed/v2/?server=" + p1 + p2)
        except:
            pass
            
        print("Менеджер: {} ({})".format(str(data[x]["ManagerPhoneNumber"]), data[x]["StoreManager"]))