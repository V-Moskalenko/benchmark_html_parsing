from parser_and_benchmark import benchmark
from parsing_functions import selectolax_html, selectolax_lexbor, lxml_find_class, lxml_parser_xpath, bf4_lxml, \
    bf4_html, parsel_xpath, requests_html, requests_html_xpath

if __name__ == '__main__':
    # query = 'html%20parsing%20python&target_type=posts&order=date'
    query = 'html&target_type=posts&order=date'
    function_tuple = (selectolax_html, selectolax_lexbor, lxml_find_class, lxml_parser_xpath, bf4_lxml, bf4_html,
                      parsel_xpath, requests_html, requests_html_xpath)
    result = benchmark(50, 50, query, function_tuple)
    print(result)

