import { createSlice, PayloadAction } from "@reduxjs/toolkit"
import type {UserInfo, ResearchFieldsItem} from '../../utils/types'
export  interface UserState extends UserInfo {
    rememberme:boolean
	access_token:string
}

const initialState:UserState = {
	firstName:'',
	lastName:'',
	avatar:'',
	researchFileds:[],
	tags:[],
	university:'',
	rememberme:false,
	access_token:''
}

const userSlice = createSlice({
	name:'user',
	initialState:initialState,
	reducers:{
		//
		setFirstName(state, action:PayloadAction<string>){
			state.firstName = action.payload
		},
		setLastName(state, action:PayloadAction<string>){
			state.lastName = action.payload
		},
		setUniversity(state, action:PayloadAction<string>){
			state.university = action.payload
		},
		setTags(state, action:PayloadAction<Array<string>>){
			state.tags = action.payload
		},
		setResearchFields(state, action:PayloadAction<Array<ResearchFieldsItem>>){
			state.researchFileds = action.payload
		},
		setUserInfo(state, action:PayloadAction<UserState>){
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