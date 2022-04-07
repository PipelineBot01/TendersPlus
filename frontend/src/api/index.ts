import {request} from './request'

import type { 
	UserInfo, 
	CustomAPIResponse, 
	Login, 
	Signup, 
	ProfileForm,
	MatchResearcher, 
	UniversityStrengthMap,
	QueryTender,
	QueryType,
	UserAction } from '../utils/types'

export const getUserInfoAPI = ():Promise<CustomAPIResponse<UserInfo>> =>{
	return request.get('/user')
}

export const setUserInfoAPI = (data:ProfileForm):Promise<CustomAPIResponse<string>>=>{
	return request.post('/user', data)
}

export const loginAPI = (data:Login):Promise<CustomAPIResponse<UserInfo>>=>{
	return request.post('/account/login', data)
}

export const signupAPI = (data:Signup):Promise<CustomAPIResponse<UserInfo>>=>{
	return request.post('/account/signup', data)
}

export const strengthOverviewAPI = ():Promise<CustomAPIResponse<UniversityStrengthMap>>=>{
	return request.get('/strength_overview')
}

export const matchResearcherAPI = (data:MatchResearcher):Promise<CustomAPIResponse<any>> =>{
	return request.post('/matcher/researchers', data)
}

export const queryTendersAPI = (type:QueryType, query:string|number):Promise<CustomAPIResponse<QueryTender[]>>=>{
	switch (type){
	case 'latest':
		return query ? request.get('/search/latest', {params:{
			n:query
		}}) : request.get('/search/latest')
	case 'expiring':
		return query ? request.get('/search/expiring', {params:{
			n:query
		}}) : request.get('/search/expiring')
	case 'hot':
		return query ? request.get('/search/hot', {params:{
			n:query
		}}) : request.get('/search/hot')
	default:
		return request.get('/search', {params:{query}})
	}
}

export const queryTendersCountAPI = ():Promise<CustomAPIResponse<number>>=>{
	return request.get('/search/count')
}

export const userActionAPI = (data:UserAction):Promise<CustomAPIResponse<string>>=>{
	return request.post('/action', data)
}

export const getUserFavouriteAPI = ():Promise<CustomAPIResponse<QueryTender[]>>=>{
	return request.get('/favourite')
}

export const getUserFavouriteIdAPI = ():Promise<CustomAPIResponse<string[]>>=>{
	return request.get('/favourite/id')
}

export const addUserFavouriteAPI = (id:string):Promise<CustomAPIResponse<string>>=>{
	return request.post('/favourite/add', {id})
}

export const removeUserFavouriteAPI = (id:string):Promise<CustomAPIResponse<string>>=>{
	return request.post('/favourite/remove', {id})
}