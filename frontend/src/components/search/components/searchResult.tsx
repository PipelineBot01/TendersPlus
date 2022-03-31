import React, {useEffect, useState} from 'react'
import { useSearchParams } from 'react-router-dom'
import { List, Tag, Row, Col} from 'antd'

import type { WeightItem } from '../../../utils/types'
import SearchBar from './searchBar'
import './searchResult.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faAngleRight} from '@fortawesome/free-solid-svg-icons'
import {DonutChart} from '../../../components/charts'
import {queryTendersAPI} from '../../../api'
import type { QueryTender } from '../../../utils/types'
//  Read More  <FontAwesomeIcon icon={faAngleRight} /> 
export default function SearchResult():JSX.Element{
	const [searchParams, setSearchParams] = useSearchParams()
	const [totalResult, setTotalResult] = useState(10) 
	const [data, setData] = useState(new Array<QueryTender>())

	useEffect(()=>{
		const query = searchParams.get('query') || ''
		queryTendersAPI(query).then((response)=>{
			setTotalResult(response.data?.length || 0)
			setData(response.data as Array<QueryTender>)
		})
	}, [searchParams.get('query')])

	return <>
		<div className='search-result'>

			<SearchBar placeholder='Enter your keywords'/>
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
						return <List.Item key={item.id}>
							<List.Item.Meta 
								title={
									<a href={item.url} className='link' >{item.title}   </a>
        
								} 
								description={
									<>
										<Row className='open-date' style={{marginTop:'0.5rem'}}  gutter={6}>
											<Col style={{textAlign:'center'}} span={3}>Open Date:</Col>
									
											<Col span={14}>{item.open_date}</Col>
										</Row>

										<Row className='close-date' style={{marginTop:'0.5rem'}}  gutter={6}>
											<Col style={{textAlign:'center'}} span={3}>Close Date:</Col>
											
											<Col span={14}>{item.close_date}</Col>
										</Row>
										

											
										<Row className='tags' style={{marginTop:'0.5rem'}}  gutter={6}>
										
											<Col style={{textAlign:'center'}} span={3}>Keywords: </Col>
												
											<Col span={20}>
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
									</>
									
								}
							/>
					
						
						</List.Item>
					}
					}
				/>
                    
			
			</div>
		</div>
    
	</>
}