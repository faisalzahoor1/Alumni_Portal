import Spinner from "./Spinner";

export default function Button({ variant = "primary", size, block, loading, disabled, className = "", children, ...props }) {
  const classes = ["btn", `btn-${variant}`, size === "sm" && "btn-sm", block && "btn-block", className]
    .filter(Boolean)
    .join(" ");
  return (
    <button className={classes} disabled={disabled || loading} {...props}>
      {loading && <Spinner size="sm" />}
      {children}
    </button>
  );
}
