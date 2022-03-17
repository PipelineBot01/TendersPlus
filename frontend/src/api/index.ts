import {request} from './request'
import type { UserInfo, CustomAPIResponse } from '../utils/types'

export const getTendersAPI = () =>{
	return request.get('/api/tenders/open')
}

export const getUserInfoAPI = ():Promise<CustomAPIResponse> =>{
	return request.get('/api/user')
}

export const setUserInfoAPI = (data:UserInfo)=>{
	return request.post('/api/user', data)
}