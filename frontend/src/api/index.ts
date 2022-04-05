import {request} from './request'

import type { 
	UserInfo, 
	CustomAPIResponse, 
	Login, 
	Signup, 
	ProfileForm,
	MatchResearcher, 
	UniversityStrengthMap,
	QueryTender } from '../utils/types'

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

export const queryTendersAPI = (query:string):Promise<CustomAPIResponse<Array<QueryTender>>>=>{
	return request.get('/search', {params:{query}})
}

export const queryLatestTendersAPI = (query?:number):Promise<CustomAPIResponse<Array<QueryTender>>>=>{
	return query ? request.get('/search/latest', {params:{
		n:query
	}}) : request.get('/search/latest')
}

export const queryExpiringTendersAPI = (query?:number):Promise<CustomAPIResponse<Array<QueryTender>>>=>{
	return query ? request.get('/search/expiring', {params:{
		n:query
	}}) : request.get('/search/expiring')
}
