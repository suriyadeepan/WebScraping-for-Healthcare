# WebScraping for Healthcare

Scraping the internet for extracting healthcare and pharma data.

- [x] Drug Bank
- [x] clinicaltrials.gov
- [x] COVID19 API [4.0-sr-covid19_api.ipynb](https://github.com/suriyadeepan/WebScraping-for-Healthcare/blob/main/notebooks/4.0-sr-covid19_api.ipynb)
- [ ] twitter #remdesivir
- [ ] Smpc-PIL pair extraction
  - [x] EMC
  - [x] HPRA
  - [ ] MHRA

## Drug Bank

```python
from phscrape import drugbank

url = "https://go.drugbank.com/drugs/DB00295"
data = drugbank.fetch(url)
print(data)
```

```console
{'name': 'Morphine', 'type': 'Small Molecule', 
'description': 'Morphine, the main alkaloid of opium, was first obtained from poppy seeds in 1805. It is a potent analgesic, though its use is limited due to tolerance, withdrawal, and the risk of abuse. Morphine is still routinely used today, though there are a number of semi-synthetic opioids of varying strength such as codeine, fentanyl, methadone, hydrocodone, hydromorphone, meperidine, and oxycodone.\nMorphine was granted FDA approval in 1941.', 
'ingredients': ['Morphine acetate', 'Morphine hydrochloride', 'Morphine hydrochloride trihydrate', 'Morphine mesylate', 'Morphine nitrate', 'Morphine phosphate', 'Morphine sulfate', 'Morphine sulfate pentahydrate', 'Morphine tartrate'], 
'unii': '76I7G6D29C', 
'dosage_forms': ['Capsule, coated, extended release', 'Capsule', 'Suppository, extended release', 
'Injection, solution', 'Tincture', 'Suppository', 'Injection, lipid complex', 'Solution', 'Liquid',
'Tablet, extended release', 'Granule, for suspension', 'Tablet, multilayer, extended release',
'Tablet, film coated, extended release', 'Solution, concentrate', 'Capsule, coated pellets', 'Tablet',
'Granule, delayed release', 'Powder', 'Capsule, extended release', 'Syrup', 'Tablet, film coated',
'Injection', 'Solution / drops', 'Injection, solution, concentrate']}
```

## Clinical Trials

```python
from phscrape import clinicaltrials

dexamethasone_study = 'https://clinicaltrials.gov/ct2/show/NCT04707534?cond=covid19&draw=2&rank=1'
data = clinicaltrials.fetch(dexamethasone_study)
print(data)
```

```console
{'status': 'Recruiting',
 'phase': 'Phase 4',
 'age': '18 Years and older \xa0 (Adult, Older Adult)',
 'sex': 'All',
 'nct': 'NCT04707534',
 'inclusion': ['Age ≥ 18 years old',
  'RT-PCR confirmed COVID-19 infection',
  'Positive pressure ventilation (non-invasive or invasive) or high flow nasal cannula (HFNC) or need supplemental oxygen with oxygen mask or nasal cannula'],
 'exclusion': ['Underlying disease requiring chronic corticosteroids',
  'Severe adverse events before admission, i.e. cardiac arrest;',
  'Contraindication for corticosteroids;',
  'Death is deemed to be imminent and inevitable during the next 24 hours',
  'Recruited in other clinical intervention trial',
  'Pregnancy',
  'Patient on judicial protection'],
 'enrollment': '300 participants'}
 ```

## COVID19 API

```python
import requests
import pandas as pd
import json

_from = "2021-01-01T00:00:00Z"
_to = "2021-10-20T00:00:00Z"
country = 'India'.lower()
resp = requests.get(
    f'https://api.covid19api.com/country/{country}/status/confirmed?from={_from}&to={_to}'
)
data = json.loads(resp.content)
df = pd.DataFrame(data)
```

## EMC - Electronic Medicines Compendium

```python
from phscrape import emc

df = emc.crawl_k(5)
```

|    | smpc                                                | pil                                                | name                                                                      | manufacturer                                      | SmpcLink                 | PilLink                                              |   uid |
|---:|:----------------------------------------------------|:---------------------------------------------------|:--------------------------------------------------------------------------|:--------------------------------------------------|:-------------------------|:-----------------------------------------------------|------:|
|  0 | https://www.medicines.org.uk/emc/product/305/smpc   | https://www.medicines.org.uk/emc/product/305/pil   | 4head Cutaneous Stick                                                     | Diomed Developments Limited                       | data/emc/smpc/305.html   | https://www.medicines.org.uk/emc/files/pil.305.pdf   |   305 |
|  1 | https://www.medicines.org.uk/emc/product/10525/smpc | https://www.medicines.org.uk/emc/product/10525/pil | Abacavir 300 mg Film-Coated Tablets                                       | Dr. Reddy's Laboratories (UK) Ltd                 | data/emc/smpc/10525.html | https://www.medicines.org.uk/emc/files/pil.10525.pdf | 10525 |
|  2 | https://www.medicines.org.uk/emc/product/12475/smpc | https://www.medicines.org.uk/emc/product/12475/pil | Abacavir 300mg Film-coated tablets                                        | Aurobindo Pharma - Milpharm Ltd.                  | data/emc/smpc/12475.html | https://www.medicines.org.uk/emc/files/pil.12475.pdf | 12475 |
|  3 | https://www.medicines.org.uk/emc/product/9079/smpc  | https://www.medicines.org.uk/emc/product/9079/pil  | Abacavir Mylan 300 mg Film-coated Tablets                                 | Mylan                                             | data/emc/smpc/9079.html  | https://www.medicines.org.uk/emc/files/pil.9079.pdf  |  9079 |
|  4 | https://www.medicines.org.uk/emc/product/7375/smpc  | https://www.medicines.org.uk/emc/product/7375/pil  | Abacavir/Lamivudine 600 mg/300 mg film-coated tablets                     | Lupin Healthcare (UK) Ltd                         | data/emc/smpc/7375.html  | https://www.medicines.org.uk/emc/files/pil.7375.pdf  |  7375 |


## HPRA - Health Products Regulatory Authority

```python
from phscrape import hpra

df = hpra.crawl_k(5)
df
```


|    | Name                                                                                          | SPC                                                                                        | PIL                                                                                                                                                     |
|---:|:----------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------|
|  0 | 0.18 % w/v Sodium Chloride and 4 % w/v Glucose Intravenous Infusion BP, Solution for Infusion | https://www.hpra.ie/img/uploaded/swedocuments/Licence_PA0179-003-006_10092019132631.pdf    | https://www.hpra.ie/img/uploaded/swedocuments/2201112.PA0179_003_006.3301dac4-a0ce-4656-935d-394237130d47.000001Product%20Leaflet%20Approved.180206.pdf |
|  1 | 0.18%w/v Sodium Chloride and 4.0% w/v Glucose Intravenous Infusion BP, (Viaflo Container)     | https://www.hpra.ie/img/uploaded/swedocuments/Licence_PA2299-008-005_24092020152132.pdf    | https://www.hpra.ie/img/uploaded/swedocuments/974b101b-bc8d-4cdc-baa3-4b3542835ba3.pdf                                                                  |
|  2 | 0.9 % w/v Sodium Chloride Injection BP                                                        | https://www.hpra.ie/img/uploaded/swedocuments/Licence_PA0179-002-013_25022020122300.pdf    | https://www.hpra.ie/img/uploaded/swedocuments/0dade6ce-2f83-4985-996e-ccc05506e2be.pdf                                                                  |
|  3 | 0.9% Sodium Chloride Intravenous Infusion Solution                                            | https://www.hpra.ie/img/uploaded/swedocuments/Licence_PA22859-001-001_02062020081054.pdf   | https://www.hpra.ie/img/uploaded/swedocuments/659e659f-1764-4e84-abdb-5dc62116cc29.pdf                                                                  |
|  4 | 1% w/v Lidocaine Hydrochloride Injection BP                                                   | https://www.hpra.ie/img/uploaded/swedocuments/Licence_PA0179-037-001_14112019130102.pdf    | https://www.hpra.ie/img/uploaded/swedocuments/2159164.PA0179_037_001.72651cf5-3519-41bb-a479-6ccde7d81930.000001pil1percent.150427.pdf
