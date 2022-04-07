import React, {useState} from 'react'
import {Row, Col, Form, Input, Button, Spin, Checkbox, message } from 'antd'
import {LeftOutlined, LoadingOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import Cookies from 'js-cookie'


import { useAppDispatch } from '../../store'
import { setUserInfo, type UserState } from '../../store/features/user'
import { loginAPI } from '../../api'
import type { Login } from '../../utils/types'
import './index.css'




export default function Header():JSX.Element{
	const navigate = useNavigate()
	const dispatch = useAppDispatch()
	const [form] = Form.useForm()
	const [isSubmitting, setIsSubmitting] = useState(false)

	const handleSubmitForm = (values:Login)=>{
		message.loading({content:'Logging in', key:'login', duration:2})
		loginAPI(values).then((response)=>{
			message.destroy('login')
			if(response.data){
				const data = response.data
				const user : UserState = {
					email:data.email,
					rememberme:values.rememberme || false,
					first_name:data.first_name,
					last_name:data.last_name,
					university:data.university,
					tags:data.tags,
					research_fields:data.research_fields,
					access_token:data.access_token,
					favourite:data.favourite
				}
				user.rememberme ? Cookies.set('access_token', user.access_token, {expires:7}) : Cookies.set('access_token', user.access_token)
				dispatch(setUserInfo(user))
				navigate('/')
				message.success('Welcome back, ' + user.first_name, 3)

			}
		}).catch((error)=>{
			message.destroy('login')
			message.error({content:error.msg, duration:2})
		}).finally(()=>{
			setIsSubmitting(false)
		})
	}
	
	const handleTriggerSubmitForm = ()=>{
		setIsSubmitting(true)
		form.submit()
	}

	return <>
		<Row justify='center' align='middle' >
			<Col className='login-gallery' span={14}>
                
			</Col>
			<Col className='login-page' span={10}>
				<div className='btn-to-home' onClick={()=>{navigate('/')}}>
					<LeftOutlined style={{margin:0, padding:0}}/> Back
				</div>
				<div className='login-container'>
					<div style={{fontSize:'1.8rem', textAlign:'center', marginTop:'1rem', fontWeight:'700'}}>Log in</div>
					<div style={{fontSize:'0.8rem', textAlign:'center', marginBottom:'1rem', color:'grey'}}>Hi, welcome back ~ </div>
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
								<Form.Item label='Passowrd' required  name='password' rules={[{required:true, message:'Please enter your password'}]}>
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