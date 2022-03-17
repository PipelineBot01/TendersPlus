import React from "react"
export function RingChart():JSX.Element{
	return <>
		<svg width="100%" height="100%" viewBox="0 0 42 42" className="donut">
			<circle className="donut-hole" cx="21" cy="21" r="15.91549430918954" fill="#fff"></circle>
			<circle className="donut-ring" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#d2d3d4" stroke-width="3"></circle>

			<circle className="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#ce4b99" stroke-width="3" stroke-dasharray="85 15" stroke-dashoffset="0"></circle>
		</svg>
	</>
}