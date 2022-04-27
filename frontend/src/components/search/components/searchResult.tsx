import React, {useEffect, useState} from 'react'
import { useSearchParams } from 'react-router-dom'
import { List, Row, Col, Spin, message, Tag} from 'antd'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faAnglesRight, faStar} from '@fortawesome/free-solid-svg-icons'


import { setFavourite } from '../../../store/features/user'
import { useAppSelector, useAppDispatch } from '../../../store'
import {DonutChart} from '../../../components/charts'
import {addUserFavouriteAPI, queryTendersAPI, removeUserFavouriteAPI, getUserFavouriteIdAPI} from '../../../api'
import {useCollector} from '../../../utils/customHook'
import type { QueryTender, QueryType } from '../../../utils/types'
import capitalize from '../../../utils/capitalize'

import SearchBar from './searchBar'
import './searchResult.css'

export default function SearchResult():JSX.Element{
  const [searchParams, setSearchParams] = useSearchParams()
  const [totalResult, setTotalResult] = useState(-1) 
  const [data, setData] = useState(new Array<QueryTender>())
  const [queryKeywords, setQueryKeywords] = useState('All')
  const user = useAppSelector(state=>state.user)
  const dispatch = useAppDispatch()

  useEffect(()=>{
    if(user.access_token){
      getUserFavouriteIdAPI().then(response=>{
        if(response.data){
          dispatch(setFavourite(response.data))
        }
      })
    }
  }, [])

  useEffect(()=>{	
    let encodeQuery = searchParams.get('query') || ''
    const decodeQuery = window.atob(encodeQuery)
    setQueryKeywords(decodeQuery || 'All')
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
      useCollector({type:0, payload:	(encodeQuery ? `keywords=${encodeQuery}&` : '') + 'go_id=' + response.data?.reduce((prev, cur)=>cur['GO ID'] + '/' + prev, '')})
    }).catch(()=>{
      setTotalResult(0)
    })
  }, [searchParams.get('query')])

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
    <div className='search-result'>
      <SearchBar placeholder={`Searched: ${queryKeywords}`}/>
      {
        totalResult === -1 ? 
          <>
            <div style={{padding:'15rem 0', textAlign:'center', height:'80vh'}}>
              <Spin size='default' />
              <div style={{color:'gray', fontSize:'0.8rem', fontWeight:600, marginTop:'0.3rem'}}>Searching...</div>
            </div>
          </> : 
          <>
            <div className='search-result-info'>Found: <span>{totalResult}</span> results</div>
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
													
                            <Col  className='favourite-btn' >
                              {
                                renderFavouriteBtn(item['GO ID'])
                              }
                            </Col>
													
			
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