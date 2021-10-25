import pytest
from phscrape.drugbank import DrugBank


@pytest.fixture
def db_scraper():
    return DrugBank("https://go.drugbank.com/drugs/DB00295")


def test_drugbank_name(db_scraper):
    name = db_scraper.name_
    print(name)
    assert "morphine" in name.lower()


def test_drugbank_type(db_scraper):
    _type = db_scraper.type_
    print(_type)
    assert "small" in _type.lower() and "molecule" in _type.lower()


def test_drugbank_description(db_scraper):
    description = db_scraper.description_
    print(description)
    assert "1941" in description


def test_drugbank_ingredients(db_scraper):
    ingredients = db_scraper.ingredients_
    print(ingredients)
    assert "Morphine tartrate" in ingredients
    assert len(ingredients) == 9


def test_drugbank_unii(db_scraper):
    unii = db_scraper.unii_
    print(unii)
    assert "76I7G6D29C" == unii


def test_drugbank_dosage_forms(db_scraper):
    dosage_forms = db_scraper.dosage_forms_
    print(dosage_forms)
    assert "Tablet, multilayer, extended release" in dosage_forms


def test_drugbank_fetch():
    from phscrape import drugbank

    url = "https://go.drugbank.com/drugs/DB00295"
    items = drugbank.fetch(url)
    assert len(items) > 0
    print(items)


def test_clinicaltrials_fetch():
    from phscrape import clinicaltrials

    url = "https://clinicaltrials.gov/ct2/show/NCT04452669?recrs=e&cond=covid19&draw=2"
    items = clinicaltrials.fetch(url)
    assert len(items) > 0
    assert items['nct'] == "NCT04452669"
    print(items)
