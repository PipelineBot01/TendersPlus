import React, {useState, useEffect} from 'react'
import {Row, Col, Card, Avatar, Tag, Divider, Spin } from 'antd'
import { matchResearcherAPI } from '../../api'
import { useAppSelector } from '../../store'
import type { MatcherParams } from '../../utils/types'
import capitalize from '../../utils/capitalize'
import './index.css'
export default function Chatty():JSX.Element{
  const userInfo = useAppSelector(state=>state.user)
  const [researchers, setResearchers] = useState(new Array<any>())
  useEffect(()=>{
    console.log('chatty', userInfo)
    const data:MatcherParams = {
      research_fields:userInfo.research_fields.map(e=>{ 
        if(typeof e === 'object'){
          return e.field
        }else{
          return  e
        }}),
      tags:userInfo.tags
    }
    matchResearcherAPI(data).then((response)=>{
      console.log(response.data)
      setResearchers(response.data)
    })
  }, [])
  return <>
    <Row className='chatty-researcher'  justify='center' align='top' gutter={12}>
      {
        researchers.length > 0 ? researchers.map((e, index)=>{
          return <Col span={12} key={index}>
            <Card style={{height:'18rem', marginBottom:'0.5rem'}} >
              <Card.Meta
                avatar={
                  <Avatar>{e?.name?.slice(0, 1)}</Avatar>}
                title={e?.name}
                description={<>
                  <div className='email' style={{fontWeight:500}}>{e?.email || e.name.replace(' ', '').toLowerCase() + '@uc.au'}</div>
                  <div className='university'>University of Canberra</div>
                  <Divider style={{margin:'0.8rem 0'}}/>
                  <div className='research_fields'>
                    {e?.division?.slice(0, 3).map((e2:any, index2:any)=>{
                      return <Tag style={{margin:'0.2rem'}} color='volcano' key={index2}>{ capitalize(e2)}</Tag>
                    })}
                  </div>
                  <div className='tags' style={{marginTop:'0.5rem'}}>
                    {e?.tag?.slice(0, 6).map((e2:any, index2:any)=>{
                      return <Tag style={{margin:'0.2rem', borderRadius:'2rem'}} key={index2}>{ capitalize(e2)}</Tag>
                    })}
                  </div>
                </>}
              />
            </Card>
          </Col>
        }) :	<>
          <Spin style={{width:'100%'}} ></Spin>
          <div style={{fontWeight:600, fontSize:'0.8rem', color:'gray', margin:'0.3rem'}}>Analyzing...</div>
        </>
      }
    </Row>
  </>
}