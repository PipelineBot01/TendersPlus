import React, {useState, useEffect, useRef} from 'react'
import { Layout, Divider, Menu  } from 'antd'

import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import Cookies from 'js-cookie'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMagnifyingGlass, faStar, faUserTag, faCircleNodes, faComment, faArrowRightFromBracket } from '@fortawesome/free-solid-svg-icons'

import { useAppSelector, useAppDispatch } from '../../store'
import { type UserState, setUserInfo, setAccessToken } from '../../store/features/user'
import { getUserInfoAPI } from '../../api'
import './index.css'

const { Header, Footer, Sider, Content } = Layout

export default function Dashboard():JSX.Element{
	const navigate = useNavigate()
	const location = useLocation()
	const dispatch = useAppDispatch()
	const userInfo = useAppSelector((state)=>state.user)
	const tokenFromStore = userInfo.access_token

	useEffect(()=>{
		const tokenFromCookie  = Cookies.get('access_token')
		if (tokenFromCookie && (!tokenFromStore || tokenFromCookie !== tokenFromStore)){
			// fetch latest user info
			getUserInfoAPI().then((response)=>{
				if(response.data){
					const user:UserState = {
						access_token:tokenFromCookie,
						rememberme:userInfo.rememberme,
						first_name:response.data.first_name,
						last_name:response.data.last_name,
						university:response.data.university,
						research_fields:response.data.research_fields.map(e=>{ 
							if(typeof e === 'object'){
								return e.field
							}else{
								return e
							}})
						,
						tags:response.data.tags,
						email:response.data.email
					}
					console.log('dashboard get user', user)
					
					dispatch(setUserInfo(user))
				}
			}).catch(()=>{
				Cookies.remove('access_token')
				navigate('/')
			})
		}else if (!tokenFromCookie){
			navigate('/')
		}
	}, [])


	const [isCollapsed, setIscollapsed] = useState(false)
	const handleCollapse = ()=>{
		setIscollapsed(!isCollapsed)
	
		
		
	}
	
	const handleLogout  = ()=>{
		console.log('logout!')
		Cookies.remove('access_token')
		dispatch(setAccessToken(''))

		navigate('/')
	}
	return <>
		<Layout hasSider style={{minHeight:'100vh', position:'relative'}} >
			<Sider theme='light' 
			 style={{
					position:'fixed',
					left: 0,
					top: 0,
					bottom: 0,
				}}
				collapsedWidth='5.5rem'
				width='16rem'
				collapsible
				collapsed={isCollapsed}
				onCollapse={handleCollapse}
				className='dashboard-sider'
			>
				<div className='user-info'>
					<span className='avatar'>{userInfo.first_name[0]}</span>
					{ isCollapsed ? null : <span className='user-name' >{userInfo.first_name + ' ' + userInfo.last_name}</span>}
				</div>

				<Menu  className='sider-menu' theme='light' mode='inline' defaultSelectedKeys={[location.pathname.split('/').pop() || '']}>
					<Menu.Item onClick={()=>navigate('/dashboard/search')} key="search" icon={<FontAwesomeIcon icon={faMagnifyingGlass} />}>
						Search
					</Menu.Item>
					<Menu.Item onClick={()=>navigate('/dashboard/favorites')} key="favorites" icon={<FontAwesomeIcon icon={faStar} />}>
						Favorites
					</Menu.Item>
					<Menu.Item key="profile" onClick={()=>navigate('/dashboard/profile')} icon={<FontAwesomeIcon icon={faUserTag} />}>
						Profile
					</Menu.Item>
					<Divider type='horizontal' style={{margin:'1rem 0'}}/>
					<Menu.Item key="analysis" onClick={()=>navigate('/dashboard/analysis')} icon={<FontAwesomeIcon icon={faCircleNodes} />}>
						AI analysis
					</Menu.Item>
					<Menu.Item key="chatty" onClick={()=>navigate('/dashboard/chatty')} icon={<FontAwesomeIcon icon={faComment} />}>
						Chatty
					</Menu.Item>
				</Menu>
			</Sider>
			<Layout  className={`dashboard-container ${isCollapsed}`} >
				<Header className='dashboard-header'>
					<div></div>
					<div className='btn-home' onClick={()=>{navigate('/')}}>
						Tenders+
					</div>
					<div className='btn-logout' onClick={handleLogout}><span style={{marginRight:'0.4rem', fontWeight:600}}></span><FontAwesomeIcon icon={faArrowRightFromBracket} /></div>
				</Header>
				<Content style={{overflowY:'auto'}} className='dashboard-content'><Outlet></Outlet></Content>
			</Layout>
		</Layout>
	</>
}