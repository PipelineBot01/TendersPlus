import React from 'react'
import {Route, Routes, Outlet } from "react-router-dom"

import Header from './components/header'
import Footer from './components/footer'
import Search from './components/search'
import Discovery from './components/discovery'

const Login = React.lazy(()=>import('./components/login'))
const Signup = React.lazy(()=>import('./components/signup'))
const Profile = React.lazy(()=>import('./components/profile'))

export default function App() :JSX.Element{
	return (
		<>
			<Routes>
				<Route path='/' element={<BasicLayout/>}>
					<Route index element={
						<>
							<Search/>
							<Discovery/>
						</>
					}/>
					<Route path='profile' element={
						<React.Suspense fallback={<div>Loading...</div>}>
							<Profile/>
						</React.Suspense>
					}/>
				</Route>
				<Route path='/login' element={
					<React.Suspense fallback={<div>Loading...</div>}>
						<Login/>
					</React.Suspense>
				}/>
				<Route path='/signup' element={
					<React.Suspense fallback={<div>Loading...</div>}>
						<Signup/>
					</React.Suspense>
				}/>
			</Routes>
		
		</>
	)
}

function BasicLayout ():JSX.Element{
	// we fetch user in header component
	return <>
		<Header/>
		<Outlet/>
		<Footer/>
	</>
}


