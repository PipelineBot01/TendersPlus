import { createSlice, PayloadAction } from "@reduxjs/toolkit"
import Cookies from "js-cookie"
import type {UserInfo, ResearchFieldsItem} from '../../utils/types'
export  interface UserState extends UserInfo {
    rememberme:boolean
	access_token:string
}

const initialState:UserState = {
	email:localStorage.getItem('email') || '',
	first_name:localStorage.getItem('first_name') || '',
	last_name:localStorage.getItem('last_name') || '',
	research_fields:localStorage.getItem('research_fields')?.split('/').slice(1) || [],
	tags:localStorage.getItem('tags')?.split('/').slice(1) || [],
	university:localStorage.getItem('university') || '',
	rememberme: localStorage.getItem('rememberme') === 'true',
	access_token:''
}

const userSlice = createSlice({
	name:'user',
	initialState:initialState,
	reducers:{
		//
		setFirstName(state, action:PayloadAction<string>){
			state.first_name = action.payload
		},
		setLastName(state, action:PayloadAction<string>){
			state.last_name = action.payload
		},
		setUniversity(state, action:PayloadAction<string>){
			state.university = action.payload
		},
		setTags(state, action:PayloadAction<Array<string>>){
			state.tags = action.payload
		},
		setResearchFields(state, action:PayloadAction<Array<ResearchFieldsItem>>){
			state.research_fields = action.payload
		},
		setUserInfo(state, action:PayloadAction<UserState|any>){
			localStorage.setItem('first_name', action.payload.first_name)
			localStorage.setItem('last_name', action.payload.last_name)
			localStorage.setItem('email', action.payload.email)
			localStorage.setItem('university', action.payload.university)
			localStorage.setItem('rememberme', action.payload.rememberme)
			localStorage.setItem('tags', action.payload?.tags.reduce((prev:string, cur:string)=>prev + '/' + cur, ''))
			localStorage.setItem('research_fields', action.payload?.research_fields.reduce((prev:string, cur:string)=>prev + '/' + cur, ''))
			Object.assign(state, action.payload)
		},
		setRememberme(state, action:PayloadAction<boolean>){
			state.rememberme = action.payload
		},
		setAccessToken(state, action:PayloadAction<string>){
			state.access_token = action.payload
		}
	}
})

export const {setFirstName, setLastName, setTags, setUniversity, setResearchFields, setUserInfo, setAccessToken } = userSlice.actions
export default userSlice.reducer