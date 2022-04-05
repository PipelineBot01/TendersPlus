
import './index.css'
import { Card, Row, Col } from 'antd'
import {Link, useNavigate} from 'react-router-dom'
import {DoubleRightOutlined} from '@ant-design/icons'
import { useEffect, useState } from 'react'
import {DonutChart} from '../charts'
import {  queryTendersCountAPI, queryTendersAPI } from '../../api'
import type {QueryTender} from '../../utils/types'
import  {useCollector} from '../../utils/customHook'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faAnglesRight } from '@fortawesome/free-solid-svg-icons'

export default function Discovery():JSX.Element{
	const navigate = useNavigate()
	const [totalNumberTenders, setTotalNumberTenders] = useState(0)
	const [latestTenders, setLatestTenders] = useState(new Array<QueryTender>())
	const [expiringTenders, setExpiringTenders] = useState(new Array<QueryTender>())
	const [hotTenders, setHotTenders] = useState(new Array<QueryTender>())
	useEffect(()=>{
		queryTendersCountAPI().then((response)=>{
			if(response.data){
				setTotalNumberTenders(response.data)
			}
		})
		queryTendersAPI('latest', 3).then((response)=>{
			if(response.data){
				setLatestTenders(response.data)
			}
		})
		queryTendersAPI('expiring', 3).then((response)=>{
			if(response.data){
				setExpiringTenders(response.data)
			}
		})
		queryTendersAPI('hot', 3).then((response)=>{
			if(response.data){
				setHotTenders(response.data)
			}
		})
	}, [])
	const renderTenders = (tenders:QueryTender[])=>{
		return tenders.map(item=>{
			const tags:Array<string> = item.tags?.split(' ')
			return (
				<Card
					type='inner' 
					style={{margin:'1rem 0'}} title={<>
						<span style={{color:'#4b4b4b'}}>{`${item['GO ID']} - ${item['Title']}`}</span>
		  		</>}>
					<Row className='close-date' style={{marginTop:'0.5rem'}}  gutter={6}>
						<Col style={{textAlign:'right'}} span={10}>Close Date & Time:</Col>
						<Col span={14}>{item['Close Date & Time']}</Col>
					</Row>
					<Row className='open-date' style={{marginTop:'0.5rem'}}  gutter={6}>
						<Col style={{textAlign:'right'}} span={10}>Publish Date:</Col>
						<Col span={14}>{item['Publish Date']}</Col>
					</Row>
					<Row className='agency' style={{marginTop:'0.5rem'}}  gutter={6}>
						<Col style={{textAlign:'right'}} span={10}>Agency:</Col>
						<Col span={14}>{item['Agency']}</Col>
					</Row>
					<Row className='location' style={{marginTop:'0.5rem'}}  gutter={6}>
						<Col style={{textAlign:'right'}} span={10}>Location:</Col>
						<Col span={14}>{item['Location']}</Col>
					</Row>
					<Row className='tags' style={{marginTop:'0.5rem'}}  gutter={6}>
						<Col style={{textAlign:'right'}} span={10}>Keywords: </Col>
						<Col span={14}>
							{tags.map((e, i)=>(<span key={i} className='item'>
								<DonutChart 
									width={12} 
									height={12}
									backgroundColor='#EDEEEE' 
									chartColor='#FFC736'
									percentage={(18 - i) / 15}
									strokeWidth={2}
								/>
								{e}
							</span>))}	
						</Col>
					</Row>

					<Row style={{marginTop:'1rem'}} justify='end' gutter={6}>
						<a  className='url' 
							href={item['URL']}
							onClick={()=>{
								useCollector({type:1, payload:item['URL']})
							}}
						>
							Read more
							<FontAwesomeIcon style={{marginLeft:'0.5rem'}} icon={faAnglesRight}/>
						</a>
					</Row>
				</Card>
			)
		})
	}

	
	return(<>
		<div className="discovery">
			<Row justify='space-between' align="bottom" >
				<Col span={ 7}>
					<div className="title">
                    Find a grant opportunity
					</div>
				</Col>
				<Col>
					<div className='subtitle' onClick={()=>{
						useCollector({type:1, payload:'/search'})
						navigate('/search')
						
					}}>
					All <span>{totalNumberTenders}</span> Opened
					</div>
					
				</Col>
			</Row>
			
			<div className="tenders">
				<Row gutter={12}>
					<Col span={8}>
						<Card 
							className='tenders-card' 
							title='Latest' 
							headStyle={{
								fontSize:'1.2rem',
								color:'#585959'
							}}
							extra={<Link 
								to='/search?query=bGF0ZXN0'
								style={{
									fontWeight:700,
									color:'#228e64',
					
									fontSize:'0.8rem',
								}}
								onClick={()=>{
									useCollector({type:1, payload:'/search/latest'})
								}}
							>READ MORE</Link>}
                        
						>
							{renderTenders(latestTenders)}
						</Card>
					</Col>
                    
					<Col span={8}>
						<Card className='tenders-card'  title='Hot'
                        
							headStyle={{
								fontSize:'1.2rem',
								color:'#585959'
							}}
							extra={<Link 
								to='/search?query=aG90'
								style={{
									fontWeight:700,
									color:'#228e64',
									fontSize:'0.8rem',
								}}
								onClick={()=>{
									useCollector({type:1, payload:'/search/hot'})
								}}
							>READ MORE</Link>}
						>
							{renderTenders(hotTenders)}
						</Card>
					</Col>
                    
					<Col span={8}>
						<Card 	className='tenders-card'  title='Expiring Soon'
							headStyle={{
								fontSize:'1.2rem',
								color:'#585959'
							}}
							extra={<Link 
								to='/search?query=ZXhwaXJpbmc='
								style={{
									fontWeight:700,
									color:'#228e64',
									fontSize:'0.8rem',
								}}
								onClick={()=>{
									useCollector({type:1, payload:'/search/expring'})
								}}
							>READ MORE</Link>}>
							{renderTenders(expiringTenders)}
						</Card>
					</Col>

				</Row>
				
				

			</div>
		</div>
	</>)
}