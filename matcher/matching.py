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
    profile = {"id": "StageZero@anu.edu.au",
               "divisions": ["d_06", "d_11", "d_17"],
               "tags": ["parkinson disease",
                        "drug-related side effects and adverse reactions",
                        "proliferation",
                        "health personnel",
                        "weight loss",
                        "physical activity",
                        "triage",
                        "ankle",
                        "home care services",
                        "health care professionals"]}

    profile = {'id': 'u6872840@anu.edu.au', 'divisions': ['d_08'], 'tags': []}
    #
    # profile = {"id": "jennytestone@test.com", "divisions": ["d_14", "d_15"], "tags": ["accounting",
    #                                                                               "bank",
    #                                                                               "cash",
    #                                                                               "contingency",
    #                                                                               "design",
    #                                                                               "economic success",
    #                                                                               "endorsements",
    #                                                                               "financial performance",
    #                                                                               "gold standard",
    #                                                                               "income tax"]}

    tmp_df = get_reco_tenders(profile)
    # print(tmp_df['go_id'].tolist())
    # print(fl.get_hot_tenders())
    print(reco_process.run("u6872840@anu.edu.au", tmp_df))
    # print(get_sim_researchers({"id": "Ryanyang@anu.com", "divisions": ["d_20", "d_21", "d_22"], "tags": ["Human"]}))
    #

    # {"id": "jennytestone@test.com", "divisions": ["d_14", "d_15"], "tags": ["accounting",
    #                                                                               "bank",
    #                                                                               "cash",
    #                                                                               "contingency",
    #                                                                               "design",
    #                                                                               "economic success",
    #                                                                               "endorsements",
    #                                                                               "financial performance",
    #                                                                               "gold standard",
    #                                                                               "income tax"]}