import React from 'react'
import {Route, Routes } from "react-router-dom"
import {Spin, Skeleton} from 'antd'

import Home from './pages/home'
import Search from './components/search'
import Discovery from './components/discovery'
import StrengthOverview from './components/strengthOverview'

const Login = React.lazy(()=>import('./pages/login'))
const Signup = React.lazy(()=>import('./pages/signup'))
const Profile = React.lazy(()=>import('./components/profile'))
const Dashboard = React.lazy(()=>import('./pages/dashboard'))
const Chatty = React.lazy(()=>import('./components/chatty'))


export default function App() :JSX.Element{
	return (
		<>
			<Routes>
				<Route path='/' element={<Home/>}>
					<Route index element={
						<>
							<Search/>
							<Discovery/>
							<StrengthOverview/>
						</>
					}/>
				</Route>
				<Route path='/login' element={
					<React.Suspense fallback={<div><Spin></Spin></div>}>
						<Login/>
					</React.Suspense>
				}/>
				<Route path='/signup' element={
					<React.Suspense fallback={<div><Spin></Spin></div>}>
						<Signup/>
					</React.Suspense>
				}/>
				<Route path='/dashboard'element={
					<React.Suspense fallback={<div><Spin></Spin></div>}>
						<Dashboard/>
					</React.Suspense>
					
				} >
					<Route  path='search' element={
						<>
							<Skeleton style={{margin:'2rem'}} loading={true} />
						</>
					}/>
					<Route  path='profile' element={
						<>
							<React.Suspense fallback={<div><Spin></Spin></div>}>
								<Profile/>
							</React.Suspense>
					
						</>
					}/>
					<Route  path='favorites' element={
						<>
							<Skeleton style={{margin:'2rem'}} loading={true} />
						</>
					}/>
					<Route  path='analysis' element={
						<>
							<Spin style={{width:'100%'}} size="large"></Spin>
							{/* <Skeleton  style={{margin:'2rem'}} loading={true} /> */}
						</>
					}/>
					<Route  path='chatty' element={
						<>
							<React.Suspense fallback={<div><Spin></Spin></div>}>
								<Chatty/>
							</React.Suspense>
							
						</>
					}/>
				</Route>

	
			</Routes>
		
		</>
	)
}

