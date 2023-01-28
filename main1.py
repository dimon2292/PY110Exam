import random
import json
import re
from faker import Faker
from conf import MODEL
from regular_expression import REGEX


fake = Faker()


def max_len_title() -> int:
    """
    вычисляет максимальную длину книги для декоратора fabric_decoration
    :return: натуральное число
    """
    with open("books.txt", 'r', encoding='utf8') as f:
        list_ = f.readlines()
        return len(max(list_, key= len))


def fabric_decoration(fn):
    """
    фабрика декоратора чтобы принимать максимальную длину книги как параметр для декоратора
    :param fn: функция max_len_title
    :return:
    """
    max_len = fn()                                           # максимальная длина книги
    def validation_length_of_title(func):
        """
        декоратор, проверяющий чтобы не была превышена максимальную длину книги .
        :param func: функция get_title
        :return:
        """
        def wrapper(*args, **kwargs):
            result = func()
            if len(result) > max_len:
                raise ValueError("Превышена макcимальная длина заглавия")
            return result
        return wrapper
    return validation_length_of_title


@fabric_decoration(max_len_title)
def get_title() -> str:
    """
    название книги
    :return: случайная строка из файла books.txt
    """
    with open('books.txt', 'r', encoding='utf8') as f:
        titles = f.readlines()
        return str.strip(random.choice(titles))


def get_year() -> int:
    """
    год выпуска книги
    :return: случайное натуральное число
    """
    year = random.randint(1600, 2022)
    return year


def get_pages() -> int:
    """
    количество страниц в книге
    :return: случайное натуральное число
    """
    pages = random.randint(100, 500)
    return pages

def validate_isbn13(func):
    """
    декоратор, проверяющий правильность структуры значения ISBN13, генерируемого модулем Faker
    :param func: функция генерирующая isbn13
    :return: соотвествие регулярному выражению
    """
    def wrapper(*args, **kwargs):
        result = func()
        if re.fullmatch(REGEX, result):
            return result
        else:
            raise ValueError('ISBN неверный')
    return wrapper


@validate_isbn13
def get_isbn() -> str:
    """
    международный стандартный книжный номер
    :return: строковое значение, сгенерированное модулем faker
    """
    isbn = fake.isbn13()
    return isbn


def get_rating() -> float:
    """
    рейтинг книги
    :return: число с плавающей запятой в диапазоне от 0 до 5 обе границы
включительно, округлённое до трёх знаков после запятой
    """
    rating = round(random.uniform(0, 5.0), 3)
    return rating


def get_price() -> float:
    """
    цена книги
    :return: число с плавающей запятой, округлённое до двух знаков после запятой
    """
    price = round(random.uniform(100.0, 1500.0), 2)
    return price


def get_author() -> list:
    """
    имена и фамилии авторов (от 1 до 3) сгенерированные модулем Faker
    :return: список содержащий строковые значения имен авторов
    """
    author_list = []
    number_of_author = random.randint(1, 3)
    for i in range(number_of_author):
        author_list.append(fake.name())
    return author_list


def get_fields() -> dict:
    """
    полное описание характеристик книги
    :return: словарь
    """
    dict_ = {
        'title': get_title(),
        'year': get_year(),
        'pages': get_pages(),
        'isbn13': get_isbn(),
        'rating': get_rating(),
        'price': get_price(),
        'author': get_author()
    }

    return dict_


def get_book(pk =1) -> dict:
    """
    генератор книг, плюс счётчик количества генераций (по умолчанию равен 1)
    :param pk:  счётчик, который увеличивается на единицу при генерации нового объекта
    :return: словарь
    """
    increment = pk
    while True:
        dict_ = {
            'model': MODEL,
            'pk': increment,
            'fields': get_fields()
        }
        yield dict_
        increment += 1


def get_json(data) -> json:
    """
    записывает данные в файл json
    :param data: список словарей (100 книг)
    :return: итоговый файл в формате json
    """
    with open('books.json', 'w', encoding= 'utf8')as f:
        json.dump(data, f, indent= 4, ensure_ascii= False)


def main():
    """
    1. запускает функцию-генератор книг, формирует список из 100 книг
    2. сериализует этот список в файл формата json
    :return:
    """
    generator = get_book()
    data = [next(generator) for i in range(100)]
    get_json(data)


if __name__ == "__main__":
    main()












































