"use client";

import Link from "next/link";
import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Alert from "@/components/ui/Alert";
import { useConfig } from "@/hooks/useConfig";

export default function LoginForm() {
  const { loginStudent, loginUser } = useAuth();
  const config = useConfig();
  const [mode, setMode] = useState("student");
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const switchMode = (next) => {
    setMode(next);
    setIdentifier("");
    setError("");
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (mode === "student") await loginStudent(identifier.trim(), password);
      else await loginUser(identifier.trim(), password);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <form className="stack" onSubmit={onSubmit}>
      <div>
        <h1>Welcome back</h1>
        <p className="muted">Sign in to your Alumni Portal account.</p>
      </div>

      <div className="tabs">
        <button type="button" className={`tab ${mode === "student" ? "tab-active" : ""}`} onClick={() => switchMode("student")}>
          Student
        </button>
        <button type="button" className={`tab ${mode === "user" ? "tab-active" : ""}`} onClick={() => switchMode("user")}>
          Alumni / Industry
        </button>
      </div>

      <Alert>{error}</Alert>

      {mode === "student" ? (
        <Input
          label="Registration number"
          name="registration_no"
          placeholder="e.g. FA21-BCS-001"
          value={identifier}
          onChange={(e) => setIdentifier(e.target.value)}
          hint="Sign in with your university SSO credentials."
          minLength={config.registration_no.min_length}
          maxLength={config.registration_no.max_length}
          required
        />
      ) : (
        <Input
          label="Email"
          name="email"
          type="email"
          placeholder="you@example.com"
          value={identifier}
          onChange={(e) => setIdentifier(e.target.value)}
          required
        />
      )}

      <Input
        label="Password"
        name="password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        minLength={config.password.min_length}
        maxLength={config.password.max_length}
        required
      />

      <Button type="submit" block loading={loading}>
        Sign in
      </Button>

      {mode === "user" && (
        <p className="muted small" style={{ textAlign: "center" }}>
          New here? <Link href="/auth/signup">Create an account</Link>
        </p>
      )}
    </form>
  );
}
