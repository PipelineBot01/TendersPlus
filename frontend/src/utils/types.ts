import {AxiosPromise, AxiosResponse} from 'axios'
type ResearchFieldLevel = 'division'|'group'|2|1|'DIVISION'|'GROUP'

export interface Login{
    email:string
    password:string
    rememberme?:boolean
}

export interface ResearchField{
    name:string
    level:ResearchFieldLevel
    sub_fields:Array<ResearchField>|undefined|null

}

export interface UserInfo{
    first_name:string
    last_name:string
    university:string
    research_fields:Array<ResearchFieldsItem>
    tags:Array<string>
    access_token:string
}

export interface ResearchFieldsItem{
    field:string
    sub_fields:Array<string>
}
export interface ResearchFields{
    [key:string]:ResearchFieldsItem
}

export interface CustomAPIResponse<T>{
    code:string|number,
    data?:T
    msg?:string
}


