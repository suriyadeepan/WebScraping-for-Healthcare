import pandas as pd
from tqdm import tqdm

from phscrape.common import get_page

SRC = "https://www.medicines.org.uk/emc/browse-medicines"
DOMAIN = "https://www.medicines.org.uk"


class EmcCrawler:

    def __init__(self, url=SRC):
        self.url = url
        self.page = get_page(url)

    def crawl(self, k=0):
        data = self._crawl_collections(k)
        data = self._crawl_drug_pages(data)
        self.data = data
        return data

    def _make_drug_pages(self, page=None):
        if page is None:
            page = self.page
        if isinstance(page, type("69")):
            page = get_page(page)
        # get list of all urls
        _urls_all = [a.attrs['href'] for a in page.find_all(
            'a', recursive=True) if 'href' in a.attrs]
        pages = []
        for _url in page.select('h2>a'):
            uid = _url.attrs.get('href').split('/')[-2]
            manu = _url.parent.find_next_siblings()[1].text
            name = _url.text.strip()
            pil_url = f"/emc/product/{uid}/pil"
            smpc_url = f"/emc/product/{uid}/smpc"
            pages.append({
                'smpc': DOMAIN + smpc_url if smpc_url in _urls_all else None,
                'pil': DOMAIN + pil_url if pil_url in _urls_all else None,
                'name': name,
                "manufacturer": manu,
                "SmpcLink": None,
                "PilLink": None,
                "uid": uid
            })
        return pages

    def _crawl_collections(self, k=0):
        collections = self._get_pagination()
        drug_pages = []
        pbar = tqdm(collections)
        for collection in pbar:
            drug_pages.extend(
                self._make_drug_pages(collection))
            if k > 0 and len(drug_pages) > k:
                return pd.DataFrame(drug_pages[:k])

        return pd.DataFrame(drug_pages)

    def _crawl_drug_pages(self, data):
        pbar = tqdm(data.iterrows(), total=data.shape[0])
        for idx, row in pbar:
            pbar.set_description(str(row["name"]))
            if row.smpc:
                smpc_page = get_page(row.smpc)
                smpc = self._get_smpc_from_page(smpc_page, row.uid)
                data.at[idx, "SmpcLink"] = smpc
            if row.pil:
                pil_page = get_page(row.pil)
                pil = self._get_pil_from_page(pil_page, row.uid)
                data.at[idx, "PilLink"] = pil
        return data

    def _get_pagination(self):
        pagination_sel = ".browse-head"
        pagination = self.page.select_one(pagination_sel)
        collections = [DOMAIN + a.get('href')
                       for a in pagination.select('li>a') if 'href' in a.attrs]
        return collections

    def _get_smpc_from_page(self, page, uid):
        for a in page.find_all('a'):
            if 'href' in a.attrs:
                if '/emc/files/smpc' in a.get("href"):
                    return a.get('href')

        content = str(page.select_one('.smpc'))
        local_filepath = f'data/emc/smpc/{uid}.html'
        with open(local_filepath, 'w') as fd:
            fd.write(str(page.select_one('.smpc')))

        return local_filepath

    def _get_pil_from_page(self, page, uid):
        pil_download_link = page.select_one(".pil-download>a").get('href')
        if pil_download_link:
            return DOMAIN + pil_download_link
        return ""


def crawl_all():
    return EmcCrawler().crawl()


def crawl_k(k):
    return EmcCrawler().crawl(k)
