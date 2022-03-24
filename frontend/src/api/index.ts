import {request} from './request'
import type { UserInfo, CustomAPIResponse, Login, Signup, ProfileForm } from '../utils/types'
import Cookies from 'js-cookie'

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
