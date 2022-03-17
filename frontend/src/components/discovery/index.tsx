
import './index.css'
import { Card, Row, Col } from 'antd'
import {Link} from 'react-router-dom'
import {DoubleRightOutlined} from '@ant-design/icons'
import { useState } from 'react'
export default function Discovery():JSX.Element{
	const [totalNumberTenders, setTotalNumberTenders] = useState(153)

	const renderLatestOpportunities = ()=>{
		return <>
		  <Card 
		  type='inner' 
		  style={{margin:'1rem 0'}} title={<>
		  <span style={{color:'#4b4b4b'}}>GO5382 - Every Doctor, Every Setting Framework</span>
		  </>}>
			  <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Agency :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Close Date&Time :</Col>
					<Col span={17}>18-Mar-2022 2:00 pm (ACT Local Time)</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Category :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			  <Row justify='end' style={{marginTop:'1.5rem'}}>
					<Col ><a  style={{fontWeight:'600', color:'#e96b44'}} href='https://www.grants.gov.au/Go/Show?GoUuid=aa34c76b-34a7-4b43-ac15-dcf82abd0bb4'>Full Details <DoubleRightOutlined /></a></Col>
			  </Row>

			</Card>
			 <Card type='inner' 
			 style={{margin:'1rem 0'}}
			 title={<>
		  <span style={{color:'#4b4b4b'}}>GO5382 - Every Doctor, Every Setting Framework</span>
		  </>}>
			  <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Agency :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Close Date&Time :</Col>
					<Col span={17}>18-Mar-2022 2:00 pm (ACT Local Time)</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Category :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			  <Row justify='end' style={{marginTop:'1.5rem'}}>
					<Col ><a  style={{fontWeight:'600', color:'#e96b44'}} href='https://www.grants.gov.au/Go/Show?GoUuid=aa34c76b-34a7-4b43-ac15-dcf82abd0bb4'>Full Details <DoubleRightOutlined /></a></Col>
			  </Row>

			</Card>
			 <Card type='inner' 
			 style={{margin:'1rem 0'}}
			 title={<>
		  <span style={{color:'#4b4b4b'}}>GO5382 - Every Doctor, Every Setting Framework</span>
		  </>}>
			  <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Agency :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Close Date&Time :</Col>
					<Col span={17}>18-Mar-2022 2:00 pm (ACT Local Time)</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Category :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			  <Row justify='end' style={{marginTop:'1.5rem'}}>
					<Col ><a  style={{fontWeight:'600', color:'#e96b44'}} href='https://www.grants.gov.au/Go/Show?GoUuid=aa34c76b-34a7-4b43-ac15-dcf82abd0bb4'>Full Details <DoubleRightOutlined /></a></Col>
			  </Row>

			</Card>
		</>

		
	}
	const renderHotOpportunities = ()=>{
		return <>
		  <Card type='inner' 
		  style={{margin:'1rem 0'}} title={<>
		  <span style={{color:'#4b4b4b'}}>GO5382 - Every Doctor, Every Setting Framework</span>
		  </>}>
			  <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Agency :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Close Date&Time :</Col>
					<Col span={17}>18-Mar-2022 2:00 pm (ACT Local Time)</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Category :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			  <Row justify='end' style={{marginTop:'1.5rem'}}>
					<Col ><a  style={{fontWeight:'600', color:'#e96b44'}} href='https://www.grants.gov.au/Go/Show?GoUuid=aa34c76b-34a7-4b43-ac15-dcf82abd0bb4'>Full Details <DoubleRightOutlined /></a></Col>
			  </Row>

			</Card>
			 <Card  type='inner' 
			 style={{margin:'1rem 0'}}
			 title={<>
		  <span style={{color:'#4b4b4b'}}>GO5382 - Every Doctor, Every Setting Framework</span>
		  </>}>
			  <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Agency :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Close Date&Time :</Col>
					<Col span={17}>18-Mar-2022 2:00 pm (ACT Local Time)</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Category :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			  <Row justify='end' style={{marginTop:'1.5rem'}}>
					<Col ><a  style={{fontWeight:'600', color:'#e96b44'}} href='https://www.grants.gov.au/Go/Show?GoUuid=aa34c76b-34a7-4b43-ac15-dcf82abd0bb4'>Full Details <DoubleRightOutlined /></a></Col>
			  </Row>

			</Card>
			 <Card type='inner' 
			 style={{margin:'1rem 0'}}
			 title={<>
		  <span style={{color:'#4b4b4b'}}>GO5382 - Every Doctor, Every Setting Framework</span>
		  </>}>
			  <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Agency :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Close Date&Time :</Col>
					<Col span={17}>18-Mar-2022 2:00 pm (ACT Local Time)</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Category :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			  <Row justify='end' style={{marginTop:'1.5rem'}}>
					<Col ><a  style={{fontWeight:'600', color:'#e96b44'}} href='https://www.grants.gov.au/Go/Show?GoUuid=aa34c76b-34a7-4b43-ac15-dcf82abd0bb4'>Full Details <DoubleRightOutlined /></a></Col>
			  </Row>

			</Card>
		</>
	}
	const renderExpiringOpportunities = ()=>{
		return <>
		  <Card type='inner' style={{margin:'1rem 0'}} title={<>
		  <span style={{color:'#4b4b4b'}}>GO5382 - Every Doctor, Every Setting Framework</span>
		  </>}>
			  <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Agency :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Close Date&Time :</Col>
					<Col span={17}>18-Mar-2022 2:00 pm (ACT Local Time)</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Category :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			  <Row justify='end' style={{marginTop:'1.5rem'}}>
					<Col ><a  style={{fontWeight:'600', color:'#e96b44'}} href='https://www.grants.gov.au/Go/Show?GoUuid=aa34c76b-34a7-4b43-ac15-dcf82abd0bb4'>Full Details <DoubleRightOutlined /></a></Col>
			  </Row>

			</Card>
			 <Card  type='inner' 
			 style={{margin:'1rem 0'}}
			 title={<>
		  <span style={{color:'#4b4b4b'}}>GO5382 - Every Doctor, Every Setting Framework</span>
		  </>}>
			  <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Agency :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Close Date&Time :</Col>
					<Col span={17}>18-Mar-2022 2:00 pm (ACT Local Time)</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Category :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			  <Row justify='end' style={{marginTop:'1.5rem'}}>
					<Col ><a  style={{fontWeight:'600', color:'#e96b44'}} href='https://www.grants.gov.au/Go/Show?GoUuid=aa34c76b-34a7-4b43-ac15-dcf82abd0bb4'>Full Details <DoubleRightOutlined /></a></Col>
			  </Row>

			</Card>
			 <Card type='inner' 
			 style={{margin:'1rem 0'}}
			 title={<>
		  <span style={{color:'#4b4b4b'}}>GO5382 - Every Doctor, Every Setting Framework</span>
		  </>}>
			  <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Agency :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Close Date&Time :</Col>
					<Col span={17}>18-Mar-2022 2:00 pm (ACT Local Time)</Col>
			  </Row>
			   <Row>
					<Col span={7} style={{fontWeight:'600', textAlign:'right', paddingRight:'0.2rem'}}>Category :</Col>
					<Col span={17}>Department of Health</Col>
			  </Row>
			  <Row justify='end' style={{marginTop:'1.5rem'}}>
					<Col ><a  style={{fontWeight:'600', color:'#e96b44'}} href='https://www.grants.gov.au/Go/Show?GoUuid=aa34c76b-34a7-4b43-ac15-dcf82abd0bb4'>Full Details <DoubleRightOutlined /></a></Col>
			  </Row>

			</Card>
		</>
	}
	

	return(<>
		<div className="discovery">
			<Row justify='space-between' align="bottom" >
				<Col span={ 7}>
					<div className="title">
                    Find a grant opportunity
					</div>
				</Col>
				<Col>
					<div className='subtitle'>
					All <span>{totalNumberTenders}</span> Opened
					</div>
				</Col>
			</Row>
			
			<div className="tenders">
				<Row gutter={12}>
					<Col span={8}>
						<Card 
							className='tenders-card' 
							title='Latest' 
							headStyle={{
								fontSize:'1.2rem',
								color:'#585959'
							}}
							extra={<Link 
								to='/result/latest'
								style={{
									fontWeight:700,
									color:'#228e64',
					
									fontSize:'0.8rem',
								}}
							>READ MORE</Link>}
                        
						>
							{renderLatestOpportunities()}
						</Card>
					</Col>
                    
					<Col span={8}>
						<Card 	className='tenders-card'  title='Hot'
                        

							headStyle={{
								fontSize:'1.2rem',
								color:'#585959'
							}}
							extra={<Link 
								to='/result/hot'
								style={{
									fontWeight:700,
									color:'#228e64',
									fontSize:'0.8rem',
								
								}}
							>READ MORE</Link>}
						>
							{renderHotOpportunities()}
						</Card>
					</Col>
                    
					<Col span={8}>
						<Card 	className='tenders-card'  title='Expiring Soon'
							headStyle={{
								fontSize:'1.2rem',
								color:'#585959'
							}}
							extra={<Link 
								to='/result/expiring_soon'
								style={{
									fontWeight:700,
									color:'#228e64',
									fontSize:'0.8rem',
								}}
							>READ MORE</Link>}>
							{renderExpiringOpportunities()}
						</Card>
					</Col>

				</Row>
				
				

			</div>
		</div>
	</>)
}