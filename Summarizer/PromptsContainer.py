import os
import csv
import logging
from langchain_community.document_loaders import PyPDFLoader
from collections import OrderedDict
import dotenv

from langchain_community.chat_models.gigachat import GigaChat

class PromptsContainer:
    prompts = OrderedDict({
        "micro_conclusions": "Please provide a summary in 1 sentence of the main findings and their significance from the article. Answer without introductory text.",
        "conclusions": "Please provide a 50-word summary of the main findings and their significance from the article. Answer without introductory text.",
        "OWASP": "What is main type of attack described in the article according to OWASP Top 10 for LLM Applications which contain of OWASP top 10 for LLM: LLM01: Prompt Injection, LLM02: Insecure Output Handling, LLM03: Training Data Poisoning, LLM04: Model Denial of Service, LLM05: Supply Chain Vulnerabilities, LLM06: Sensitive Information Disclosure, LLM07: Insecure Plugin Design, LLM08: Excessive Agency, LLM09: Overreliance, LLM10: Model Theft? Answer formatted 'LLM__: _______' without introductory text.",
        "applicability": "Review the content of an article. If the article describes an attack method, determine whether this method can be applied to a black-box model and how. If the article is a survey or discusses a defense method, respond with 'NO'. Limit 10 words.",
        "summary": 'Summarize the article in about 150 words, highlighting the main points, arguments, and conclusions. Avoid personal opinions and unnecessary details.',
        "top": "Summarize the article in about 500 words by identifying and explaining the top key points. Present each point in a distinct paragraph.",
        "datasets_models": "Based on the information provided in the article, please list all the datasets and language models that are mentioned. Don't use json. Organize your response in the format below:\nDatasets: List each dataset name separated by commas.\nModels: List each model name separated by commas.",
    })

    translation_prompt = """
    The article introduces AutoDAN, an interpretable, gradient-based adversarial attack that can compromise the safety alignment of Large Language Models (LLMs). 
    Статья представляет AutoDAN, интерпретируемую, основанную на градиентах, состязательную атаку, которая может нарушить safety alignment больших языковых моделей (LLM).

    AutoDAN merges the strengths of manual jailbreak attacks and automatic adversarial attacks, generating readable prompts that bypass perplexity filters while maintaining high attack success rates. 
    AutoDAN объединяет сильные стороны ручных джейлбрейк атак и автоматических состязательных атак, генерируя читаемые промпты, которые обходят perplexity фильтры, сохраняя при этом высокие показатели успешности атак.

    
    These prompts are interpretable, diverse, and can generalize to unforeseen harmful behaviors. They also transfer better to black-box LLMs than their unreadable counterparts when using limited training data or a single proxy model. 
    Эти подсказки поддаются интерпретации, разнообразны и могут быть обобщены на непредвиденное вредное поведение. Они также лучше переносятся в black-box LLM, чем их нечитаемые аналоги, при использовании ограниченных обучающих данных или единственной прокси-модели.

    They refine the agent using a ReST-like method that iteratively trains on previous trajectories, using growing-batch reinforcement learning with AI feedback for continuous self-improvement and self-distillation. The authors demonstrate that starting from a prompted large model, they can produce a fine-tuned small model with comparable performance on challenging compositional question-answering benchmarks, but with two orders of magnitude fewer parameters. 
    Они совершенствуют агент, используя метод, подобный ReST, который итеративно обучается по предыдущим траекториям, используя обучение с подкреплением по мере роста батча с обратной связью ИИ для непрерывного самосовершенствования и самодистилляции. Авторы демонстрируют, что, отталкиваясь от большой модели с запросом, они могут создать дообученную малую модель с сопоставимой производительностью в сложных композиционных вопрос-ответ бенчмарках, но с на два порядка меньшим количеством параметров.


    The authors conclude that more work needs to be done to make LLMs safe, as even smaller, unaligned models can be used to jailbreak larger ones.
    Авторы приходят к выводу, что необходимо продолжать работу над безопасностью LLM, поскольку даже меньшие, unaligned модели могут быть использованы для взлома больших.

    The article titled "Tree of Attacks: Jailbreaking Black-Box LLMs Automatically" presents a new method, Tree of Attacks with Pruning (TAP), for automatically generating jailbreaks for Large Language Models (LLMs).
    Статья под названием "Tree of Attacks: Jailbreaking Black-Box LLMs Automatically" представляет новый метод, Дерево атак с прунингом (TAP), для автоматической генерации джейлбрейков для больших языковых моделей (LLM).

    
    The article presents a study on fingerprinting Large Language Models (LLMs) to protect intellectual property and ensure compliance with licensing terms. The authors propose a lightweight instruction tuning method where a model publisher specifies a private key and implants it as a backdoor in the LLM.
    В статье представлено исследование по маркировке больших языковых моделей (LLM) для защиты интеллектуальной собственности и обеспечения соблюдения условий лицензирования. Авторы предлагают метод легковесного дообучения на инструкциях, при котором издатель модели указывает закрытый ключ и внедряет его в качестве бэкдора в LLM.

    The article "Security and Privacy Challenges of Large Language Models: A Survey" provides a comprehensive review of the vulnerabilities, security, and privacy challenges associated with Large Language Models (LLMs). It highlights the significant advantages of LLMs in various fields while also addressing their susceptibility to security and privacy attacks, such as jailbreaking, data poisoning, and PII leakage.
    Статья "Security and Privacy Challenges of Large Language Models: A Survey" представляет собой всесторонний обзор уязвимостей, проблем безопасности и конфиденциальности, связанных с большими языковыми моделями (LLM). В ней подчеркиваются значительные преимущества LLM в различных областях, а также их уязвимость к атакам на безопасность и конфиденциальность, таким как джейлбрейкинг, отравление данных и утечка PII. 



    Ты - профессиональный переводчик на русский язык. Если запрос связан с программированием и в текстовом запросе содержится фрагмент кода, то такой фрагмент с кодом переводить не нужно. Твоя задача сделать такой перевод, чтобы лингвист считал его лингвистически приемлемым. По аналогии с приведенными выше примерами переведи следующий текст на русский язык, сохранив исходное форматирование текста и переведя !все слова.


    """

    def __init__(self, email="", prompts={}, add=True):
        if prompts and add:
            for name, prompt in prompts.items():
                self.prompts[name] = prompt
        elif prompts:
            self.prompts = prompts

        dotenv.load_dotenv()
        self.llm = GigaChat(
            credentials=os.getenv("GIGACHAT_CREDENTIALS"),
            verify_ssl_certs=False,
            timeout=6000,
            model="GigaChat-Pro",
            temperature=0.1,
            scope=os.getenv("GIGACHAT_API_SCOPE")
        )


    def _to_query(self, prompt: str, filename: str, num_pages: int = 10) -> str:
        if not os.path.exists(filename):
            logging.error(f'_to_query: No such file: {filename}')
            return ""

        loader = PyPDFLoader(filename)
        documents = loader.load()
        all_docs = documents[0].page_content
        
        for doc in documents[:num_pages]:
            all_docs += "\n" + doc.page_content
            
        return prompt + f'\n\n"{all_docs}"\n\n' + prompt

    def _get_answer(self, query: str) -> str:
        answer = self.llm.invoke(query)
        return answer.content

    def apply_prompt_to_article(self, prompt: str, filename: str) -> str:
        return self._get_answer(self._to_query(prompt, filename))
    
    def apply_micro_conclusions_prompt_to_article(self, filename: str) -> str:
        return self._get_answer(self._to_query(self.prompts["micro_conclusions"], filename, 1))

    def apply_translation_prompt_to_article(self, prompt: str) -> str:
        return self._get_answer(self.translation_prompt + prompt)
    
    def parse_article(self, filename: str) -> list[tuple]:
        answers = []
        for name, prompt in self.prompts.items():
            answers.append( 
                (name, self.apply_prompt_to_article(prompt, filename))
            )
        
        return answers

    def parse_article_json(self, filename: str) -> list[tuple]:
        answers = {}
        for name, prompt in self.prompts.items():
            answers[name] = self.apply_prompt_to_article(prompt, filename)
        return answers


    def parse_all(self, filenames: list) -> list[tuple]:
        answers = []
        for i in range(len(filenames)):
            answers.append(self.parse_article(filenames[i]))
        return answers    
    
    def parse_to_summary(self, filename: str) -> str:
        return self.apply_prompt_to_article(self.prompts["summary"], filename)
    
    def parse_all_to_summary(self, filenames=[]) -> list[str]:
        summaries = []
            
        for i in range(len(filenames)):
            summaries.append(self.parse_to_summary(filenames[i]))
        return summaries


    def write_to_file(self, filename: str, parsed_article: OrderedDict):
        with open(filename, mode='w') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')

            for key, value in parsed_article:

                if key == "article_type":
                    writer.writerow(("math", ""))
                    writer.writerow(("github", ""))
                    writer.writerow(("source", ""))

                writer.writerow((key, value))
