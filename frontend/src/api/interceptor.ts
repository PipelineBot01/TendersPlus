
/**
 * Configuration request interceptors
 */

import Cookies from "js-cookie"
import {AxiosRequestConfig, AxiosError, AxiosResponse} from "axios"
import { CustomAPIResponse } from "../utils/types"

export default {
	request:{
		handleConfig(config:AxiosRequestConfig){
            
			const access_token =  Cookies.get('access_token') || false
			if(access_token &&  config.headers){
				config.headers['x-token'] = access_token
			}
			console.log('intercept request:', config)
			return config
		},
		handleError(error:AxiosError){
			console.log('request error:', error)
			return Promise.reject(error)
		}
	},
	reponse:{
		handleResponse(response:AxiosResponse<CustomAPIResponse>){
			console.log('intercept response:', response)
			if(response.data){
				return response.data
			}else{
				return Promise.reject(response.status)
			}
		},
		handleError(error:AxiosError){
			console.log('response error:', error)
			return Promise.reject(error)
		}
	}
}