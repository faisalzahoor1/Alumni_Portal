"use client";

import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { useConfigQuery } from "@/hooks/useConfig";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Alert from "@/components/ui/Alert";
import ParticleField from "@/components/fx/ParticleField";

export default function AdminLoginPage() {
  const { login } = useAuth();
  const { data: config } = useConfigQuery();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email.trim(), password);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <div className="admin-login">
      <div className="orbs" aria-hidden>
        <span className="orb orb-1" />
        <span className="orb orb-2" />
        <span className="orb orb-3" />
        <ParticleField variant="light" />
      </div>
      <form className="card admin-login-card stack" onSubmit={onSubmit}>
        <div className="admin-login-mark" aria-hidden>
          🛡️
        </div>
        <div style={{ textAlign: "center" }}>
          <h1 className="gradient-text">Admin Portal</h1>
          <p className="muted" style={{ margin: 0 }}>
            {config?.university?.name || "Alumni Portal"}
          </p>
        </div>
        <Alert>{error}</Alert>
        <Input label="Email" name="email" type="email" autoComplete="username" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <Input
          label="Password"
          name="password"
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <Button type="submit" block loading={loading}>
          Sign in
        </Button>
        <p className="muted small" style={{ textAlign: "center", margin: 0 }}>
          Admin accounts are created by the system administrator.
        </p>
      </form>
    </div>
  );
}
