import {AxiosPromise, AxiosResponse} from 'axios'
type ResearchFieldLevel = 'division'|'group'|2|1
export interface ResearchField{
    name:string
    level:ResearchFieldLevel
    subFields:Array<ResearchField>|undefined|null

}
export interface UserInfo{
    firstName:string
    lastName:string
    avatar:string
    university:string
    researchFileds:Array<ResearchFieldsItem>
    tags:Array<string>
}

export interface ResearchFieldsItem{
    field:string
    subField:Array<string>
}
export interface ResearchFields{
    [key:string]:ResearchFieldsItem
}

export interface CustomAPIResponse{
    code:string|number,
    data?:JSON|object
    msg:string
}

export interface CustomAPIResponse32{
    code:string|number,
    data?:JSON|object
    msg:string
}
