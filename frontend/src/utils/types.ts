
export interface Login{
    email:string
    password:string
    rememberme?:boolean
}

export interface Signup{
    first_name:string
    last_name:string
    email:string
    password:string
    confirmed_password:string
    university:string
    research_fields:Array<string>
}
export interface ProfileForm{
    first_name:string
    last_name:string
    university:string
    research_fields:Array<string>
    tag:Array<string>
}

export interface UserInfo{
    email:string
    first_name:string
    last_name:string
    university:string
    research_fields:Array<ResearchFieldsItem>|Array<string>
    tags:Array<string>
    access_token:string
    favourite:Array<string>
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


export interface UniversityStrength{
    research_field:string
    score:number
}
export interface UniversityStrengthMap{
    [key:string]:Array<UniversityStrength>
}

export interface MatcherParams{
    research_fields:Array<string>
    tags:Array<string>
}


export interface WeightItem{
    weight:number
    name:string
}

export interface QueryTender{
    'URL':string
    'Title':string
    'Publish Date':string
    'GO ID':string
    'tags':string
    'division':string
    'Close Date & Time':string
    'Location':string
    'Agency':string
}
export type QueryType = 'latest' | 'expiring' | 'hot' | 'none'

export interface UserAction{
    type:number
    payload:string
}