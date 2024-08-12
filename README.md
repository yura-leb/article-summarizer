# article-summarizer

Это инструмент для обработки arxiv, суммаризации статей и генерации таблиц, представленный на Offzone 2024. 
Он включает:
* ArxivParser: инструмент для выгрузки статей из arxiv за период по ключевым словам
* Summarizer: инструмент для суммаризации статей и генерации таблиц

## Установка

`git clone https://github.com/yura-leb/article-summarizer.git`
`cd article-summarizer`
`pip install -r requirements.txt`

## ArxivParser

* В файле keywords.csv находятся ключевые слова, по которым происходит поиск статей в arxiv. Поменяйте их на свои, если требуется.
* arxiv.py содержит класс для выгрузки статей из arxiv
* arx.py содержит вызов функции для загрузки статей

Получение статей за период:
`python3 ArxivParser/arx.py <start_date> <end_date> <directory to save pdfs>`

Например:
`python3 ArxivParser/arx.py 2024-06-01 2024-06-02 june`

## Summarizer

* PromptsContainer содержит промпты для генерации саммари и полей таблицы. Класс отвечает за обращение к LLM (GigaChat). Для работы с ним понадобится api-ключ, который можно получить на https://developers.sber.ru/portal/products/gigachat-api. Далее требуется создать файл .env (наподобие .env.template), в который требуется добавить ключ и scope.
* generate_conclusions генерирует саммари длиной в 1 предложение для всех статей в директории.
`python3 Summarizer/generate_conclusions.py <директория с pdf> <json файл вывода>`
Пример:
`python3 Summarizer/generate_conclusions.py june concl.txt`
* generate_tables генерирует таблицы для статей, добавленных в файл data/<название директории в формате Month_Year>/nlp.bib с помощью [JabRef](https://www.jabref.org). Таблицы генерируются для статей, которые опубликованы в месяц и год, совпадающий с названием директории, для которых стоят оценки и приоритет. На выходе создается json файл с таблицами для каждой статьи.
`python3 Summarizer/generate_tables.py <директория формата Month_Year> <json файл вывода>`
Пример:
`python3 Summarizer/generate_tables.py June2024 output.json`





PS: спасибо Антону Переходову за написание основной части ArxivParser