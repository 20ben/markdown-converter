import { useState } from 'react'
import { useFlags, useLDClient } from 'launchdarkly-react-client-sdk'
import ReactMarkdown from 'react-markdown'

interface SummaryPanelProps {
  markdown: string
}

export default function SummaryPanel({ markdown }: SummaryPanelProps) {
  const { aiSummaryEnabled } = useFlags()
  const ldClient = useLDClient()

  const [summary, setSummary] = useState<string>('')
  const [variant, setVariant] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string>('')

  if (!aiSummaryEnabled) return null

  const handleGenerate = async () => {
    setLoading(true)
    setError('')
    setSummary('')

    const userId = localStorage.getItem('md_user_id') || 'anonymous'

    try {
      const response = await fetch('http://localhost:5000/api/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ markdown, user_id: userId })
      })

      if (!response.ok) {
        throw new Error('Failed to generate summary')
      }

      const data = await response.json()
      setSummary(data.summary)
      setVariant(data.variant)
    } catch (e) {
      setError('Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleHelpful = () => {
    ldClient?.track('helpful-click', undefined, 1)
  }

  return (
    <div className="summary-panel">
      <button className="generate-btn" onClick={handleGenerate} disabled={loading || !markdown.trim()}>
        {loading ? 'Generating...' : 'Generate Summary'}
      </button>

      {summary && (
        <div className="summary-content">
          <span className="variant-badge">{variant}</span>
          <div className="summary-text">
            <ReactMarkdown allowedElements={[
              'p', 'br',
              'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
              'strong', 'em',
              'ul', 'ol', 'li',
              'code', 'pre',
              'blockquote',
              'hr',
              'table', 'thead', 'tbody', 'tr', 'th', 'td',
            ]}>
              {summary}
            </ReactMarkdown>
          </div>
          <button className="helpful-btn" onClick={handleHelpful}>👍 Helpful</button>
        </div>
      )}

      {error && <p className="summary-error">{error}</p>}
    </div>
  )
}
