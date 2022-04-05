
/**
 * The search component has following features:
 * 1. search tenders via tags
 * 2. search tenders via divisions
 */
import React from "react"
import { useNavigate } from "react-router-dom"
import {Input } from 'antd'

import './searchBar.css'

import { useCollector } from "../../../utils/customHook"


const { Search } = Input







interface SearchBarProp{
    placeholder:string
}
export default function SearchBar(props:SearchBarProp):JSX.Element{
	const navigate = useNavigate()

	const onSearch = (value:string)=>{
		value === '' ? navigate('/search') : navigate('/search?query=' + window.btoa(value))
		useCollector({type:0, payload:value})
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