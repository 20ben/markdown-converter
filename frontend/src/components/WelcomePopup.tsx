import { useFlags } from 'launchdarkly-react-client-sdk'


/* THIS IS DEPRECIATED, WAS USED ONLY FOR TESTING FLAGS */

export default function WelcomePopup() {
  const { showWelcomePopup } = useFlags()

  if (!showWelcomePopup) return null

  return (
    <div style={{
      position: 'fixed', bottom: '1rem', right: '1rem',
      background: '#4c48ff', color: 'white',
      padding: '0.75rem 1rem', borderRadius: '8px',
      boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
      fontSize: '14px', zIndex: 9999,
    }}>
      Feature flags are working!
    </div>
  )
}