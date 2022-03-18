/**
 * User profile settings
 */
import React, {useEffect, useState, useMemo} from 'react'
import type {ReactElement} from 'react'
import { useNavigate } from 'react-router-dom'


import { Form, Input, Select, Button, Spin, Row, Col } from 'antd'
import {LoadingOutlined} from '@ant-design/icons'


import { useAppSelector } from '../../store'
import { researchFields } from '../../utils/data/researchFields'
import { universities } from '../../utils/data/universities'

import './index.css'


const { Option, OptGroup } = Select
export default function Profile():JSX.Element{
	const [isSubmitting, setIsSubmitting] = useState(false)
	const [selectedResearchFields, setSelectedResearchFields] = useState([])
	const userInfo = useAppSelector((state)=>state.user)
	const navigate = useNavigate()

	const [form] = Form.useForm()

	useEffect(()=>{
		if(!userInfo.access_token){
			navigate('/')
		}else{
			form.setFieldsValue({
				'firstName':userInfo.firstName || '', 
				'lastName':userInfo.lastName || '',
				'university':userInfo.university || '',
				'researchFields':userInfo.researchFileds.map(e=>{return e.field}) || []})
		}
	})

	// update sub research fields when selected reseach fields changed 
	useEffect(()=>{
		const oldSubResearchFields = form.getFieldValue('subResearchFields')
		let newSubResearchFields:Array<string> = []
		console.log(oldSubResearchFields, selectedResearchFields)
		if(selectedResearchFields?.length !== 0 && oldSubResearchFields?.length !== 0){
			for(const k of selectedResearchFields){	
				newSubResearchFields = newSubResearchFields.concat(oldSubResearchFields.filter((e:string)=>{
					return researchFields[k].subField.includes(e)}))
			}
		}
		form.setFieldsValue({'researchFields':selectedResearchFields, 'subResearchFields':newSubResearchFields})
	}, [selectedResearchFields])


	const handleTriggerSubmitForm = ()=>{
		console.log(form.getFieldValue('subResearchFields'))
		
		form.submit()
	}
	const handleSubmitForm = ()=>{
		console.log('handleSubmitForm')
	}
	const handleSubmitFormFailed = ()=>{
		console.log('handleSubmitFormFailed')
	}

	const handleResearchFieldsChange = ()=>{
		setSelectedResearchFields(form.getFieldValue('researchFields').slice(0, 3))
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
		<div className='profile-page'>
			<div className='profile-container'>
				<div className='profile-title'>Profile</div>
				<Form  
					requiredMark={false}
					autoComplete = "off"
					size='large' 
					className='profile-form'
					form={form} 
					labelCol={{span:5}}
					validateTrigger='onBlur'
					onFinish={handleSubmitForm}
					onFinishFailed={handleSubmitFormFailed}
					colon={false}
				>
					<Form.Item  label='First Name' name='firstName'
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
					
					<Form.Item label='Last Name'  name='lastName' 
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
				

				
					<Form.Item label='Research Fields'  className='profile-fields' name='researchFields' extra='At most three fields' validateTrigger='onChange'
						rules={[
							{required:true, 
								message:'Please select your reasearch fields'
							},
							({ getFieldValue }) => ({
								validator(_, value) {		
									if(value.length === 0){
										return Promise.reject()
									}
									return Promise.resolve()
								},
							})
						]}
					>
						<Select mode='multiple' showArrow onChange={handleResearchFieldsChange} >
							{renderResearchFieldsOptions()}	
						</Select>
					</Form.Item>
					<Form.Item label='Subfields' name='subResearchFields' shouldUpdate extra='More specific researching fields can help us to find more suitable opportunities for you!' >
						<Select mode='multiple' showArrow >
							{
								selectedResearchFields.map((e:string)=>{						 
									return (<OptGroup key={e} label={researchFields[e].field}>{
										researchFields[e].subField.map((c:string, i:number)=>{
											return (<Option key={c + i} value={c}>
												{c}
											</Option>)	
										})
									}
									</OptGroup>)
									
								})
							}
						</Select>			
					</Form.Item>
					<Form.Item label='Tags' name='tags' shouldUpdate extra='You can use tags to indicate what area of ​​research you are good at!'>
						<Select mode='tags' open={false} tokenSeparators={[',', ';']}>
							{
								selectedResearchFields.map((e:string)=>{						 
									return (<OptGroup key={e} label={researchFields[e].field}>{
										researchFields[e].subField.map((c:string, i:number)=>{
											return (<Option key={c + i} value={c}>
												{c}
											</Option>)	
										})
									}
									</OptGroup>)
									
								})
							}
						</Select>			
					</Form.Item>
				
				
						

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