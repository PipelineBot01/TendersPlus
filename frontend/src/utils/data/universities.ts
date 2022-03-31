/**
 * the university information is derived from 
 * https://www.studyaustralia.gov.au/english/study/universities-higher-education/list-of-australian-universities
 */
interface University{
    [key:string]:Array<string>
}
export const universities:University = {
	'Australian Capital Territory':['Australian National University', 'University of Canberra'],
	'New South Wales':['Australian Catholic University', 'Charles Sturt University', 'Macquarie University', 'Southern Cross University', 'University of New England', 'University of New South Wales', 'University of Newcastle', 'University of Sydney', 'University of Technology, Sydney', 'Western Sydney University', 'University of Wollongong'],
	'Northern Territory':['Charles Darwin University'],
	'Queensland':['Bond University', 'CQ University', 'Federation University of Australia', 'Griffith University', 'James Cook University', 'Queensland University of Technology', 'University of Queensland', 'University of Southern Queensland', 'University of the Sunshine Coast'],
	'South Australia':['Carnegie Mellon University', 'Flinders University', 'Torrens University Australia', 'University of Adelaide', 'University of South Australia'],
	'Tasmania':['University of Tasmania'],
	'Victoria':['Deakin University', 'Federation University of Australia', 'La Trobe University', 'Monash University', 'RMIT University', 'Swinburne University of Technology', 'University of Divinity', 'University of Melbourne', 'Victoria University'],
	'Western Australia':['Curtin University', 'Edith Cowan University', 'Murdoch University', 'University of Notre Dame Australia', 'University of Western Australia']
}

export const universitiesMap:{[key:string]:string} = {
	u_01:'University of Canberra'
}