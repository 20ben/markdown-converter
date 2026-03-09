import { useState } from "react"
import TextBox from "./TextBox"
import SummaryPanel from "./SummaryPanel"

export default function Converter(): React.ReactElement {
  const [markdown, setMarkdown] = useState<string>("")
  const [html, setHtml] = useState<string>("")

  const handleConvert = async (): Promise<void> => {
    const response = await fetch('http://localhost:5000/api/convert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ markdown })
    })

    const data = await response.json()
    setHtml(data.html)
  }

  return (
    <div className="converter">
      <button className="convert-btn" onClick={handleConvert} disabled={!markdown.trim()}>Convert</button>
      <div className="textboxes">
        <div className="textbox-wrapper">
          <label className="textbox-label">Input</label>
          <TextBox
            value={markdown}
            placeholder="Enter Markdown text here..."
            onChange={(e) => setMarkdown(e.target.value)}
          />
        </div>
        <div className="arrow">→</div>
        <div className="textbox-wrapper">
          <label className="textbox-label">Output</label>
          <TextBox value={html} placeholder="" readOnly />
        </div>
      </div>
      <SummaryPanel markdown={markdown} />
    </div>
  )
}
