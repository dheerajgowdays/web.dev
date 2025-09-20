import { FlaskConical } from 'lucide-react'
import React from 'react'

const App = () => {
  return (
    <div className='bg-[#343638] h-screen text-white'>
      <nav className='flex p-4 flex-row justify-between items-center'>
        <div className='flex flex-row items-center space-x-10'>
            <a href=''><p className='font-sans  hover:underline'>About</p></a>
            <a href=''><p className='font-sans  hover:underline'>Store</p></a>
        </div>
        <div className='flex flex-row items-center space-x-10 '>
          <a href=''><p className='font-sans hover:underline'>Gmail</p></a>
          <a href=''className='font-sans  hover:underline '>Images</a>
          <a href='' className='font-san hover:underline'>Advance </a>
          <a href=''><FlaskConical /></a>
          <a href=''><button className='relative text-white after:block after:h-[2px] after:bg-black after:scale-x-0 after:transition-transform after:duration-300 hover:after:scale-x-100 after:origin-left'>Sign in</button></a>
        </div>
      </nav>
      <div className='flex justify-center items-center h-screen '>
        <form action=""> 
          <input type="text" name="" id=""  className='border border-white bg-transparent text-white px-3 py-2 rounded-2xl items-center'/>
        </form>
      </div>
    </div>
  )
}

export default App 



 
        
    