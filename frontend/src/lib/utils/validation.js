export function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) ? null : "Enter a valid email address";
}

export function validatePassword(password, { min_length, max_length }) {
  if (password.length < min_length) return `Password must be at least ${min_length} characters`;
  if (password.length > max_length) return `Password must be at most ${max_length} characters`;
  return null;
}

export function validateUrl(value) {
  if (!value) return null;
  try {
    new URL(value);
    return null;
  } catch {
    return "Enter a full URL, e.g. https://example.com";
  }
}

export function validateSignup({ email, password, confirm_password, role }, config) {
  const errors = {};
  const emailError = validateEmail(email);
  if (emailError) errors.email = emailError;
  const passwordError = validatePassword(password, config.password);
  if (passwordError) errors.password = passwordError;
  if (password !== confirm_password) errors.confirm_password = "Passwords do not match";
  if (!config.signup_roles.some((r) => r.value === role)) errors.role = "Choose a role";
  return errors;
}

export function validateFile(file, { max_size_bytes, content_types, extensions }) {
  const name = file.name.toLowerCase();
  const typeOk = content_types.includes(file.type) || extensions.some((ext) => name.endsWith(ext));
  if (!typeOk) return `Allowed file types: ${extensions.join(", ")}`;
  if (file.size > max_size_bytes) return `File must be under ${Math.round(max_size_bytes / (1024 * 1024))} MB`;
  return null;
}
