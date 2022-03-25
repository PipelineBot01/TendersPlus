import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter  } from "react-router-dom"
import { Provider } from 'react-redux'
import App from './App'

import {store} from './store'
import 'antd/dist/antd.css'
import './index.css'
import setRem from './utils/setRem'

window.addEventListener('resize', setRem)
window.addEventListener('pageshow', setRem)


ReactDOM.render(
	<React.StrictMode>
		<Provider store={store}>
			<BrowserRouter basename='tendersplus' >
				<App />
			</BrowserRouter>
		</Provider>
	</React.StrictMode>,
	document.getElementById('root')

)
