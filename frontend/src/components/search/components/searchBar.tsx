
/**
 * The search component has following features:
 * 1. search tenders via tags
 * 2. search tenders via divisions
 */
import React, { MouseEventHandler, useRef, useState } from "react"
import { useNavigate, useLocation } from "react-router-dom"
import {Dropdown, Input, Menu, Form } from 'antd'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faChevronDown} from '@fortawesome/free-solid-svg-icons'

import './searchBar.css'
import { researchFields } from "../../../utils/data/researchFields"
import capitalize from '../../../utils/capitalize'



const { Search } = Input

interface SearchBarProp{
    placeholder:string
}

export default function SearchBar(props:SearchBarProp):JSX.Element{
  const navigate = useNavigate()
  const location = useLocation()
  const [searchContent, setSearchContent]  = useState('')
  const [dropdownVisible, setDropdownVisible] = useState(false)
  const onSearch = (value:string)=>{
    let targetPath = '/search'
    if(location.pathname.includes('dashboard')){
      targetPath = '/dashboard' + targetPath
    }
    if(value){
      targetPath += '?query=' + window.btoa(value)
    }
    navigate(targetPath)
  }
  const onSelectedMenuItem = (item:any)=>{
    console.log('item:', item)
    console.log(searchContent)
    searchContent === '' ? 
      setSearchContent(capitalize(researchFields[item.key].field)) :  
      setSearchContent(searchContent + ' ' + capitalize(researchFields[item.key].field))
  }

  const renderDropdownMenu = ()=>{
    const menuItem = Object.entries(researchFields).map(([k, v])=>{
      return <Menu.Item key={k} onClick={onSelectedMenuItem}>
        {capitalize(v.field)}
      </Menu.Item>
    })
		
    const menu = (<Menu 
      triggerSubMenuAction='click'
    >
      {
        menuItem
      }
    </Menu>)
    return (
      <Dropdown 
        trigger={['click', 'hover']}  
        placement="bottomCenter" 
        overlay={menu} 
        overlayStyle={{maxHeight:'15rem', overflowY:'scroll'}}
        visible={dropdownVisible}
        onVisibleChange={(flag)=>{setDropdownVisible(flag)}}
      >
        <FontAwesomeIcon icon={faChevronDown} style={{padding:'0 0.8rem'}}/>
      </Dropdown>)
  }

  return (
    <>
      <div className="search-bar">	
        <Search  maxLength={100} 
          addonAfter={renderDropdownMenu()}
          value={searchContent}
          onSearch={onSearch}
          onChange={(e)=>{setSearchContent(e.currentTarget.value)}}
          placeholder={props.placeholder}
          enterButton></Search>
      </div>
    </>
  )

}