import React from 'react'

const Navbar = () => {
  return (
    <div className=' flex w-full justify-between px-7 py-2 bg-gray-900 text-white'>
      <div className=' text-4xl font-bold'>MEM.CODE</div>
      <div>
        <ul className=' flex w-full text-2xl space-x-3'>
          <li>Home</li>
          <li>Quiz</li>
          <li>Faq</li>
        </ul>
      </div>
    </div>
  )
}

export default Navbar