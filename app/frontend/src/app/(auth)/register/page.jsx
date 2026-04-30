"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Card } from "../../../components/ui/Card";
import { Button } from "../../../components/ui/Button";
import { AuthService } from "../../../lib/api/services";

export default function RegisterPage() {
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await AuthService.registerGuardian({
        email,
        password,
        full_name: fullName,
      });
      localStorage.setItem("guardian_token", res.access_token);
      const payload = JSON.parse(atob(res.access_token.split(".")[1]));
      localStorage.setItem("guardian_id", payload.sub);
      router.push("/parent-dashboard");
    } catch (err) {
      setError(err.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="p-8 shadow-xl bg-white">
      <div className="text-center mb-6">
        <h1 className="text-3xl font-['Baloo_2'] text-[var(--text)] mb-2">Create Account</h1>
        <p className="text-[var(--muted)]">Guardian registration</p>
      </div>

      {error && <div className="bg-red-50 text-red-600 p-3 rounded-md mb-4 text-sm">{error}</div>}

      <form onSubmit={handleRegister} className="space-y-4">
        <div>
          <label className="block text-sm font-bold text-gray-700 mb-1">Full name</label>
          <input
            type="text"
            required
            minLength={2}
            className="w-full border-2 border-gray-200 rounded-lg p-3 outline-none focus:border-[var(--gold)]"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
          />
        </div>
        <div>
          <label className="block text-sm font-bold text-gray-700 mb-1">Email</label>
          <input
            type="email"
            required
            className="w-full border-2 border-gray-200 rounded-lg p-3 outline-none focus:border-[var(--gold)]"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label className="block text-sm font-bold text-gray-700 mb-1">Password</label>
          <input
            type="password"
            required
            className="w-full border-2 border-gray-200 rounded-lg p-3 outline-none focus:border-[var(--gold)]"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <Button type="submit" fullWidth disabled={loading}>
          {loading ? "Creating account..." : "Sign Up"}
        </Button>
      </form>

      <p className="text-center mt-4 text-sm text-gray-600">
        Already have an account?{" "}
        <button onClick={() => router.push("/login")} className="text-blue-600 font-bold hover:underline">
          Log In
        </button>
      </p>
    </Card>
  );
}
