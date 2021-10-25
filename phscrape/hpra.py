import pandas as pd
from tqdm import tqdm

from phscrape.common import get_page


def generate_pages(start=1, end=510):
    url_template = "https://www.hpra.ie/homepage/medicines/medicines-information/find-a-medicine/results?page={}&field=&query="
    return [url_template.format(n) for n in range(start, end)]


def scrape_docs_from_page(page):
    page_docs = []
    soup = get_page(page)
    for tr in soup.find_all('tr'):
        cols = tr.find_all('td')
        if len(cols) < 3:
            continue
        if not cols[-1].find('a'):
            continue
        if '.pdf' in cols[-1].find('a').get('href'):
            prod_title = tr.find('td', {'class': 'tdtop'}).find('a').text
            doc_url = "https://www.hpra.ie"
            docs = {'Name': prod_title}
            docs.update(
                {a.text: doc_url + a.get('href')
                 for a in cols[-1].find_all('a')})
            if 'SPC' in docs and 'PIL' in docs:
                if '.pdf' in docs['SPC'] and '.pdf' in docs['PIL']:
                    page_docs.append(docs)

    return page_docs


class HpraCrawler:

    def __init__(self):
        self.pages = generate_pages()
        self.cols = ["Name", "SPC", "PIL"]

    def crawl(self, k=0):
        drugs = []
        pbar = tqdm(self.pages)
        for page in pbar:
            drugs.extend(scrape_docs_from_page(page))
            pbar.set_description(drugs[-1]["Name"])
            if k > 0 and len(drugs) > k:
                return pd.DataFrame(drugs[:k])[self.cols]
        return pd.DataFrame(drugs)[self.cols]


def crawl_all():
    return HpraCrawler().crawl()


def crawl_k(k):
    return HpraCrawler().crawl(k)
