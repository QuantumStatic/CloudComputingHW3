import { Fragment, useState } from 'react'
import './App.css'
import UploadBox from './components/UploadBox'
import SearchArea from './components/SearchArea'
import './utlities.js'


function App() {

  return (
    <div id='left-right-division'>
      <div className='minor-left-item'>
        <UploadBox />
      </div>
      
      <div className='minor-right-item'>
        <SearchArea className="minor-right-item" />
      </div>
      
    </div>
  )
}

export default App
