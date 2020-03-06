#!/usr/bin/env python3
from urllib.request import urlopen
from urllib.parse import quote
import re


def get_content(name: str):
    """
    Функция возвращает содержимое вики-страницы name из русской Википедии.
    В случае ошибки загрузки или отсутствия страницы возвращается None.
    """
    if name.startswith('http'):
        link = name
    else:
        link = 'http://ru.wikipedia.org/wiki/' + quote(name)

    try:
        page = urlopen(link)
    except Exception:
        return None

    return page.read().decode('utf=8')


def extract_content(page: str) -> tuple:
    """
    Функция принимает на вход содержимое страницы и возвращает 2-элементный
    tuple, первый элемент которого — номер позиции, с которой начинается
    содержимое статьи, второй элемент — номер позиции, на котором заканчивается
    содержимое статьи.
    Если содержимое отсутствует, возвращается (0, 0).
    """
    return page.find('<body'), page.find('</body')


def extract_links(page: str, begin: int, end: int) -> list:
    """
    Функция принимает на вход содержимое страницы и начало и конец интервала,
    задающего позицию содержимого статьи на странице и возвращает все имеющиеся
    ссылки на другие вики-страницы без повторений и с учётом регистра.
    """
    links = re.findall(r'"(/wiki/.*?)"', page)
    for i in enumerate(links):
        if i[1].startswith('http'):
            continue
        links[i[0]] = 'http://ru.wikipedia.org' + links[i[0]]

    return links


def get_page_title(page: str) -> str:
    """Возращает значение поля title html страницы"""
    return str(*re.findall(r"<title>(.*)</title>", page))


# def find_path(start_link: str, finish_link: str, path: list):
#     path.append(start_link)
#     if start_link == finish_link:
#         return path
#     get_content(start_link)
#     links = extract_links(page, *extract_content(page))
#     for i in links:


def find_chain(start: str, finish: str) -> list:
    """
    Функция принимает на вход название начальной и конечной статьи и возвращает
    список переходов, позволяющий добраться из начальной статьи в конечную.
    Первым элементом результата должен быть start, последним — finish.
    Если построить переходы невозможно, возвращается None.
    """
    pass


def main():
    page = get_content('AWK')
    begin, end = extract_content(page)
    links = extract_links(page, begin, end)
    print(links)


if __name__ == '__main__':
    main()
