import React, {useEffect, useState} from 'react'
import { useSearchParams } from 'react-router-dom'
import { List, Tag, Row, Col, Spin} from 'antd'


import SearchBar from './searchBar'
import './searchResult.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faAnglesRight, faLink} from '@fortawesome/free-solid-svg-icons'
import {DonutChart} from '../../../components/charts'
import {queryTendersAPI} from '../../../api'
import type { QueryTender, QueryType } from '../../../utils/types'

export default function SearchResult():JSX.Element{
	const [searchParams, setSearchParams] = useSearchParams()
	const [totalResult, setTotalResult] = useState(-1) 
	const [data, setData] = useState(new Array<QueryTender>())
	const [queryKeywords, setQueryKeywords] = useState('Enter your keywords')
	useEffect(()=>{
		let encodeQuery = searchParams.get('query') || ''
		const decodeQuery = window.atob(encodeQuery)

		setQueryKeywords(decodeQuery || 'Enter your keywords')

		let type:QueryType = 'none'
		switch (decodeQuery){
		case 'latest':
		case 'hot':
		case 'expiring':
			type = decodeQuery
			encodeQuery = ''
			break
		}

		queryTendersAPI(type, encodeQuery).then((response)=>{
			setTotalResult(response.data?.length || 0)
			setData(response.data as Array<QueryTender>)
		}).catch(()=>{
			setTotalResult(0)
		})
	}, [searchParams.get('query')])

	return <>
		<div className='search-result'>
			<SearchBar placeholder={`Searched: ${queryKeywords}`}/>
			{
				totalResult === -1 ? 
					<>
						<div style={{padding:'15rem 0', textAlign:'center', height:'80vh'}}>
							<Spin size='large' />
							<div style={{color:'gray', marginTop:'0.3rem'}}>Searching...</div>
						</div>

					</> : 
					<>
						<div className='search-result-info'>About <span>{totalResult}</span> results</div>
						<div className='search-result-content'>
							<List
								itemLayout='vertical'
								size='large'
								dataSource={data}
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
									const tags:Array<string> = item.tags?.split(' ')
									return <List.Item key={item['GO ID']}>
										<List.Item.Meta 
											title={
												<a href={item['URL']} className='link' >{item['GO ID'] + ' - ' + item['Title']}   </a>
        
											} 
											description={
												<>
													<Row className='close-date' style={{marginTop:'0.5rem'}}  gutter={6}>
														<Col style={{textAlign:'right'}} span={5}>Close Date & Time:</Col>
														<Col span={15}>{item['Close Date & Time']}</Col>
													</Row>
													<Row className='open-date' style={{marginTop:'0.5rem'}}  gutter={6}>
														<Col style={{textAlign:'right'}} span={5}>Publish Date:</Col>
														<Col span={15}>{item['Publish Date']}</Col>
													</Row>
													<Row className='agency' style={{marginTop:'0.5rem'}}  gutter={6}>
														<Col style={{textAlign:'right'}} span={5}>Agency:</Col>
														<Col span={15}>{item['Agency']}</Col>
													</Row>
													<Row className='location' style={{marginTop:'0.5rem'}}  gutter={6}>
														<Col style={{textAlign:'right'}} span={5}>Location:</Col>
														<Col span={15}>{item['Location']}</Col>
													</Row>
													<Row className='tags' style={{marginTop:'0.5rem'}}  gutter={6}>
														<Col style={{textAlign:'right'}} span={5}>Keywords: </Col>
														<Col span={15}>
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
															href={item['URL']}>
															Read more
															<FontAwesomeIcon style={{marginLeft:'0.5rem'}} icon={faAnglesRight}/>
														</a>
													</Row>
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
		</div>
	</>
}