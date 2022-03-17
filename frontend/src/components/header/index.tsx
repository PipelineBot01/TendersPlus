import React, {useState, useEffect} from 'react'
import { useNavigate } from 'react-router-dom'
import {BellOutlined, SettingOutlined, ExportOutlined, MenuOutlined} from '@ant-design/icons'
import {Badge, Menu, Dropdown } from 'antd'
import Cookie from 'js-cookie'

import { setUserInfo, UserState, setAccessToken } from '../../store/features/user'
import { useAppSelector, useAppDispatch } from '../../store'
import { getUserInfoAPI } from '../../api'

import './index.css'
export default function Header():JSX.Element{
	const navigate = useNavigate()
	const [hasLogined, setHasLogined] = useState(true)
	const dispatch  = useAppDispatch()
	const userInfo = useAppSelector((state)=>state.user)
	const tokenFromStore = userInfo.access_token


	// fetch data
	useEffect(()=>{ 
		const tokenFromCookie  = Cookie.get('access_token')
		if (tokenFromCookie && (!tokenFromStore || tokenFromCookie !== tokenFromStore)){
			// fetch latest user info
			getUserInfoAPI().then((response)=>{
				if(response.code === '200'){
					const userInfo = response.data as UserState
					userInfo.access_token = tokenFromCookie 
					userInfo.rememberme = true
					dispatch(setUserInfo(userInfo))
					setHasLogined(true)
				}
			}).catch(()=>{
				Cookie.remove('access_token')
			})
		}else if (!tokenFromCookie && tokenFromStore){
			// currently user logined without rememberme
			setHasLogined(true)
		
		}
	}, [tokenFromStore])

	const handleLogout = ()=>{
		console.log('logout!')
		Cookie.remove('access_token')
		dispatch(setAccessToken(''))
		setHasLogined(false)
		navigate('/')
	}
	const handleRender = ()=>{
		const menu = (<Menu>
			<Menu.Item key='0'>
				<div className='btn-notice' style={{fontWeight:500}} onClick={()=>{navigate('/message')}}>
					<BellOutlined  style={{marginRight:'0.5rem'}}/> Notices
				</div>
			</Menu.Item>
			<Menu.Item key='1'>
				<div className='btn-settings' style={{fontWeight:500}} onClick={()=>{navigate('/profile')}}>
					<SettingOutlined style={{marginRight:'0.5rem'}} /> Settings
				</div>
			</Menu.Item>
			<Menu.Item key='2'>
				<div className='btn-logout'  style={{fontWeight:500}}
					onClick={(e)=>{
						e.preventDefault()
						handleLogout()}}>
					<ExportOutlined style={{marginRight:'0.5rem'}} /> Log out
				</div>
			</Menu.Item>
		</Menu>)

		if (hasLogined){
			return <>
				<div className='username'>
					Hi, {userInfo.firstName}
				</div>
				<Dropdown 
					className='btn-dropdown' 
				 	placement='bottomCenter'
				 	overlay={menu} 
				 	trigger={['hover']}>
					<button>
						<MenuOutlined />
					</button>
				</Dropdown>
	
			</>
		}
		return <>
			<div className = 'btn-login' onClick={()=>{navigate('/login')}}>
					Log in
			</div>
			<div className = 'btn-signup' onClick={()=>{navigate('/signup')}}>
				<BellOutlined style={{paddingRight:'0.4rem'}} />
					Sign up
			</div>
		</>
	}

	return (
		<header>
			<nav>
				<div className='brand' onClick={()=>{navigate('/')}}>
					Tenders+
				</div>
				<div className='btn-group'>
					{handleRender()}
				</div>
			
			</nav>
		</header>
	)
}