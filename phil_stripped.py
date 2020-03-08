#!/usr/bin/env python3
from urllib.request import urlopen
from urllib.parse import quote, unquote
from urllib.error import URLError, HTTPError
import re

PATTERN = re.compile(r'["\']/wiki/([^.#:]*?)["\']')


def get_content(name: str) -> str:
    """
    Функция возвращает содержимое вики-страницы name из русской Википедии.
    В случае ошибки загрузки или отсутствия страницы возвращается None.
    """
    link = 'http://ru.wikipedia.org/wiki/' + quote(name)
    try:
        page = urlopen(link)
    except (URLError, HTTPError):
        return None

    return page.read().decode('utf-8')


def extract_content(page: str) -> tuple:
    """
    Функция принимает на вход содержимое страницы и возвращает 2-элементный
    tuple, первый элемент которого — номер позиции, с которой начинается
    содержимое статьи, второй элемент — номер позиции, на котором заканчивается
    содержимое статьи.
    Если содержимое отсутствует, возвращается (0, 0).
    """
    if page is None:
        return 0, 0

    return page.find(r'<div id="mw-content-text"'), \
           page.find(r'<div id="catlinks"')


def extract_links(page: str, begin: int, end: int) -> list:
    """
    Функция принимает на вход содержимое страницы и начало и конец интервала,
    задающего позицию содержимого статьи на странице и возвращает все имеющиеся
    ссылки на другие вики-страницы без повторений и с учётом регистра.
    """
    if page is None:
        return []
    links = set(re.findall(PATTERN, page[begin:end]))
    links = list(links)
    for index, link in enumerate(links):
        links[index] = unquote(link)

    return links


def replace_yo_ye(name: str) -> str:
    name = list(name)
    for i, letter in enumerate(name):
        if not letter.isalpha() and letter not in '()_:-/,.':
            name[i] = ''
    return str.join('', name)


def find_chain(start: str, finish: str) -> list:
    """
    Функция принимает на вход название начальной и конечной статьи и возвращает
    список переходов, позволяющий добраться из начальной статьи в конечную.
    Первым элементом результата должен быть start, последним — finish.
    Если построить переходы невозможно, возвращается None.
    """
    path = [start]
    current_name = replace_yo_ye(start)
    while True:
        path.append(current_name)
        if current_name == finish:
            break
        page = get_content(current_name)
        if not page:
            return None
        links = extract_links(page, *extract_content(page))
        if finish in links:
            path.append(finish)
            break
        for link in links:
            if link in path:
                continue
            current_name = link
            break

    return path


def main():
    pass


if __name__ == '__main__':
    main()
