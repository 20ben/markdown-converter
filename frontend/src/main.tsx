import ReactDOM from 'react-dom/client'
import { asyncWithLDProvider } from 'launchdarkly-react-client-sdk'
import { v4 as uuidv4 } from 'uuid'
import App from './App.tsx'
import './index.css'

function getUserId(): string {
  let id = localStorage.getItem('md_user_id')
  if (!id) { id = uuidv4(); localStorage.setItem('md_user_id', id) }
  return id!
}

;(async () => {
  const LDProvider = await asyncWithLDProvider({
    clientSideID: '69aba909395e3b09f11f6cac',
    context: {
      kind: 'user',
      key: getUserId(),
      anonymous: true,
    },
  })

  ReactDOM.createRoot(document.getElementById('root')!).render(
    <LDProvider>
      <App />
    </LDProvider>
  )
})()
