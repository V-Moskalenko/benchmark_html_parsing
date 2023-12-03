import statistics
from collections import defaultdict

import requests


class MyProjectError(Exception):
    pass


def parser(amount_pages: int, query: str, func_list: list | tuple, check_result=False) -> tuple[dict, defaultdict]:
    """
    Функция парсинга

    :param amount_pages: количество страниц, которые необходимо спарсить
    :param query: url- фильтр/запрос
    :param func_list: список функций, которыми будем парсить
    :return: словарь {имя функции парсинга: суммированное время парсинга указанных страниц}, defaultdict - результат
    парсинга
    """
    time_dict = defaultdict(list)  # Словарь, ключ: имя функции-парсера, значение: список времени обработки страниц
    parsing_result = defaultdict(list)  # Результат парсинга страниц
    benchmark_dict = {}
    for number in range(1, amount_pages + 1):
        print(f'\tСтраница: {number}')
        r = requests.get(fr'https://habr.com/ru/search/page{number}/?q={query}')
        # Получили страницу
        if r.status_code == 200:
            html_content = r.content
        else:
            raise MyProjectError(f'Ошибка запроса, статус код: {r.status_code}')

        temp_check_result = []
        for method in func_list:
            # Каждым методом получаем его результат, время выполнения и имя самого метода
            result, timer, name = method(html_content)
            time_dict.setdefault(name, []).append(timer)
            temp_check_result.append(result)

        # Проверим что результаты всех методов одинаковы
        if check_result:
            if all([i == temp_check_result[0] for i in temp_check_result]):
                # Если совпадают, добавим один из результатов в итоговый вывод парсинга
                for key, value in temp_check_result[0].items():
                    parsing_result.setdefault(key, []).extend(value)
            else:
                raise MyProjectError(
                    f"Результаты парсинга методов/функций, не совпадают: {[i == temp_check_result[0] for i in temp_check_result]}")
        else:
            for key, value in temp_check_result[0].items():
                parsing_result.setdefault(key, []).extend(value)

        # Просуммируем результаты времени обработки
        benchmark_dict = {key: sum(value) for key, value in time_dict.items()}
    return benchmark_dict, parsing_result


def benchmark(rounds: int, amount_pages: int, query: str, func_list: list | tuple) -> defaultdict:
    """
    Функция запуска бенчмарка

    :param rounds: количество раундов (прогонов) парсинга
    :param amount_pages: количество страниц, которые необходимо спарсить
    :param query: url- фильтр/запрос
    :param func_list: список функций, которыми будем парсить
    :return: defaultdict {имя функции парсинга: список время парсинга указанных страниц по раундам}
    """
    benchmark_dict = defaultdict(list)
    for i in range(rounds):
        print(f'Раунд: {i}')
        time_dict, _ = parser(amount_pages, query, func_list)
        for key, value in time_dict.items():
            benchmark_dict.setdefault(key, []).append(value)

    for key, value in sorted(benchmark_dict.items(), key=lambda x: statistics.mean(x[1])):
        print(f'Среднее время отработки функции {key}: {statistics.mean(value)}, медиана: {statistics.median(value)}')
    return benchmark_dict
