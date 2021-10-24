from phscrape.common import get_page


SELECTORS = {
    "name": ".content-header>h1",
    "type": "#type",
    "description": "#background",
    "ingredients": ["#drug-salts-table", "strong>a"],
    "unii": "#unii",
    "dosageForms": "#dosages",
}


class DrugBank:
    def __init__(self, url):
        self.url = url
        self.page = get_page(url)

    def next_node(self, sel):
        node = self.page.select_one(sel)
        if node:
            return node.find_next_sibling()
        return ""

    def post_proc_description(self, desc):
        for sup in desc.find_all("sup"):
            sup.decompose()
        return desc.text.strip()

    def _get_ingredients(self):
        sel1, sel2 = SELECTORS["ingredients"]
        table = self.page.select_one(sel1)
        if table:
            return [item.text.strip() for item in table.select(sel2)]
        return []

    def _get_dosage_forms(self):
        dosage_table = self.page.select_one("#dosages")
        if dosage_table:
            rows = dosage_table.find_all("tr")[1:]
            return list(set([row.find("td").text for row in rows]))
        return []

    def fetch(self):
        return {
            "name": self.name_,
            "type": self.type_,
            "description": self.description_,
            "ingredients": self.ingredients_,
            "unii": self.unii_,
            "dosage_forms": self.dosage_forms_,
        }

    @property
    def name_(self):
        node = self.page.select_one(SELECTORS["name"])
        if node:
            return node.text.strip()
        return ""

    @property
    def type_(self):
        node = self.next_node(SELECTORS["type"])
        if node:
            return node.text.strip()
        return ""

    @property
    def description_(self):
        desc_node = self.next_node(SELECTORS["description"])
        if desc_node:
            return self.post_proc_description(desc_node)
        return ""

    @property
    def ingredients_(self):
        return self._get_ingredients()

    @property
    def unii_(self):
        return self.next_node(SELECTORS["unii"]).text.strip()

    @property
    def dosage_forms_(self):
        return self._get_dosage_forms()


def fetch(url):
    db = DrugBank(url)
    return db.fetch()
