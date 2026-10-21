"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { authApi } from "@/lib/api/auth";
import { validateSignup } from "@/lib/utils/validation";
import { useConfig } from "@/hooks/useConfig";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Alert from "@/components/ui/Alert";
import RoleSelector from "./RoleSelector";

export default function SignupForm() {
  const router = useRouter();
  const config = useConfig();
  const [form, setForm] = useState({ email: "", password: "", confirm_password: "", role: config.signup_roles[0]?.value || "" });
  const [errors, setErrors] = useState({});
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target ? e.target.value : e }));

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const fieldErrors = validateSignup(form, config);
    setErrors(fieldErrors);
    if (Object.keys(fieldErrors).length) return;

    setLoading(true);
    try {
      const res = await authApi.signup({ ...form, email: form.email.trim() });
      const params = new URLSearchParams({ email: form.email.trim(), message: res.message });
      router.push(`/auth/verify-otp?${params}`);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <form className="stack" onSubmit={onSubmit} noValidate>
      <div>
        <h1>Create your account</h1>
        <p className="muted">For alumni and industry partners. Students sign in with university SSO.</p>
      </div>

      <Alert>{error}</Alert>

      <RoleSelector value={form.role} onChange={set("role")} error={errors.role} />
      <Input label="Email" name="email" type="email" value={form.email} onChange={set("email")} error={errors.email} />
      <Input
        label="Password"
        name="password"
        type="password"
        value={form.password}
        onChange={set("password")}
        error={errors.password}
        hint={`${config.password.min_length}–${config.password.max_length} characters`}
      />
      <Input
        label="Confirm password"
        name="confirm_password"
        type="password"
        value={form.confirm_password}
        onChange={set("confirm_password")}
        error={errors.confirm_password}
      />

      <Button type="submit" block loading={loading}>
        Create account
      </Button>

      <p className="muted small" style={{ textAlign: "center" }}>
        Already have an account? <Link href="/auth/login">Sign in</Link>
      </p>
    </form>
  );
}
