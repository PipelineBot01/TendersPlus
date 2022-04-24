from filter.filter import Filter
from researcher.matching.researcher_relation import ResearcherMatcher


def get_sim_researchers(profile):
    rm = ResearcherMatcher()
    return rm.match_by_profile(profile)


def get_reco_tenders(profile):
    fl = Filter()
    return fl.match(profile)

if __name__ == '__main__':
    print(get_reco_tenders({'id': 'Ryanyang@anu.com', 'divisions': ["d_20", "d_21", "d_22"], 'tags': ["Human"]}))