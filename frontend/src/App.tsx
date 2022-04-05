import React from 'react'
import {Route, Routes } from "react-router-dom"
import {Spin} from 'antd'

import BasicLayout from './layout/basicLayout'
import Home from './pages/home'



const SearchResult = React.lazy(()=>import('./components/search/components/searchResult'))
const Login = React.lazy(()=>import('./pages/login'))
const Signup = React.lazy(()=>import('./pages/signup'))
const Profile = React.lazy(()=>import('./components/profile'))
const Dashboard = React.lazy(()=>import('./pages/dashboard'))
const Chatty = React.lazy(()=>import('./components/chatty'))


export default function App() :JSX.Element{
	return (
		<>
			<Routes>
				<Route path='/' element={<BasicLayout/>}>
					<Route index element={<Home/>}></Route>
					<Route path='search' element={
						<React.Suspense fallback={<div><Spin></Spin></div>}>
							<SearchResult/>
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
					<Route  path='search' element={
						<React.Suspense fallback={<Spin style={{width:'100%'}} ></Spin>}>
							<SearchResult/>
						</React.Suspense>
					}/>
					<Route  path='profile' element={
		
						<React.Suspense fallback={<Spin style={{width:'100%'}} ></Spin>}>
							<Profile/>
						</React.Suspense>
					}/>
					<Route  path='favorites' element={
						<>
							<Spin style={{width:'100%'}} ></Spin>
							<div style={{fontWeight:600, fontSize:'0.8rem', color:'gray', margin:'0.3rem'}}>Coming Soon ...</div>
						</>
					}/>
					<Route  path='analysis' element={
						<> 
							<Spin style={{width:'100%'}} ></Spin>
							<div style={{fontWeight:600, fontSize:'0.8rem', color:'gray', margin:'0.3rem'}}>Coming Soon ...</div>
						</>
					}/>
					<Route  path='chatty' element={
						<>
							<React.Suspense fallback={
								<Spin style={{width:'100%'}} ></Spin>
							}>
								<Chatty/>
							</React.Suspense>
						</>
					}/>
				</Route>

	
			</Routes>
		
		</>
	)
}

