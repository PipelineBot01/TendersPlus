from auto_reco.clb_filter import Filter
from researcher.matching.researcher_relation import ResearcherMatcher
from auto_reco import reco_process
rm = ResearcherMatcher()
fl = Filter()

def get_sim_researchers(profile):
    return rm.match_by_profile(profile)

def get_reco_tenders(profile):
    return fl.match(profile)

if __name__ == '__main__':
    profile = {"id": "jennytestone@test.com", "divisions": ["d_14", "d_15"], "tags": ['accounting',
                                                                                      'bank',
                                                                                      'cash',
                                                                                      'contingency',
                                                                                      'design',
                                                                                      'economic success',
                                                                                      'endorsements',
                                                                                      'financial performance',
                                                                                      'gold standard',
                                                                                      'income tax']}
    tmp_df = get_reco_tenders(profile)
    print(tmp_df)
    # print(get_sim_researchers({"id": "Ryanyang@anu.com", "divisions": ["d_20", "d_21", "d_22"], "tags": ["Human"]}))