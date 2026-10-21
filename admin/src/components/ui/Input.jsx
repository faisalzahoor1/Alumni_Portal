export default function Input({ label, error, hint, as = "input", options, className = "", id, ...props }) {
  const inputId = id || props.name;
  let control;
  if (as === "textarea") {
    control = <textarea id={inputId} className={`textarea ${className}`} {...props} />;
  } else if (as === "select") {
    control = (
      <select id={inputId} className={`select ${className}`} {...props}>
        {options.map((option) => {
          const value = typeof option === "string" ? option : option.value;
          const text = typeof option === "string" ? option : option.label;
          return (
            <option key={value} value={value}>
              {text}
            </option>
          );
        })}
      </select>
    );
  } else {
    control = <input id={inputId} className={`input ${className}`} {...props} />;
  }

  return (
    <div className="field">
      {label && <label htmlFor={inputId}>{label}</label>}
      {control}
      {hint && !error && <span className="field-hint">{hint}</span>}
      {error && <span className="field-error">{error}</span>}
    </div>
  );
}
