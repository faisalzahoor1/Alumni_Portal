"use client";

import { useConfig } from "@/hooks/useConfig";

export default function RoleSelector({ value, onChange, error }) {
  const { signup_roles } = useConfig();
  return (
    <div className="field">
      <label>I am joining as</label>
      <div className="role-options">
        {signup_roles.map((role) => (
          <button
            type="button"
            key={role.value}
            className={`role-option ${value === role.value ? "role-option-active" : ""}`}
            onClick={() => onChange(role.value)}
          >
            <strong>{role.label}</strong>
            <span>{role.description}</span>
          </button>
        ))}
      </div>
      {error && <span className="field-error">{error}</span>}
    </div>
  );
}
