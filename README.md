# WebScraping for Healthcare

Scraping the internet for extracting healthcare and pharma data.

- [x] [Drug Bank](https://go.drugbank.com/drugs/DB00295)
- [ ] [clinicaltrials.gov](https://clinicaltrials.gov)
- [ ] [twitter #remdesivir](https://twitter.com/search?q=remdesivir&src=typeahead_click&f=live)
- [ ] [Smpc-PIL pair extraction](#)

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
