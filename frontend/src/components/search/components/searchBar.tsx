
/**
 * The search component has following features:
 * 1. search tenders via tags
 * 2. search tenders via divisions
 */
import React from "react"
import { useNavigate, useLocation } from "react-router-dom"
import {Input } from 'antd'

import './searchBar.css'

import { useCollector } from "../../../utils/customHook"


const { Search } = Input







interface SearchBarProp{
    placeholder:string
}
export default function SearchBar(props:SearchBarProp):JSX.Element{
	const navigate = useNavigate()
	const location = useLocation()

	const onSearch = (value:string)=>{
		let targetPath = '/search'
		useCollector({type:0, payload:value})
		if(location.pathname.includes('dashboard')){
			targetPath = '/dashboard' + targetPath
		}
		if(value){
			targetPath += '?query=' + window.btoa(value)
		}
		console.log(targetPath)
		navigate(targetPath)
	}
	return (
		<>
			<div className="search-bar">
				<Search maxLength={100} 
					placeholder={props.placeholder}
					onSearch={onSearch} 
					enterButton></Search>
			</div>
		</>
	)

}