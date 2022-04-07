import React, { useEffect, useState } from 'react'
import { Row, Col, List, message } from 'antd'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faAnglesRight, faStar} from '@fortawesome/free-solid-svg-icons'

import { DonutChart } from '../charts'

import { useAppSelector, useAppDispatch } from '../../store'
import { setFavourite } from '../../store/features/user'

import { getUserFavouriteAPI, removeUserFavouriteAPI, addUserFavouriteAPI } from '../../api'

import type { QueryTender } from '../../utils/types'
import { useCollector } from '../../utils/customHook'

import './index.css'

export default function Favourite():JSX.Element{
	const user = useAppSelector(state=>state.user)
	const dispatch = useAppDispatch()
	const [data, setData] = useState(new Array<QueryTender>())
	useEffect(()=>{
		getUserFavouriteAPI().then((response)=>{
			if(response.data){
				setData(response.data)
			}
		})
	}, [user.favourite])

	const handleClickFavouriteBtn = (type:string, id:string)=>{
		const newUserFavourite = user.favourite.slice()
		if (type === 'to-remove'){
			useCollector({type:3, payload:id})
			message.warn('Cancel Favorite', 1)
			const index = newUserFavourite.indexOf(id)
			if(index !== -1){
				newUserFavourite.splice(index, 1)
			}
			removeUserFavouriteAPI(id)
		}else{
			useCollector({type:2, payload:id})
			message.success('Add Favorite', 1)
			newUserFavourite.push(id)
			addUserFavouriteAPI(id)
		}
		dispatch(setFavourite(newUserFavourite))
	}

	const renderFavouriteBtn = (id:string)=>{
		if(user.access_token){
			const className = user.favourite.includes(id) ? 'to-remove' : ''
			return	<FontAwesomeIcon className={className} onClick={()=>{handleClickFavouriteBtn(className, id)}}  icon={faStar}/>
		}
	}
	return <>
		<div className='favourite-title'>My Favourite Tenders:</div>
    	<div className='favourite-content'>
			<List
				itemLayout='vertical'
				size='large'
				dataSource={data}
				pagination={
					{	simple : true,
						pageSize:4,
						hideOnSinglePage:true
					}
				}
				renderItem={item=>{
					const tags:Array<string> = item.tags?.split(' ')
					return <List.Item key={item['GO ID']}>
						<List.Item.Meta 
							title={
								<a href={item['URL']} className='link' 
									onClick={()=>{
										useCollector({type:1, payload:item['URL']})
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
													
										<Col  className='favourite-btn' >
											{
												renderFavouriteBtn(item['GO ID'])
											}
										</Col>
													
													
										<Col span={5}>
											<a  className='url' 
												href={item['URL']}
												onClick={()=>{
													useCollector({type:1, payload:item['URL']})
												}}
											>
															Read more
												<FontAwesomeIcon style={{marginLeft:'0.5rem'}} icon={faAnglesRight}/>
											</a>
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
	</>
}