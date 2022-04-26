from auto_reco.clb_filter import Filter
# from researcher.matching.researcher_relation import ResearcherMatcher

# rm = ResearcherMatcher()
fl = Filter()


# def get_sim_researchers(profile):
#     return rm.match_by_profile(profile)

def get_reco_tenders(profile):
    return fl.match(profile)

if __name__ == '__main__':
    print(get_reco_tenders({'id': 'test@0.com', 'divisions': ['d_08', 'd_09', 'd_10'], 'tags': []}))