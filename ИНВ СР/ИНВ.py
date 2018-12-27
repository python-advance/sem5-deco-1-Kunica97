def logger(f):
    import functools
    @functools.wraps(f)
    def wrapper(*args):
        result = f(*args)
        with open("./log.txt", "a") as file:
            file.write(("-" * 20) + "\n")
            file.write("Rubles: " + str(args[0]) + "\n")
            file.write("Currency: " + str(args[2]) + "\n")
            file.write("Result: " + str(result) + "\n")
        return result

    return wrapper


def get_currencies():
    import urllib.request
    from xml.etree import ElementTree as ET

    response = ET.parse(urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp"))
    currencies = {}
    for line in response.findall('Valute'):
        currencies.update({line.find('CharCode').text: line.find('Value').text})
    return currencies


def get_currency_value(currencies: dict, currency_char):
    return float(currencies[currency_char].replace(",", "."))


@logger
def rubles_to_currency(rubles, currencies, currency_char):
    return rubles / get_currency_value(currencies, currency_char)


def display_currencies(currencies):
    currency_chars = sorted(list(currencies.keys()))
    print("+" + ("-" * 10) + "+")
    for (i, j) in enumerate(currency_chars):
        print("|" + str(i + 1), str(j) + "|", sep="\t|\t")
        print("+" + ("-" * 10) + "+")


def get_currency_chars(currencies):
    return sorted(list(currencies.keys()))


if __name__ == "__main__":

    print("Выполняется запрос на сервер ЦБР...")

    try:
        currencies = get_currencies()
    except URLError:
        print("Ошибка выполнения запроса")
        exit(1)
    else:
        print("Запрос выполнен успешно")

    while True:
        try:
            print("1. Показать доступные валюты")
            print("2. Осуществить конвертацию")
            print("3. Выход")

            operation = int(input("Ввод: "))
            if operation == 1:
                display_currencies(currencies)
            elif operation == 2:
                currency_chars = get_currency_chars(currencies)
                currency_char = currency_chars[abs(int(input("Введите индекс валюты из списка доступных валют: "))) - 1]
                rubles = float(input("Введите колличество рублей: "))
                print("Согласно текущему курсу " + str(rubles), "RUB =", rubles_to_currency(rubles, currencies, currency_char), currency_char)
            elif operation == 3:
                exit()
            else:
                print("Ошибка ввода, повторите попытку")
                continue
        except (ValueError, TypeError) as e:
            print("Ошибка ввода, повторите попытку")
            continue