import React, {useEffect, useState} from 'react'

import { Spin, Row, Col, List, Tag, message } from 'antd'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faAnglesRight, faThumbsUp, faThumbsDown } from '@fortawesome/free-solid-svg-icons'



import { DonutChart } from '../charts'


import { useAppSelector, useAppDispatch } from '../../store'


import { matchTenderAPI } from '../../api'

import { useCollector } from '../../utils/customHook'
import capitalize from '../../utils/capitalize'
import type {QueryTender, MatcherParams}  from '../../utils/types'

import './index.css'

export default function AIMatch():JSX.Element{
	const [matchResult, setMatchResult] = useState(new Array<QueryTender>())
	const [isAnalyzing, setIsAnalyzing] = useState(true)
	const [ratedTenders, setRatedTenders] = useState(new Array<string>())
	const user = useAppSelector((state)=>state.user)
	useEffect(()=>{
		const fields = new Array<string>()
		for (const e of user.research_fields){
			typeof e === 'string' ? fields.push(e) : fields.push(e.field)
		}
		const params:MatcherParams = {research_fields:fields, tags:user.tags}

		matchTenderAPI(params).then(response=>{
			if(response.data) setMatchResult(response.data)
		}).finally(()=>{
			setIsAnalyzing(false)
		})
	}, [])

	const handleClickRatingBtn = (target:HTMLElement, type:number, id:string)=>{
		console.log(target)
		setRatedTenders([id, ...ratedTenders])
		target.classList.add('active')


		switch(type){
		case 0:
			useCollector({type:4, payload:id})
			break
		case 1:
			useCollector({type:5, payload:id})
		}
        
		message.info('Thanks for your feedback!', 2)
	}



	return (<div className='match-result'>
		{
			isAnalyzing ? 
				<>
					<div style={{padding:'15rem 0', textAlign:'center', height:'80vh'}}>
						<Spin size='default' />
						<div style={{color:'gray', fontSize:'0.8rem', fontWeight:600, marginTop:'0.3rem'}}>Analyzing...</div>
					</div>
				</> : 
				<>
					<div className='match-result-content'>
						<List
							itemLayout='vertical'
							size='large'
							dataSource={matchResult}
							pagination={
								{	simple : true,
									pageSize:5,
									hideOnSinglePage:true
								}
							}
							locale={
								{emptyText:' '}
							}
							renderItem={item=>{
								const tags:string[] = item.tags?.split(' ')
								const divisions:string[]  = item.division?.split('/')
								return <List.Item key={item['GO ID']}>
									<List.Item.Meta 
										title={
											<a href={item['URL']} className='link' 
												onClick={()=>{
													useCollector({type:1, payload:item['GO ID']})
												}}
											>{item['GO ID'] + ' - ' + item['Title']}</a>        
										} 
										description={
											<>
												<Row className='close-date' style={{marginTop:'0.5rem'}}  gutter={6}>
													<Col style={{textAlign:'right'}} span={5}>Close Date & Time:</Col>
													<Col span={18}>{item['Close Date & Time']}</Col>
												</Row>
												<Row className='open-date' style={{marginTop:'0.5rem'}}  gutter={6}>
													<Col style={{textAlign:'right'}} span={5}>Publish Date:</Col>
													<Col span={18}>{item['Publish Date']}</Col>
												</Row>
												<Row className='agency' style={{marginTop:'0.5rem'}}  gutter={6}>
													<Col style={{textAlign:'right'}} span={5}>Agency:</Col>
													<Col span={18}>{item['Agency']}</Col>
												</Row>
												<Row className='location' style={{marginTop:'0.5rem'}}  gutter={6}>
													<Col style={{textAlign:'right'}} span={5}>Location:</Col>
													<Col span={18}>{item['Location']}</Col>
												</Row>
												<Row className='division' style={{marginTop:'0.5rem'}}  gutter={6}>
													<Col style={{textAlign:'right'}} span={5}>Divisions: </Col>
													<Col span={18}>
														{divisions.map((e, i)=>(
																   <Tag color="volcano" key={i}>{capitalize(e)}</Tag>
														))}
								
													</Col>
												</Row>
												<Row className='tags' style={{marginTop:'0.5rem'}}  gutter={6}>
													<Col style={{textAlign:'right'}} span={5}>Keywords: </Col>
													<Col span={18}>
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

												<Row style={{marginTop:'1rem'}} align='middle' justify='end' gutter={6}>
																							
													<Col span={5}>
														<a  className='url' 
															href={item['URL']}
															onClick={()=>{
																useCollector({type:1, payload:item['GO ID']})
															}}
														>
															Read more
															<FontAwesomeIcon style={{marginLeft:'0.5rem'}} icon={faAnglesRight}/>
														</a>
													</Col>
													
												</Row>

												{
													ratedTenders.includes(item['GO ID']) ?
														''
														:
														<Row className='rating' style={{marginTop:'1rem'}} align='middle' justify='center' gutter={24}>
															<Col   onClick={(event)=>{
																handleClickRatingBtn(event.currentTarget, 0, item['GO ID'])
															}} >
                                                        	<FontAwesomeIcon style={{marginRight:'0.25rem'}} icon={faThumbsUp}/>Good
															</Col>
															<Col  onClick={(event)=>{
																handleClickRatingBtn(event.currentTarget, 1, item['GO ID'])
															}}>
                                                        	<FontAwesomeIcon style={{marginRight:'0.3rem'}} icon={faThumbsDown}/>
                                                            Dislike
															</Col>
														</Row>
												}
												
											</>
									
										}
									/>
								</List.Item>
							}
							}
						/>
					</div>
				</>
				
		}
	</div>)
}