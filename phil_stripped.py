#!/usr/bin/env python3
from urllib.request import urlopen
from urllib.parse import quote
import re


def get_content(name: str) -> str:
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
        print(name)
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
    return page.find('<div id="mw-content-text">'), page.find('</body')


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


def find_path(start_link: str, finish_link: str, path: list, counter: int):
    if counter > 3:
        return
    print(counter)
    print(start_link)
    path.append(start_link)
    if finish_link in start_link:
        print('DONE')
        return path
    page = get_content(start_link)
    if page is None:
        return
    links = extract_links(page, *extract_content(page))
    counter += 1
    for i in links:
        if i in path:
            continue
        find_path(i, finish_link, path, counter)
        


def find_chain(start: str, finish: str) -> list:
    """
    Функция принимает на вход название начальной и конечной статьи и возвращает
    список переходов, позволяющий добраться из начальной статьи в конечную.
    Первым элементом результата должен быть start, последним — finish.
    Если построить переходы невозможно, возвращается None.
    """
    pass


def main():
    page = get_content('Аристотель')
    begin, end = extract_content(page)
    links = extract_links(page, begin, end)
    print(len(links))
    start_link = 'http://ru.wikipedia.org/wiki/' + quote('Аристотель')
    finish_link = 'http://ru.wikipedia.org/wiki/' + quote('Философия')

   # print(find_path(start_link, finish_link, [], 0))


if __name__ == '__main__':
    main()
