import React, {useState, useEffect} from 'react'

import { matchResearcherAPI } from '../../api'
import { useAppSelector } from '../../store'
import type { MatchResearcher } from '../../utils/types'
export default function Chatty():JSX.Element{
	const userInfo = useAppSelector(state=>state.user)

	useEffect(()=>{
		const research_fields = userInfo.research_fields.map(e=>{ 
			if(typeof e === 'object'){
				return e.field
			}else{
				return e
			}})
		const data:MatchResearcher = {
			research_fields:research_fields,
			tags:userInfo.tags
		}
		matchResearcherAPI(data).then((response)=>{
			console.log(response.data)
		})
	}, [])
	return <>
    123123
	</>
}