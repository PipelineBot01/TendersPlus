
/**
 * The search component has following features:
 * 1. search tenders via tags
 */
import React, {useEffect, useState} from "react"
import {Select, Button } from 'antd'
import {SearchOutlined} from '@ant-design/icons'
import './index.css'
const {Option} = Select

interface options{
    label:string
    value:string
}

export default function Search():JSX.Element{
	const [tagOptions, setTagOptions] = useState(new Array<options>())
	const [showResult, setShowResult] = useState(false)
	useEffect(()=>{
		// 1. fetch tag options from backend
		setTagOptions([{
			label:'label1',
			value:'value1'
		}, {
			label:'label2',
			value:'value2'
		}])
	}, [])




	const handleChange = ()=>{
		console.log(111)
       
	}
	const renderSearch = ()=>{
	
		const children = tagOptions.map((e)=>{
			return <Option key={e.label}>{e.value}</Option>
		})
        	console.log(tagOptions)
		return (
			<>

				<div className="search">

					<div className="search-container">
						<div className="slogan">
                        Seize million  dollars & <br /> greatest opportunities.
						</div>
						<div className="desc">
Tenders+ provides life-cycle assistance for tenders and procurement through effective and efficient management of the tender and procurement process.
						</div>

						<div className="search-box">
							<Select
								className="tag-selector"
								mode="tags"
								style={{width:'100%'}}
								allowClear
								placeholder="Let's find out tenders"
								maxTagTextLength={30}
								tokenSeparators={[',', ';']}
								// notFoundContent={null}
								maxTagCount={30}
								// optionFilterProp='label'
							>
								{children}
							</Select>
							<button className="tag-search" >
								<SearchOutlined />
							</button>
						
						</div>
					
				
					
                    
					</div>
				</div>
			</>
		)
	}
	const renderResult = ()=>{
		return (<>Here is the Result</>)
	}

	return showResult ? renderResult() : renderSearch()
}