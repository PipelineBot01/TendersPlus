import Cookies from "js-cookie"
import { userActionAPI } from "../api"
import type { UserAction } from "./types"
export function useCollector(data:UserAction){
	
  if(Cookies.get('access_token')){
		
		
    userActionAPI(data)
  }
}