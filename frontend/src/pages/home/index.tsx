import React from "react"

import {SearchBar} from '../../components/search'
import Discovery from '../../components/discovery'
import StrengthOverview from '../../components/strengthOverview'
import './index.css'
export default function Home():JSX.Element{
  return <>
    
    <>
      <div className="search">

        <div className="search-container">
          <div className="slogan">
                        Seize million  dollars & <br /> greatest opportunities.
          </div>
          <div className="desc">
Tenders+ provides life-cycle assistance for tenders and procurement through effective and efficient management of the tender and procurement process.
          </div>

          {/* <div className="search-box"> */}
          <SearchBar placeholder="Let's find out your opportunities"/>	
          {/* </div> */}
					
				
        </div>
      </div>
    </>
    <Discovery/>
    <StrengthOverview/>
		
  </>
}