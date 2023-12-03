from collections import defaultdict

import lxml.html
from selectolax.parser import HTMLParser
from selectolax.lexbor import LexborHTMLParser
from bs4 import BeautifulSoup
from parsel import Selector
from requests_html import HTML

from decorator_and_selectors import timer, item_css_selector, author_css_selector, title_css_selector, \
    date_css_selector, view_counter_css_selector, votes_css_selector, item_class_selector, author_class_selector, \
    title_class_selector, date_class_selector, view_counter_class_selector, votes_class_selector, item_xpath_selector, \
    author_xpath_selector, title_xpath_selector, date_xpath_selector, view_counter_xpath_selector, votes_xpath_selector


@timer
def selectolax_html(html_content: str) -> defaultdict:
    tree = HTMLParser(html_content)
    result = defaultdict(list)
    for node in tree.css(item_css_selector):
        try:
            result['author'].append(node.css_first(author_css_selector).text().strip())
            result['title'].append(node.css_first(title_css_selector).text().strip())
            result['date'].append(' '.join(node.css_first(date_css_selector).text().split()))
            result['view_counter'].append(node.css_first(view_counter_css_selector).text())
            result['votes'].append(node.css_first(votes_css_selector).text())
        except AttributeError:
            continue
    return result


@timer
def selectolax_lexbor(html_content: str) -> defaultdict:
    tree = LexborHTMLParser(html_content)
    result = defaultdict(list)
    for node in tree.css(item_css_selector):
        try:
            result['author'].append(node.css_first(author_css_selector).text().strip())
            result['title'].append(node.css_first(title_css_selector).text().strip())
            result['date'].append(' '.join(node.css_first(date_css_selector).text().split()))
            result['view_counter'].append(node.css_first(view_counter_css_selector).text())
            result['votes'].append(node.css_first(votes_css_selector).text())
        except AttributeError:
            continue
    return result


@timer
def lxml_find_class(html_content: str) -> defaultdict:
    tree = lxml.html.fromstring(html_content)
    result = defaultdict(list)
    for node in tree.find_class(item_class_selector):
        try:
            result['author'].append(node.find_class(author_class_selector)[0].text_content().strip())
            result['title'].append(node.find_class(title_class_selector)[0].text_content().strip())
            result['date'].append(' '.join(node.find_class(date_class_selector)[0].text_content().split()))
            result['view_counter'].append(node.find_class(view_counter_class_selector)[0].text_content())
            result['votes'].append(node.find_class(votes_class_selector)[0].text_content())
        except (AttributeError, IndexError):
            continue
    return result


@timer
def lxml_parser_xpath(html_content: str) -> defaultdict:
    tree = lxml.html.fromstring(html_content)
    result = defaultdict(list)
    for node in tree.xpath(item_xpath_selector):
        try:
            result['author'].append(node.xpath(author_xpath_selector)[0].strip())
            result['title'].append(node.xpath(title_xpath_selector)[0].strip())
            result['date'].append(' '.join(node.xpath(date_xpath_selector)[0].split()))
            result['view_counter'].append(node.xpath(view_counter_xpath_selector)[0])
            result['votes'].append(node.xpath(votes_xpath_selector)[0].text_content())
        except (AttributeError, IndexError):
            continue
    return result


@timer
def bf4_lxml(html_content: str | bytes) -> defaultdict:
    soup = BeautifulSoup(html_content, 'lxml')
    result = defaultdict(list)
    for node in soup.select(item_css_selector):
        try:
            result['author'].append(node.select_one(author_css_selector).text.strip())
            result['title'].append(node.select_one(title_css_selector).text.strip())
            result['date'].append(' '.join(node.select_one(date_css_selector).text.split()))
            result['view_counter'].append(node.select_one(view_counter_css_selector).text)
            result['votes'].append(node.select_one(votes_css_selector).text)
        except AttributeError:
            continue
    return result


@timer
def bf4_html(html_content: str | bytes) -> defaultdict:
    soup = BeautifulSoup(html_content, 'html.parser')
    result = defaultdict(list)
    for node in soup.select(item_css_selector):
        try:
            result['author'].append(node.select_one(author_css_selector).text.strip())
            result['title'].append(node.select_one(title_css_selector).text.strip())
            result['date'].append(' '.join(node.select_one(date_css_selector).text.split()))
            result['view_counter'].append(node.select_one(view_counter_css_selector).text)
            result['votes'].append(node.select_one(votes_css_selector).text)
        except AttributeError:
            continue
    return result


@timer
def parsel_xpath(html_content: bytes) -> defaultdict:
    selector = Selector(html_content.decode("utf-8"))
    result = defaultdict(list)
    for node in selector.xpath(item_xpath_selector):
        try:
            result['author'].append(node.xpath(author_xpath_selector).get().strip())
            result['title'].append(node.xpath(title_xpath_selector).get().strip())
            result['date'].append(' '.join(node.xpath(date_xpath_selector).get().split()))
            result['view_counter'].append(node.xpath(view_counter_xpath_selector).get())
            result['votes'].append(
                '  '.join([i.strip() for i in node.xpath(votes_xpath_selector+"//text()").getall() if i.strip()]))
        except (AttributeError, IndexError):
            continue
    return result


@timer
def requests_html(html_content: str | bytes) -> defaultdict:
    tree = HTML(html=html_content)
    result = defaultdict(list)
    for node in tree.find(item_css_selector):
        try:
            result['author'].append(node.find(author_css_selector, first=True).text.strip())
            result['title'].append(node.find(title_css_selector, first=True).text.strip())
            result['date'].append(' '.join(node.find(date_css_selector, first=True).text.split()))
            result['view_counter'].append(node.find(view_counter_css_selector, first=True).text)
            result['votes'].append(node.find(votes_css_selector, first=True).text.replace('\n', '  '))
        except AttributeError:
            continue
    return result

@timer
def requests_html_xpath(html_content: str | bytes) -> defaultdict:
    tree = HTML(html=html_content)
    result = defaultdict(list)
    for node in tree.find(item_css_selector):
        try:
            result['author'].append(node.xpath(author_xpath_selector, first=True).strip())
            result['title'].append(node.xpath(title_xpath_selector, first=True).strip())
            result['date'].append(' '.join(node.xpath(date_xpath_selector, first=True).split()))
            result['view_counter'].append(node.xpath(view_counter_xpath_selector, first=True))
            result['votes'].append(node.xpath(votes_xpath_selector, first=True).text.replace('\n', '  '))
        except AttributeError:
            continue
    return result