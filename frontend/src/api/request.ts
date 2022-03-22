import axios from "axios"
import interceptor from "./interceptor"


export const request = axios.create({
	baseURL:'http://',
	timeout:5000
})

request.interceptors.request.use(interceptor.request.handleConfig, interceptor.reponse.handleError)
request.interceptors.response.use(interceptor.reponse.handleResponse, interceptor.reponse.handleError)
