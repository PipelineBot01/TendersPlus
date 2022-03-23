import React from 'react'
import {Route, Routes, Outlet } from "react-router-dom"
import {Layout, Spin} from 'antd'

import Header from './components/header'
import Footer from './components/footer'
import Search from './components/search'
import Discovery from './components/discovery'

const Login = React.lazy(()=>import('./pages/login'))
const Signup = React.lazy(()=>import('./pages/signup'))
const Profile = React.lazy(()=>import('./components/profile'))
const Dashboard = React.lazy(()=>import('./pages/dashboard'))

export default function App() :JSX.Element{
	return (
		<>
			<Routes>
				<Route path='/' element={<HomeLayout/>}>
					<Route index element={
						<>
							<Search/>
							<Discovery/>
						</>
					}/>
					<Route path='profile' element={
						<React.Suspense fallback={<div><Spin></Spin></div>}>
							<Profile/>
						</React.Suspense>
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
					<Route  path='research' element={
						<>
							<Search/>
						</>
					}/>
				</Route>

	
			</Routes>
		
		</>
	)
}

function HomeLayout ():JSX.Element{
	// we fetch user in header component
	return <>
		<Header/>
		<Outlet/>
		<Footer/>
	</>
}


