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
        return self.page.select_one(sel).find_next_sibling()

    def post_proc_description(self, desc):
        for sup in desc.find_all("sup"):
            sup.decompose()
        return desc.text.strip()

    def _get_ingredients(self):
        sel1, sel2 = SELECTORS["ingredients"]
        table = self.page.select_one(sel1)
        return [item.text.strip() for item in table.select(sel2)]

    def _get_dosage_forms(self):
        rows = self.page.select_one("#dosages").find_all("tr")[1:]
        return list(set([row.find("td").text for row in rows]))

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
        _name = self.page.select_one(SELECTORS["name"])
        return _name.text.strip()

    @property
    def type_(self):
        return self.next_node(SELECTORS["type"]).text.strip()

    @property
    def description_(self):
        # return self.next_node(SELECTORS["description"]).text.strip()
        desc_node = self.next_node(SELECTORS["description"])
        return self.post_proc_description(desc_node)

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
