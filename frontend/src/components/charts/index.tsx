import React from "react"
import './index.css'

interface DonutChartProp{
	width:number
	height:number
	strokeWidth:number
	backgroundColor:string
	chartColor:string
	percentage:number
}
export function DonutChart(prop:DonutChartProp):JSX.Element{
  const  radius = Math.min(prop.width, prop.height) / 2 * 0.8
  const  circumference = Math.PI * 2 * radius

  return <span style={{display:'inline-flex', 'alignItems':'center', margin:'0 0.1rem'}}>
	
    <svg width={prop.width} height={prop.height} viewBox={`0 0 ${prop.width} ${prop.height}`} className="donut-chart">
      <circle 
        className="donut-chart-background" 
        cx={prop.width / 2} 
        cy={prop.height / 2} 
        r={radius} 
        fill="transparent" 
        stroke={prop.backgroundColor} 
        strokeWidth={prop.strokeWidth}
      />
      <circle
				
        className="donut-chart-content"
        cx={prop.width / 2} 
        cy={prop.height / 2} 
			  	r={radius} 
			   	fill="transparent" 
			   	stroke={prop.chartColor} 
        strokeWidth={prop.strokeWidth}
        strokeDasharray={`${prop.percentage * circumference} ${circumference}`} 
        strokeDashoffset="0"></circle>
    </svg>
  </span>
}