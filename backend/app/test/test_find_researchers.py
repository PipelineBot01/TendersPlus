from utils.matcher.researcher import researcher_matcher

divs=["d_10", "d_08"]
tags=['asd']

output = researcher_matcher.match_by_profile(divs,tags)
print(output)