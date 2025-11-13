import React from 'react'
function Tile() {
  return (
    <div className="
      w-16 h-16 m-0.5
      bg-blue-400
      hover:bg-pink-400
      transition-colors duration-300
      sm:hover:bg-pink-400
      animate-mobileColorChange
      sm:animate-none
    "></div>
  )
}
export default Tile;