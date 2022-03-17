import React, {ReactElement, useEffect, useState} from 'react'
import {Row, Col, Form, Input, Button, Spin, Select} from 'antd'
import {LeftOutlined, LoadingOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import './index.css'
import { useStore } from 'react-redux'
import {researchFields} from '../../utils/data/researchFields'
import { universities } from '../../utils/data/universities'
const { Option, OptGroup } = Select

export default function Header():JSX.Element{
	const navigate = useNavigate()
	const [form] = Form.useForm()
	const [isSubmitting, setIsSubmitting] = useState(false)
	

	const handleSubmitForm = ()=>{console.log('handleSubmitForm')
		setTimeout(()=>{
			setIsSubmitting(false)
		}, 500)
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

	const renderResearchFieldsOptions = ()=>{
		const arr = new Array<ReactElement>()
		for(const key of Object.keys(researchFields)){
			arr.push(<Option key={key} value={key}>{researchFields[key].field}</Option>
			)
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
		<Row justify='center' align='top' >
			<Col className='gallery' span={14}>
                 
			</Col>
			<Col className='signup-page' span={10}>
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
								<Form.Item  label='First Name' name='firstname'
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
							</Col>
							<Col span={10}>
								<Form.Item label='Last Name'  name='lastname' 
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
												return Promise.reject(new Error('Name only formed by no more than 20 letters'))
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
								<Form.Item label='Password'  name='password' extra='At least 8 length'
									rules={[
										 {required:true, 
											message:'Please enter your password',
											whitespace:true,
										},
										({ getFieldValue }) => ({
											validator(_, value) {		
												if (/^\S{8,}$/g.test(value)) {
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
								<Form.Item label='Confirmed Password'  name='confirmPassword' 
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
											message:'Please select your reasearch fields'
										}
									]}
								>
									 <Select mode='multiple' showArrow showSearch>
										{renderUniversitiesOptions()}	
									</Select>
								</Form.Item>
							</Col>
						</Row>

						<Row gutter={12} justify='center'>
							<Col span={20}>
								<Form.Item label='Research Fields'  name='researchFields' extra='At most three fields' validateTrigger='onChange'
									rules={[
										 {required:true, 
											message:'Please select your reasearch fields'
										},
										({ getFieldValue }) => ({
											validator(_, value) {		
												if(value.length === 0){
													return Promise.reject()
												}else if(value.length > 3){
													form.setFieldsValue({'researchFields':value.slice(0, 3)})
												}
												return Promise.resolve()
											},
										})
									]}
								>
									 <Select mode='multiple' showArrow >
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
				

			</Col>
		</Row>
	</>
}