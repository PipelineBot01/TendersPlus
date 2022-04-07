import React, {ReactElement, useEffect, useState} from 'react'
import {Row, Col, Form, Input, Button, Spin, Select, message, Result} from 'antd'
import {LeftOutlined, LoadingOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import Cookies from 'js-cookie'

import { useAppDispatch } from '../../store'
import { type UserState, setUserInfo } from '../../store/features/user'
import type { Signup } from '../../utils/types'
import {researchFields} from '../../utils/data/researchFields'
import { universities } from '../../utils/data/universities'
import { signupAPI } from '../../api'
import capitalize from '../../utils/capitalize'
import './index.css'
const { Option, OptGroup } = Select

export default function Header():JSX.Element{
	const navigate = useNavigate()
	const dispatch = useAppDispatch()
	const [form] = Form.useForm()
	const [isSubmitting, setIsSubmitting] = useState(false)
	const [isSucceeded, setIsSucceeded ] = useState(false)

	const handleSubmitForm = (values:Signup)=>{
		console.log(values)
		
		message.loading({content:'Requesting...', key:'signup', duration:1.5})
		
		console.log('handleSubmitForm', values)
		signupAPI(values).then((response)=>{
			message.destroy('signup')
			if(response.data){
				const user:UserState = {
					first_name:response.data.first_name,
					last_name:response.data.last_name,
					university:response.data.university,
					research_fields:response.data.research_fields,
					rememberme:false,
					tags:[],
					email:response.data.email,
					access_token:response.data.access_token,
					favourite:response.data.favourite
				}
				dispatch(setUserInfo(user))
				Cookies.set('access_token', user.access_token)
				setIsSucceeded(true)
			}
		}).catch((response)=>{
			message.destroy('signup')
			message.warn(`Warn: ${(response.msg as string).toLowerCase()}`, 3)
		}).finally(()=>{
			setIsSubmitting(false)
		})
	}
	const handleTriggerSubmitForm = ()=>{
	
		setIsSubmitting(true)
		form.submit()
	}
	const handleSubmitFormFailed = ()=>{
		setTimeout(()=>{
			setIsSubmitting(false)
		}, 1000)
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
	const renderResearchFieldsOptions = ()=>{
		const arr = new Array<ReactElement>()
		for(const key of Object.keys(researchFields)){
			arr.push(<Option key={key} value={key} >{capitalize(researchFields[key].field)}</Option>
			)
		}
		return arr
	}

	const renderSignupForm = ()=>{
		return <>
			<div className='btn-to-home' onClick={()=>{navigate('/')}}>
				<LeftOutlined style={{margin:0, padding:0}}/> Back
			</div>
			<div className='signup-container'>
				<div style={{fontSize:'1.8rem', textAlign:'center', marginTop:'1rem', fontWeight:'700'}}>Create Account</div>
				<div style={{fontSize:'0.8rem', textAlign:'center', marginBottom:'1rem', fontWeight:'600'}}>Join TendersPlus to subscribe the latest grant opportunities </div>
				<Form  
					autoComplete = "off"
					 	size='large' 
					 	className='signup-form'
					  	layout='vertical' 
					  	form={form} 
					validateTrigger='onBlur'
					  	onFinish={handleSubmitForm}
					onFinishFailed={handleSubmitFormFailed}>
					<Row gutter={12} justify='center' align='middle'>
						<Col span={10} >
							<Form.Item  label='First Name' name='first_name'
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
											return Promise.reject(new Error('Name only contains letters'))
										},
									})
								]}>
								<Input placeholder='First name' />
							</Form.Item>
						</Col>
						<Col span={10}>
							<Form.Item label='Last Name'  name='last_name' 
								rules={[
										 {required:true, 
										message:'Please enter your last name',
										whitespace:true,
									},
									({ getFieldValue }) => ({
										validator(_, value) {		
											if (/^[a-zA-Z]{1,20}$/g.test(value)) {
												return Promise.resolve()
											}
											return Promise.reject(new Error('Name only contains letters'))
										},
									})
								]}>
								<Input placeholder='Last name'  />
							</Form.Item>
						</Col>
					</Row>
					<Row gutter={12} justify='center'>
						<Col span={20}>
							<Form.Item label='Email'  name='email'
								rules={[
										 {required:true, 
										message:'Please enter your email address',
										whitespace:true,
										type:'email'
									}
								]} >
								<Input placeholder='Enter your email' allowClear={true} />
							</Form.Item>
						</Col>
					</Row>
					<Row gutter={12} justify='center'>
						<Col span={20}>
							<Form.Item label='Password'  name='password' extra='At least 6 length'
								rules={[
										 {required:true, 
										message:'Please enter your password',
										whitespace:true,
									},
									({ getFieldValue }) => ({
										validator(_, value) {		
											if (/^\S{6,}$/g.test(value)) {
												return Promise.resolve()
											}
											return Promise.reject(new Error('Invaild password'))
										},
									})
								]}
							>
								<Input.Password autoComplete='new-password'  allowClear={true} />
							</Form.Item>
						</Col>
					</Row>
					<Row gutter={12} justify='center'>
						<Col span={20}>
							<Form.Item label='Confirmed Password'  name='confirmed_password' 
								rules={[
										 {required:true, 
										message:'Please confirm your password',
										whitespace:true,
									},
									({ getFieldValue }) => ({
										validator(_, value) {		
											if (value && getFieldValue('password') !== value) {
												return Promise.reject(new Error('Confirmed password is not the same as password'))
											}
											return Promise.resolve()
										},
									})
								]}>
								<Input.Password  autoComplete='new-password'/>
							</Form.Item>
						</Col>
					</Row>

					<Row gutter={12} justify='center'>
						<Col span={20}>
							<Form.Item label='Univeristy'  name='university'
								rules={[
										 {required:true, 
										message:'Please select your university'
									}
								]}
							>
									 <Select showArrow showSearch>
									{renderUniversitiesOptions()}	
								</Select>
							</Form.Item>
						</Col>
					</Row>

					<Row gutter={12} justify='center'>
						<Col span={20}>
							<Form.Item label='Research Fields'  name='research_fields' extra='At most three fields' validateTrigger='onChange'
								rules={[
										 {required:true, 
										message:'Please select your reasearch fields'
									},
									({ getFieldValue }) => ({
										validator(_, value) {		
											console.log(value)
											
											if(value.length === 0){
												return Promise.reject()
											}else if(value.length > 3){
												console.log(123123)
												
												form.setFieldsValue({'research_fields':value.slice(0, 3)})
											}
											return Promise.resolve()
										},
									})
								]}
							>
									 <Select mode='multiple' className='research-fields' showArrow >
									{renderResearchFieldsOptions()}	
								</Select>
							</Form.Item>
						</Col>
					</Row>
						

					<Row gutter={12} justify='center' ant-click-animating-without-extra-node='false'>
						<Col span={20}>
							<Button  className='btn-submit' disabled={isSubmitting} onClick={handleTriggerSubmitForm}>
								{ 
									isSubmitting ? <Spin  indicator={<LoadingOutlined style={{color:'white'}}/>} /> : 'Join!'
								}
							</Button>
						</Col>
					</Row>	
				</Form>
			</div>
		</>
	}
	const renderSignupResult = ()=>{
		return <Result
			status="success"
			title="Successfully sign up the TendersPlus!"
			subTitle="Let's chase your opportunities."
			style={{marginTop:'10rem', height:'100%'}}
			extra={[
				<button className='btn-back' onClick={()=>{navigate('/')}}>
        			Back
				</button>
			]}
		/>
	}
	
	return <>
		<Row justify='center' align='stretch'  style={{minHeight:'100%'}}>
			<Col className='signup-gallery' span={14}>
                 
			</Col>
			<Col className='signup-page' span={10}>
				{
					isSucceeded ? renderSignupResult() : renderSignupForm()
				}
			</Col>
		</Row>
	</>
}