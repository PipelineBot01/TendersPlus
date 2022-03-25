import React, {useState, useEffect} from 'react'
import {Row, Col, Card, Avatar, Tag } from 'antd'
import { matchResearcherAPI } from '../../api'
import { useAppSelector } from '../../store'
import type { MatchResearcher } from '../../utils/types'
import './index.css'
export default function Chatty():JSX.Element{
	const userInfo = useAppSelector(state=>state.user)
	const [researchers, setResearchers] = useState(new Array<any>())

	useEffect(()=>{
		console.log('chatty', userInfo)
		const data:MatchResearcher = {
			research_fields:userInfo.research_fields.map(e=>{ 
				if(typeof e === 'object'){
					return e.field
				}else{
					return e
				}}),
			tags:userInfo.tags
		}
		matchResearcherAPI(data).then((response)=>{
			console.log(response.data)
			setResearchers(response.data)
		})
	}, [])
	return <>
		<Row className='chatty-researcher' justify='center' align='top'>
			{
				researchers.map((e, index)=>{

					return <Col span={8} key={index}>
						<Card style={{ width: 300, marginTop: 16 }} >
							<Card.Meta
								avatar={
									<Avatar>{e?.Name?.slice(0, 1)}</Avatar>}
								title={e?.Name}
								description={<>
									<div className='email'>{e?.Email || e.Name.replace(' ', '').toLowerCase() + '@uc.au'}</div>
									<div className='university'>University of Canberra</div>
									<div className='research_fields'>
										{e?.value?.slice(0, 3).map((e2:any, index2:any)=>{
											return <Tag key={index2}>{e2}</Tag>
										})}
									</div>
								</>}
							/>
						</Card>
					</Col>
				})
			}
		</Row>
	</>
}