from auto_reco.clb_filter import Filter
# from researcher.matching.researcher_relation import ResearcherMatcher
from auto_reco.postprocess import PostProcess
# rm = ResearcherMatcher()
fl = Filter()
pp = PostProcess()

# def get_sim_researchers(profile):
#     return rm.match_by_profile(profile)

def get_reco_tenders(profile):
    return fl.match(profile)

if __name__ == '__main__':
    profile = {"id": "Test@0.com","divisions": ["d_08", "d_10", "d_09"], "tags": []}
    tmp_df = get_reco_tenders(profile)
    print(pp.run(profile['id'], tmp_df))