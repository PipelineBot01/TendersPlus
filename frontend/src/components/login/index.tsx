import React, {useState} from 'react'
import {Row, Col, Form, Input, Button, Spin, Checkbox, message } from 'antd'
import {LeftOutlined, LoadingOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'

import { useAppDispatch } from '../../store'
import { setUserInfo, type UserState } from '../../store/features/user'

import './index.css'
import Cookies from 'js-cookie'


export default function Header():JSX.Element{
	const navigate = useNavigate()
	const dispatch = useAppDispatch()
	const [form] = Form.useForm()
	const [isSubmitting, setIsSubmitting] = useState(false)

	const handleSubmitForm = (values:any)=>{
		console.log('handleSubmitForm', values)
		message.loading({content:'Landing...', key:'login', duration:0})
		setTimeout(()=>{
			message.destroy('login')
			setIsSubmitting(false)
			const user:UserState = {
				firstName:'Guest',
				lastName:'Anonymous',
				tags:[],
				researchFileds:[],
				rememberme:values?.rememberme,
				avatar:'',
				access_token:'test',
				university:'Australian National University'
			}
			dispatch(setUserInfo(user))
			user.rememberme ? Cookies.set('access_token', user.access_token, {expires:7}) : Cookies.set('access_token', user.access_token)
			navigate('/')
			
			message.success('Welcome back, ' + user.firstName, 1.5)
		}, 1000)
	
	}
	const handleTriggerSubmitForm = ()=>{
		setIsSubmitting(true)
		form.submit()
	}

	return <>
		<Row justify='center' align='middle' >
			<Col className='gallery' span={14}>
                
			</Col>
			<Col className='login-page' span={10}>
				<div className='btn-to-home' onClick={()=>{navigate('/')}}>
					<LeftOutlined style={{margin:0, padding:0}}/> Back
				</div>
				<div className='login-container'>
					<div style={{fontSize:'1.8rem', textAlign:'center', marginTop:'1rem', fontWeight:'700'}}>Log in</div>
					<div style={{fontSize:'0.8rem', textAlign:'center', marginBottom:'1rem', fontWeight:'600'}}>xxxx xxx </div>
					<Form  
						requiredMark={false}
					 	size='large' 
					 	className='login-form'
					  	layout='vertical' 
						autoComplete="off"
					  	form={form} 
					  	onFinish={handleSubmitForm}>
						<Row gutter={12} justify='center'>
							<Col span={20}>
								<Form.Item label='Email' name='email' rules={[{required:true, message:'Please enter your email'}]} >
									<Input placeholder='Enter your email' allowClear={true} />
								</Form.Item>
							</Col>
						</Row>
						<Row gutter={12} justify='center'>
							<Col span={20}>
								<Form.Item label='Passowrd' required  name='passowrd' rules={[{required:true, message:'Please enter your password'}]}>
									<Input.Password autoComplete='new-password'  allowClear={true} />
								</Form.Item>
							</Col>
						</Row>

						<Row gutter={12} justify='start' ant-click-animating-without-extra-node='false'>
							<Col span={20} offset={2}>
								 <Form.Item name="rememberme" initialValue={false} valuePropName="checked" style={{marginLeft:'4px'}}>
									<Checkbox >Remember me</Checkbox>
								</Form.Item>
							</Col>
						</Row>	
						
						<Row gutter={12} justify='center' ant-click-animating-without-extra-node='false'>
							<Col span={20}>
								<Button  className='btn-submit' disabled={isSubmitting} onClick={handleTriggerSubmitForm}>
									{ 
										isSubmitting ? <Spin  indicator={<LoadingOutlined style={{color:'white'}}/>} /> : 'Go!'
									}
								</Button>
							</Col>
						</Row>	
					</Form>
				</div>
				

			</Col>
		</Row>
	</>
}