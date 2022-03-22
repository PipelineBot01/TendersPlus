import {request} from './request'
import type { UserInfo, CustomAPIResponse, Login } from '../utils/types'

// export const getGrantOpportunitiesAPI = ():Promise<CustomAPIResponse>=>{
// 	return request.get('/api/tenders/open')
// }

export const getUserInfoAPI = ():Promise<CustomAPIResponse<UserInfo>> =>{
	return request.get('/api/user')
}

export const setUserInfoAPI = (data:UserInfo):Promise<CustomAPIResponse<string>>=>{
	return request.post('/api/user', data)
}

export const loginAPI = (data:Login):Promise<CustomAPIResponse<UserInfo>>=>{
	return request.post('/api/account/login', data)
}