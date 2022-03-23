import React, {useState, useEffect} from 'react'
import { useNavigate } from 'react-router-dom'
import {BellOutlined, MenuOutlined} from '@ant-design/icons'

import Cookies from 'js-cookie'

import { setUserInfo, UserState } from '../../store/features/user'
import { useAppSelector, useAppDispatch } from '../../store'
import { getUserInfoAPI } from '../../api'

import './index.css'
import { P } from '@antv/g2plot'
export default function Header():JSX.Element{
	const navigate = useNavigate()
	const dispatch  = useAppDispatch()
	const [headerStatus, setHeaderStatus] = useState('pending')
	const userInfo = useAppSelector((state)=>state.user)



	// fetch data
	useEffect(()=>{
		const tokenFromStore = userInfo.access_token
		const tokenFromCookie  = Cookies.get('access_token')
		if (tokenFromCookie && (!tokenFromStore || tokenFromCookie !== tokenFromStore)){
			// fetch latest user info
			getUserInfoAPI().then((response)=>{
				if(response.data){
					setHeaderStatus('resolve')
					const userInfo = response.data as UserState
					userInfo.access_token = tokenFromCookie 
					userInfo.rememberme = true
					dispatch(setUserInfo(userInfo))
					
				}
			}).catch((error)=>{
				setHeaderStatus('reject')
				console.log('error', error)
				Cookies.remove('access_token')
				
			})
		}else if (!tokenFromCookie){
			setHeaderStatus('reject')
		}else if (tokenFromCookie === tokenFromStore){
			setHeaderStatus('resolve')
		}
	})


	const renderHeaderBtn = ()=>{
		if(headerStatus === 'resolve'){
			return <>
				<div className='username'>
					{userInfo.first_name}
				</div>
				<button className='btn-dashboard' onClick={()=>{
					navigate('/dashboard')
				}}>
					<MenuOutlined />
				</button>
			</>  
		}else if (headerStatus === 'reject'){
			return <>
				<div className = 'btn-login' onClick={()=>{navigate('/login')}}>
					Log in
				</div>
				<div className = 'btn-signup' onClick={()=>{navigate('/signup')}}>
					<BellOutlined style={{paddingRight:'0.4rem'}} />
					Sign up
				</div>
			</>
		}else{
			return <></>
		}
			
	}
	return (
		<header>
			<nav>
				<div className='brand' onClick={()=>{navigate('/')}}>
					Tenders+
				</div>
				<div className='btn-group'>
					{renderHeaderBtn()}
				</div>
			
			</nav>
		</header>
	)
}