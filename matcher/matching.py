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
               "divisions": ["d_11", "d_17", "d_06"],
               "tags": ["parkinson disease",
                        "drug-related side effects and adverse reactions",
                        "proliferation",
                        "health personnel",
                        "weight loss",
                        "physical"]}


    tmp_df = get_reco_tenders(profile)
    # print(fl.get_hot_tenders())
    print(reco_process.run("StageZero@anu.edu.au", tmp_df))
    # print(get_sim_researchers({"id": "Ryanyang@anu.com", "divisions": ["d_20", "d_21", "d_22"], "tags": ["Human"]}))
    #
    # {"id": "jennytestsix@test.com", "divisions": ["d_14", "d_15"], "tags": ["accounting",
    #                                                                         "bitcoin",
    #                                                                         "commodity",
    #                                                                         "credit",
    #                                                                         "development project",
    #                                                                         "ecotourism",
    #                                                                         "empowerment",
    #                                                                         "food supply",
    #                                                                         "gross domestic product",
    #                                                                         "small business"]}

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