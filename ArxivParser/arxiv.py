import requests
import re 
import os 
import math
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import urllib3
import wget
import PyPDF2
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 
import arxiv
from datetime import datetime, timezone

class Arxiv:
    _articles_per_page = 200

    months = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }
    
    @classmethod
    def make_parse(cls, from_date: datetime, to_date: datetime, key_words: list) -> dict:
        key_words_and_count = {}
        titles_with_links = {}

        for key_word in key_words:
            print(key_word)
            query = f"all:{key_word.replace(' ', ' AND all:')}"
            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=None,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            results = []
            for result in client.results(search):
                if from_date <= result.published:
                    if result.published <= to_date:
                        results.append(result)
                else:
                    break
            print(len(results))
            titles = [result.title for result in results]
            links = [result.links[1].href for result in results]
            dates = [result.published for result in results]

            for title, link, date in zip(titles, links, dates):
                if title not in titles_with_links:
                    titles_with_links[title] = link
            key_words_and_count[key_word] = len(titles)

        print(len(titles_with_links))
        return titles_with_links, key_words_and_count

    @classmethod
    def make_parse_2periods_and_draw_graph(cls, past_from_date: str, past_to_date: str, now_from_date: str, now_to_date: str, key_words: list) -> plt:
        print("Was unique: ")
        data_was = cls.make_parse(past_from_date, past_to_date, key_words)[1]
        print("Became unique: ")
        data_became = cls.make_parse(now_from_date, now_to_date, key_words)[1]
        merged_data = {}

        for key, value in data_was.items():
            merged_data.setdefault(key, []).append(value)

        for key, value in data_became.items():
            merged_data.setdefault(key, []).append(value)

        categories = list(data_was.keys())
        values_was = list(map(int, [i[0] for i in merged_data.values()]))
        values_became = list(map(int, [i[1] for i in merged_data.values()]))
        index = list(range(len(categories)))
        bar_height = 0.35

        with plt.style.context('dark_background'):
            plt.bar(index, values_was, width=bar_height, color='orange', label='Было')
            plt.bar(index + bar_height, values_became, width=bar_height, color='green', label='Стало')
            plt.ylabel('Количество')
            plt.xlabel('Категории')
            plt.title('Сравнение "было" и "стало"')
            plt.xticks(index + bar_height/2, categories, rotation=70)
            for i, v in enumerate(values_was):
                plt.text(i, v + 0.5, str(v), ha='center', va='bottom')
            for i, v in enumerate(values_became):
                plt.text(i+bar_height, v + 0.5, str(v), ha='center', va='bottom')
            plt.legend()

        for values in [values_was, values_became]:
            for category, value in sorted(zip(categories, values), key=lambda x: x[1], reverse=True):
                print(category, value)
            print()
        print("Was all:\n", sum(values_was))
        print("Became all:\n", sum(values_became))
        return plt.show()

    @classmethod            
    def get_links(cls, now_from_date: str, now_to_date: str, key_words: list) -> list:
        return [i for i in cls.make_parse(now_from_date, now_to_date, key_words)[0].values()]
    
    @classmethod            
    def get_titles_and_links(cls, now_from_date: str, now_to_date: str, key_words: list) -> list:
        return [(title, link) for title, link in cls.make_parse(now_from_date, now_to_date, key_words)[0].items()]
    
    @classmethod 
    def save_pdfs_and_get_pages(cls, now_from_date: str, now_to_date: str, path_to_save: str, key_words: list) -> list:
        titles_links = cls.get_titles_and_links(now_from_date, now_to_date, key_words)
        not_downloaded = []

        titles = []
        links = []
        for title, url in titles_links:
            titles.append(title)
            links.append(url)
            try:
                wget.download(url + '.pdf', path_to_save + os.sep + title + ".pdf")
            except:
                print(f'{url}.pdf is not downloaded')
                not_downloaded.append(url + '.pdf')
                pass

        return not_downloaded, titles, links
    
    @classmethod
    def count_pages(cls, path_to_files: str) -> int:
        files = os.listdir(path_to_files)
        page_count = 0
        for file in files:
            file = open(path_to_files + '/' + file, 'rb') 
            pdfReader = PyPDF2.PdfReader(file) 
            page_count += len(pdfReader.pages)

        return page_count

