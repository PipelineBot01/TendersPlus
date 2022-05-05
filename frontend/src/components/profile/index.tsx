/**
 * User profile settings
 */
import React, {useEffect, useState} from 'react'
import type {ReactElement} from 'react'
import { Form, Input, Select, Button, Spin, Row, Col, message, Switch  } from 'antd'
import {LoadingOutlined} from '@ant-design/icons'

import { setUserProfile, setSubscribeStatus } from '../../store/features/user'
import { setUserInfoAPI, subscribeAPI } from '../../api'
import { useAppDispatch, useAppSelector } from '../../store'
import { researchFields } from '../../utils/data/researchFields'
import { universities } from '../../utils/data/universities'
import type { ProfileForm } from '../../utils/types'
import capitalize from '../../utils/capitalize'

import './index.css'

const { Option, OptGroup } = Select
export default function Profile():JSX.Element{
  const user = useAppSelector((state)=>state.user)
  const dispatch = useAppDispatch()
  const [form] = Form.useForm()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [subscribeChecked, setSubscribeChecked] = useState(Boolean(user.subscribe_status))
 

  useEffect(()=>{
    const research_fields_data = user.research_fields.map(e=>{ 
      if(typeof e === 'object'){
        return e.field
      }else{
        return e
      }})
    form.setFieldsValue({
      'first_name':user.first_name, 
      'last_name':user.last_name,
      'university':user.university,
      'research_fields':research_fields_data,
      'tags':user.tags}
    )
    setSubscribeChecked(Boolean(user.subscribe_status))
  }, [user])
	
  const handleTriggerSubmitForm = ()=>{
    setIsSubmitting(true)
    form.submit()
  }
  const handleSubmitForm = (values:ProfileForm)=>{
    console.log('handleSubmitForm', values)
    setUserInfoAPI(values).then(()=>{
      message.success('Updated!', 3)
      dispatch(setUserProfile(values))
    }, error=>{
      console.log('error:', error)
      message.error(error?.msg, 3)
    }).finally(()=>{
      setIsSubmitting(false)
    })

  }
  const handleSubmitFormFailed = ()=>{
    console.log('handleSubmitFormFailed')
    setIsSubmitting(false)
  }
  const handleSubcribeChange = (checked:boolean)=>{
    const status = checked ? 1 : 0
    console.log(status)
    
    subscribeAPI(status).then(()=>{
      message.success('Updated!', 3)
      setSubscribeChecked(checked)
      setSubscribeStatus(status)
    }, error=>{
      message.error(error?.msg, 3)
    })

  }
  const renderResearchFieldsOptions = ()=>{
    const arr = new Array<ReactElement>()
    for(const key of Object.keys(researchFields)){
      arr.push(<Option key={key} value={key}>{capitalize(researchFields[key].field)}</Option>)
    }
    return arr
  }
  const renderUniversitiesOptions = ()=>{
    const arr = new Array<ReactElement>()
    for(const key of Object.keys(universities)){
      arr.push(<OptGroup key={key} label={key}>
        {universities[key].map((e)=>{
          return <Option key={e} value={e}>{e}</Option>
        })}
      </OptGroup>
      )
    }
    return arr
  }

  return <>
    <div className='profile-page'>
      <div className='profile-container'>
        <Form  
          requiredMark={false}
          autoComplete = "off"
          size='large' 
          className='profile-form'
          form={form} 
          labelCol={{span:5}}
          onFinish={handleSubmitForm}
          onFinishFailed={handleSubmitFormFailed}
          colon={false}
        >
          <Form.Item  label='First Name' name='first_name'
            style={{width:'100%'}}
									 rules={[
										 {required:true, 
                message:'Please enter your first name',
                whitespace:true,
              },
              ({ getFieldValue }) => ({
                validator(_, value) {		
                  if (/^[a-zA-Z]{1,20}$/g.test(value)) {
                    return Promise.resolve()
                  }
                  return Promise.reject(new Error('Name only formed by no more than 20 letters'))
                },
              })
            ]}>
            <Input placeholder='First name' />
          </Form.Item>
					
          <Form.Item label='Last Name'  name='last_name' 
            rules={[
              {required:true, 
                message:'Please enter your last name',
                whitespace:true,
              },
              ({ getFieldValue }) => ({
                validator(_, value) {	
										
                  if (!/^[a-zA-Z]{1,20}$/g.test(value)) {
                    return Promise.reject(new Error('Name only formed by no more than 20 letters'))
                  }
								
                  return Promise.resolve()
                },
              })
            ]}>
            <Input placeholder='Last name'  />
          </Form.Item>

          <Form.Item label='Univeristy'  name='university'
            rules={[
              {required:true, 
                message:'Please select your university'
              }
            ]}
          >
            <Select showArrow >
              {renderUniversitiesOptions()}	
            </Select>
          </Form.Item>

          <Form.Item label='Research Fields'  className='profile-fields' name='research_fields' extra='At most three fields' validateTrigger='onChange'
            rules={[
              {required:true, 
                message:'Please select your reasearch fields'
              },
              ({ getFieldValue }) => ({
                validator(_, value) {		
                  console.log('validate 1111')
                  if(value.length === 0){
                    return Promise.reject()
                  }
                  form.setFieldsValue({'research_fields':value.slice(0, 3)})
                  return Promise.resolve()
                },
              })
            ]}
          >
            <Select mode='multiple' showArrow  >
              {renderResearchFieldsOptions()}	
            </Select>
          </Form.Item>
          <Form.Item label='Tags' name='tags' shouldUpdate extra='You can use custom tags to indicate what area of ​​research you are good at! (≤10 tags)'
            validateTrigger='onChange'
            rules={[({ getFieldValue }) => ({
              validator(_, value) {		
                if(value.length > 10){
                  form.setFieldsValue({'tags':value.slice(0, 10)})
                }
                return Promise.resolve()
              },
            })]}>
            <Select mode='tags' open={false} tokenSeparators={[',', ';']}/>
          </Form.Item>
				    <Row style={{alignItems:'center'}}>
            <Col span={5} style={{textAlign:'right', padding:'0 0.5rem', fontWeight:'500', fontSize:'0.9rem'}}  >
                Subscribe
            </Col>
            <Col span={18} style={{marginLeft:'0.2rem'}}>
              <Switch checked={subscribeChecked} onChange={handleSubcribeChange} />
            </Col>
            <Col 
              offset={5} 
              span={19} 
              style={{padding:'0.2rem 0', color:'rgba(0, 0, 0, 0.45)'}}>
              Send me emails once it has recommendation
            </Col>
          </Row>
          <Row justify='center' >
            <Col span={6}>
              <Button  className='btn-submit' disabled={isSubmitting} onClick={handleTriggerSubmitForm}>
                { 
                  isSubmitting ? <Spin  indicator={<LoadingOutlined style={{color:'white'}}/>} /> : 'Save'
                }
              </Button>
            </Col>
          </Row>
      
        </Form>
      </div>

    </div>
  </>
}