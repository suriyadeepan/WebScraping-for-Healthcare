from phscrape.common import get_page


class ClinicalTrials:

    def __init__(self, url):
        self.url = url
        self.page = get_page(url)
        self._get_inc_exc_header_nodes()

    def _get_inc_exc_header_nodes(self):
        inc_node, exc_node = None, None
        for p in self.page.find_all("p"):
            if 'Inclusion Criteria:' == p.text.strip():
                inc_node = p
                if exc_node:
                    break
            if 'Exclusion Criteria:' == p.text.strip():
                exc_node = p
                if inc_node:
                    break

        self.inclusion_header = inc_node
        self.exclusion_header = exc_node

    def _get_phase(self):
        for span in self.page.find_all('span'):
            text = span.text.lower().strip()
            if 'phase' in text and len(text) > len('phase'):
                return span.text.strip()
        return ""

    def _get_enrollment(self):
        for td in self.page.find_all('td', {'headers': 'studyInfoColData'}):
            text = td.text.strip().lower()
            if 'participants' in text:
                return td.text.strip()
        return ""

    def _get_eligibility(self):
        _types = self.page.find_all('td', {'headers': 'elgType'})
        _elgs = self.page.find_all('td', {'headers': 'elgData'})
        age, sex = None, None
        for _type, _elg in zip(_types, _elgs):
            if 'age' in _type.text.lower():
                age = _elg.text.strip()
                if sex:
                    break
            if 'sex' in _type.text.lower():
                sex = _elg.text.strip()
                if age:
                    break
        return age, sex

    def fetch(self):
        return {
            "status": self.status,
            "phase": self.phase,
            "age": self.age,
            "sex": self.sex,
            "nct": self.nct,
            "inclusion": self.inclusion_criteria,
            "exclusion": self.exclusion_criteria,
            "enrollment": self.enrollment
        }

    @property
    def inclusion_criteria(self):
        return [li.text.strip()
                for li in self.inclusion_header.find_next_sibling().find_all('li')]

    @property
    def exclusion_criteria(self):
        return [li.text.strip()
                for li in self.exclusion_header.find_next_sibling().find_all('li')]

    @property
    def status(self):
        return self.page.select_one('.tr-status').text.strip().split('\n')[1].strip()

    @property
    def phase(self):
        return self._get_phase()

    @property
    def age(self):
        age, _ = self._get_eligibility()
        return age

    @property
    def nct(self):
        return self.page.find('meta',
                              {'property': 'og:url'}).attrs.get('content').split('/')[-1]

    @property
    def enrollment(self):
        return self._get_enrollment()

    @property
    def sex(self):
        _, sex = self._get_eligibility()
        return sex


def fetch(url):
    clinicaltrials = ClinicalTrials(url)
    return clinicaltrials.fetch()
