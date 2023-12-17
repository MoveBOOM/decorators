import os
from decorator import logger, logger_2


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_2(path)
        def hello_world():
            return 'Hello World'

        @logger_2(path)
        def summator(a, b=0):
            return a + b

        @logger_2(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


file_path = 'recipes.txt'


@logger
def read_cook_book_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        menu = {}
        for line in file:
            dish_name = line[:-1]
            dish_count = file.readline().strip()
            ingridients_list = []
            for i in range(int(dish_count)):
                dish_items = dict.fromkeys(['ingredient_name', 'quantity', 'measure'])
                ingridient_name = file.readline().strip().split(' | ')
                for item in ingridient_name:
                    dish_items['ingredient_name'] = ingridient_name[0]
                    dish_items['quantity'] = ingridient_name[1]
                    dish_items['measure'] = ingridient_name[2]
                ingridients_list.append(dish_items)
                cook_book = {dish_name: ingridients_list}
                menu.update(cook_book)
            file.readline()
    return menu


if __name__ == '__main__':
    test_1()
    test_2()
    read_cook_book_in_file(file_path)
