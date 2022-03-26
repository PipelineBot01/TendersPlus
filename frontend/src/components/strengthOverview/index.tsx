import React, {useEffect, useState} from "react"
import { Radar, RadarConfig } from '@ant-design/plots'
import {Row, Col, Card} from'antd'

import {strengthOverviewAPI} from '../../api'
import type {UniversityStrength} from '../../utils/types'

import './index.css'
export default function StrengthOverview():JSX.Element{
	const [data, setData] = useState(new Array<UniversityStrength>())
	// const fetchData = (university:string)=>{
	// 	strengthOverviewAPI(university).then((response)=>{
	// 		if(response.data){
	// 			setData(response.data)
	// 		}
	// 	})
	// }
	// useEffect(()=>{fetchData()}, [])
	const config:RadarConfig = {
		data,
		xField:'field',
		yField:'score'
	}
	return <>
		<div className="strength-overview">
			<Row>
				<Col className="title">Universities' strength overview</Col>
			</Row>
			<Row>
				<div className="name"></div>
			</Row>
		</div>
    
	</>
}