# WebScraping for Healthcare

Scraping the internet for extracting healthcare and pharma data.

- [x] Drug Bank
- [x] clinicaltrials.gov
- [x] COVID19 API [https://covid19api.com/](https://covid19api.com/)
- [ ] twitter #remdesivir
- [ ] Smpc-PIL pair extraction

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
