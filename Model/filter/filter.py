from researcher.matching.researcher_relation import ResearcherMatcher
from tenders.matching.tenders_relation import TendersMatcher


class Filter:
    def __init__(self):
        self.rm = ResearcherMatcher()
        self.tm = TendersMatcher()
    
