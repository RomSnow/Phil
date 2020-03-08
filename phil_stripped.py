#!/usr/bin/env python3
from urllib.request import urlopen
from urllib.parse import quote, unquote
from urllib.error import URLError, HTTPError
import re

CONTENT_BEGIN_PATTERN = re.compile('<p><b>')
CONTENT_END_PATTERN = re.compile(r'</body>')
PATTERN = re.compile(r'["\']/wiki/([^.#:]*?)["\']')


def get_content(name: str) -> str:
    """
    Функция возвращает содержимое вики-страницы name из русской Википедии.
    В случае ошибки загрузки или отсутствия страницы возвращается None.
    """
    try:
        with urlopen('http://ru.wikipedia.org/wiki/' + quote(name)) as link:
            page = link.read().decode('utf-8')
    except (URLError, HTTPError):
        return None

    return page


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

    begin = re.search(CONTENT_BEGIN_PATTERN, page).end()
    end = re.search(CONTENT_END_PATTERN, page).start()
    return begin, end


def extract_links(page: str, begin: int, end: int) -> list:
    """
    Функция принимает на вход содержимое страницы и начало и конец интервала,
    задающего позицию содержимого статьи на странице и возвращает все имеющиеся
    ссылки на другие вики-страницы без повторений и с учётом регистра.
    """
    if page is None:
        return []
    links = []
    for link in re.findall(PATTERN, page[begin:end]):
        if link not in links:
            links.append(unquote(link))

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
