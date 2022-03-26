import React, {useEffect, useState} from "react"
import { Radar, RadarConfig } from '@ant-design/plots'
import {Row, Col, Card} from'antd'

import {strengthOverviewAPI} from '../../api'
import { universitiesMap } from "../../utils/data/universities"
import {researchFields}from "../../utils/data/researchFields"
import capitalize from "../../utils/capitalize"

import './index.css'
export default function StrengthOverview():JSX.Element{
	const [strengthData, setStrengthData] = useState(new Object())
	useEffect(()=>{	
		strengthOverviewAPI().then((response)=>{
			if(response.data){
				console.log(response.data)
				
				setStrengthData(response.data)
			}
		})
	}, [])



	const renderUniversityStrength = ()=>{
		const render = []
		for(const [key, value] of Object.entries(strengthData)){
			// console.log(key, value)
			const temp_data = (value as Array<any>).map(e=>{
				return {'research_field':capitalize(researchFields[e.research_field].field), 'score':e.score}
			})
			temp_data.sort((a, b)=>{return  a.research_field > b.research_field ? -1 : 0})
			const tempConfig:RadarConfig = {
				data:temp_data,
				xField: 'research_field',
				yField: 'score',
				width:600,
				height:600,
				padding:32,
				meta: {
					score: {
						alias: 'score',
						min: 0,
						max: 10,
					},
				},
		
				// 开启面积
				area: {},
				// 开启辅助点
				point: {
					size: 2.5,
				},
				renderer:'svg',
				color: '#F4A52E',
				lineStyle:{
					lineWidth:3.5
				},
				xAxis:{
			 line: null,
					tickLine: null,
					label:{
						style:{
							fontWeight:'600',
							fontSize:'0.8rem'
						}
					},
			 grid: {
						line: {
							style: {
								lineDash: 8,
							},
						},
		
					},
				},
				yAxis:{
					line: null,
					tickLine: null,
			 grid: {
						line: {
							type: 'line',
					
						},
		
					},
				}
			}
			console.log('temp', tempConfig)
			
			render.push(<Card className="strength-card" title={<div className="name">{universitiesMap[key]}</div>}>
				<Radar {...tempConfig}/>
			</Card>)
			return render
		}
	}


	return <>
		<div className="strength-overview">
			<Row>
				<Col className="title">Universities' strength overview</Col>
			</Row>
			{
				renderUniversityStrength()
			}
		
		</div>
    
	</>
}