interface TextBoxProps {
  value: string;
  placeholder: string;
  onChange?: React.ChangeEventHandler<HTMLTextAreaElement>;
  readOnly?: boolean;
}

export default function TextBox({ value, placeholder, onChange, readOnly }: TextBoxProps) {
  return (
    <textarea
      className="textbox"
      value={value}
      onChange={onChange}
      readOnly={readOnly}
      placeholder={placeholder}
    />
  )
}