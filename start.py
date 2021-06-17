import re
import json
import inquirer

# Переменные
city_tmp = []
city = []
pizzeria_adrress = []

# Откр pizza.json и salary.json
f1 = open('data/salary.json', encoding="utf8")
f2 = open('data/pizza.json', encoding="utf8")
salary_data = json.load(f1)
pizza_data = json.load(f2)

# Получаем список городов и загоняем в лист city
for x in range(0, 585):
    city_tmp.append(pizza_data[x]["AddressDetails"]["LocalityName"])
    for i in city_tmp:
        if i not in city:
            city.append(i)
city.sort()

# МСК и СПб ставим на первые места в списке
city[144], city[0] = city[0], city[144]
city[207], city[1] = city[1], city[207]

# Интерактивный ввод города
print("\n\n\n\n\nДобро пожаловать!")
questions = [inquirer.List('ans', message="Выберите город", choices=city)]
answers = inquirer.prompt(questions) # И ждем ввод

# заполняем адрес пиццерий в массив
for x in range(0, 585):
    if pizza_data[x]["AddressDetails"]["LocalityName"] == answers["ans"]:
        pizzeria_adrress.append(pizza_data[x]["Address"])

# интерактивный ввод пиццерии
questions = [inquirer.List('ans', message="Выберите пиццерию", choices=pizzeria_adrress)]
answers = inquirer.prompt(questions)

# функция parse
def parse(num):
    print("Выручка с [" + salary_data[num]["period"]["start"] + "] по [" + salary_data[num]["period"]["end"] + "]\n")
    # вывод информации о доходе пиццерии
    # TODO: better vision (colorize, etc.)
    for history in range(len(salary_data[num]["history"])):
        print("[" + str(salary_data[num]["history"][history]["month"]) + "/" + str(salary_data[num]["history"][history]["year"]) + "]")
        print("Ресторан:  " + str(salary_data[num]["history"][history]["local"]["stationaryRevenue"]) + " руб. (" + str(salary_data[num]["history"][history]["usd"]["stationaryRevenue"]) + "$)")
        print("Доставка:  " + str(salary_data[num]["history"][history]["local"]["deliveryRevenue"]) + " руб. (" + str(salary_data[num]["history"][history]["usd"]["deliveryRevenue"]) + "$)")
        print("Самовывоз: " + str(salary_data[num]["history"][history]["local"]["pickupRevenue"]) + " руб. (" + str(salary_data[num]["history"][history]["usd"]["pickupRevenue"]) + "$)")
        print("Итог:      " + str(salary_data[num]["history"][history]["local"]["revenue"]) + " руб. (" + str(salary_data[num]["history"][history]["usd"]["revenue"]) + "$)\n")
    input("Нажмите любую клавишу чтобы закрыть программу.")
    
# функция salary
def salary(uid):
    # цикл для поиска, сравнения и определения id пиццерии между файлами из data/
    for num in range(len(salary_data)):
        for y in range(len(pizza_data)):
            if (salary_data[num]["unitId"] == uid) and (pizza_data[y]["Id"] == uid):
                ask = input("Показать инфорацию о выручке? (Y/n)\n")
                if (ask == "Y") or (ask == "y"):
                    # выполение функции с ранее определённым значением 'id' выбранной пиццерии
                    return parse(num)
                    
                else:
                    # в случае отказа
                    input("Нажмите любую клавишу чтобы закрыть программу.")
                    return


# вывод информации о выбранной  пиццерии
for x in range(0, 585):
    if pizza_data[x]["Address"] == answers["ans"]:
        print("Выбранный адрес: " + pizza_data[x]["Address"])
        print("Заказы в прямом эфире: https://orderstatusboard.dodois.io/boards?PizzeriaId=" + pizza_data[x]["UUId"])
        
        # попытка найти камеру
        try:
            p1 = re.search(r'(?<=open.ivideon.com/embed/v2/\?server\=).*?(?=amp)', pizza_data[x]["WebCameraUrl"])[0]
            p2 = re.findall(r'camera=\d{,}', pizza_data[x]["WebCameraUrl"])[0]
            print("Камера на кухне: https://open.ivideon.com/embed/v2/?server=" + p1 + p2)
        except:
            pass
        # вывод информации о менеджере
        print("Менеджер: {} ({})".format(str(pizza_data[x]["ManagerPhoneNumber"]), pizza_data[x]["StoreManager"]))
        # выполение функции с аргументом 'id' выбранной пиццерии
        salary(pizza_data[x]["Id"])