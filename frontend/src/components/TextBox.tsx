interface TextBoxProps {
  value: string;
  onChange?: React.ChangeEventHandler<HTMLTextAreaElement>;
  readOnly?: boolean;
}

export default function TextBox({ value, onChange, readOnly }: TextBoxProps) {
  return (
    <textarea
      className="textbox"
      value={value}
      onChange={onChange}
      readOnly={readOnly}
      placeholder="Enter Markdown..."
    />
  )
}