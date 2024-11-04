import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
// @ts-expect-error - ignore the error for import meta
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
