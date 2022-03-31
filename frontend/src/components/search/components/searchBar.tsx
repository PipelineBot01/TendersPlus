
/**
 * The search component has following features:
 * 1. search tenders via tags
 * 2. search tenders via divisions
 */
import React from "react"
import {Input } from 'antd'
const { Search } = Input

import './searchBar.css'

import { useNavigate } from "react-router-dom"

interface SearchBarProp{
    placeholder:string
}
export default function SearchBar(props:SearchBarProp):JSX.Element{
	const navigate = useNavigate()

	const onSearch = (value:string)=>{
		value === '' ? navigate('/search') : navigate('/search?query=' + window.btoa(value))
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