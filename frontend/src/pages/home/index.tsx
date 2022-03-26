import React from "react"
import {Outlet } from "react-router-dom"
import Header from '../../components/header'
import Footer from '../../components/footer'


export default function Home():JSX.Element{
	return <>
    	<Header/>
		<Outlet/>
		<Footer/>
	</>
}