import time

# Селекторы
item_css_selector = ".tm-articles-list__item"  # Селектор публикации
author_css_selector = ".tm-user-info__username"  # Селектор автора
title_css_selector = "h2[class='tm-title tm-title_h2']"  # Селектор заголовка
date_css_selector = "span[class='tm-article-datetime-published']"  # Селектор даты
view_counter_css_selector = "span[class='tm-icon-counter__value']"  # Селектор количества просмотров
votes_css_selector = "div[class='tm-votes-meter tm-data-icons__item']"  # Селектор голосов

item_class_selector = "tm-articles-list__item"
author_class_selector = "tm-user-info__username"
title_class_selector = "tm-title tm-title_h2"
date_class_selector = "tm-article-datetime-published"
view_counter_class_selector = "tm-icon-counter__value"
votes_class_selector = "tm-votes-meter tm-data-icons__item"

item_xpath_selector = "//article[@class='tm-articles-list__item']"
author_xpath_selector = "descendant::a[@class='tm-user-info__username']/text()"
title_xpath_selector = "descendant::h2[@class='tm-title tm-title_h2']//text()"
date_xpath_selector = "descendant::span[@class='tm-article-datetime-published']//text()"
view_counter_xpath_selector = "descendant::span[@class='tm-icon-counter__value']/text()"
votes_xpath_selector = "descendant::div[@class='tm-votes-meter tm-data-icons__item']"


def timer(func):
    def wrapper(*args, **kwargs):
        time_start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_time = time.perf_counter() - time_start
        return result, elapsed_time, func.__name__

    return wrapper
