import { useState } from "react"
import TextBox from "./TextBox"

export default function Converter(): React.ReactElement {
  const [markdown, setMarkdown] = useState<string>("")
  const [html, setHtml] = useState<string>("")

  const handleConvert = (): void => {
    setHtml(markdown)
  }

return (
  <div className="converter">
    <button className="convert-btn" onClick={handleConvert}>Convert</button>
    <div className="textboxes">
      <div className="textbox-wrapper">
        <label className="textbox-label">Input</label>
        <TextBox
          value={markdown}
          onChange={(e) => setMarkdown(e.target.value)}
        />
      </div>
      <div className="arrow">→</div>
      <div className="textbox-wrapper">
        <label className="textbox-label">Output</label>
        <TextBox value={html} readOnly />
      </div>
    </div>
  </div>
)
}