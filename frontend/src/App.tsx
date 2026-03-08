import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'

import WelcomePopup from './components/WelcomePopup'
import Header from "./components/Header"
import Converter from "./components/Converter"
import './App.css'

function App() {
  return (
    <>
        <Header />
        <Converter />
        <WelcomePopup />
    </>
  )
}

export default App
