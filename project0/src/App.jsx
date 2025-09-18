import { FlaskConical } from 'lucide-react'
import React from 'react'

const App = () => {
  return (
    <div>
      <nav className='flex p-4 flex-row justify-between items-center'>
        <div className='flex px-4 flex-row items-center'>
            <a href=''><p className='font-sans flex items-start '>About</p></a>
            <a href=''><p className='font-sans flex items justify-between '>Store</p></a>
        </div>
        <div className='flex flex-row py-1 items-center '>
          <a href=''>Gmail</a>
          <a href=''>Images</a>
          <a href=''>Advance </a>
          <a href=''><FlaskConical /></a>
        </div>
      </nav>
      
    </div>
  )
}

export default App 



 
        
       