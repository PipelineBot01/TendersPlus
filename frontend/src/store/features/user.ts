import { createSlice, PayloadAction } from "@reduxjs/toolkit"
import type {UserInfo, ResearchFieldsItem, ProfileForm} from '../../utils/types'
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
  access_token:'',
  favourite:localStorage.getItem('favourite')?.split('/').slice(1) || [],
  subscribe_status:parseInt(localStorage.getItem('subscribe_status') || '0')
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
    setTags(state, action:PayloadAction<string[]>){
      state.tags = action.payload
    },
    setResearchFields(state, action:PayloadAction<ResearchFieldsItem[]>){
      state.research_fields = action.payload
      let research_field = ''
      action.payload.forEach(e=>{
        typeof e === 'object' ? research_field += `/${e.field}` : research_field += `/${e}`
      })
      localStorage.setItem('research_fields', research_field)
    },
    setUserInfo(state, action:PayloadAction<UserState>){
      console.log('payload', action)
      
      localStorage.setItem('first_name', action.payload.first_name)
      localStorage.setItem('last_name', action.payload.last_name)
      localStorage.setItem('email', action.payload.email)
      localStorage.setItem('university', action.payload.university)
      localStorage.setItem('rememberme', action.payload.rememberme + '')
      localStorage.setItem('tags', action.payload?.tags.reduce((prev:string, cur:string)=>prev + '/' + cur, ''))
      localStorage.setItem('subscribe_status', action.payload.subscribe_status + '')
      let research_field = ''
      action.payload?.research_fields.forEach(e=>{
        typeof e === 'object' ? research_field += `/${e.field}` : research_field += `/${e}`
      })

      localStorage.setItem('research_fields', research_field)
      localStorage.setItem('favourite', action.payload?.favourite.reduce((prev:string, cur:string)=>prev + '/' + cur, ''))

      Object.assign(state, action.payload)
    },
    setRememberme(state, action:PayloadAction<boolean>){
      localStorage.setItem('rememberme', action.payload + '')
      state.rememberme = action.payload
    },
    setAccessToken(state, action:PayloadAction<string>){
      
      state.access_token = action.payload
    },
    setFavourite(state, action:PayloadAction<string[]>){
      state.favourite = action.payload
      localStorage.setItem('favourite', action.payload.reduce((prev:string, cur:string)=>prev + '/' + cur, ''))
    },
    setUserProfile(state, action:PayloadAction<ProfileForm>){
      localStorage.setItem('first_name', action.payload.first_name)
      localStorage.setItem('last_name', action.payload.last_name)
      localStorage.setItem('tags', action.payload.tags.reduce((prev:string, cur:string)=>prev + '/' + cur, ''))
      Object.assign(state, action.payload)
    },
    setSubscribeStatus(state, action:PayloadAction<number>){  
      state.subscribe_status = action.payload
      localStorage.setItem('subscribe_status', action.payload + '')

    }
  }
})

export const {setFirstName, 
  setLastName, 
  setTags,
  setUniversity, 
  setResearchFields, 
  setUserInfo, 
  setAccessToken,
  setFavourite,
  setUserProfile,
  setSubscribeStatus } = userSlice.actions
export default userSlice.reducer