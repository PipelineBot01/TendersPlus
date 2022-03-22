import axios from "axios"
import interceptor from "./interceptor"


export const request = axios.create({
	baseURL:'http://http://110.40.137.110/tendersplus',
	timeout:5000
})

request.interceptors.request.use(interceptor.request.handleConfig, interceptor.reponse.handleError)
request.interceptors.response.use(interceptor.reponse.handleResponse, interceptor.reponse.handleError)
