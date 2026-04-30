"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Card } from "../../../components/ui/Card";
import { Button } from "../../../components/ui/Button";
import { AuthService } from "../../../lib/api/services";
import { useLearner } from "../../../context/LearnerContext";

export default function LoginPage() {
  const router = useRouter();
  const { setLearner } = useLearner();
  const [isParent, setIsParent] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (isParent) {
        const res = await AuthService.loginGuardian({ email, password });
        localStorage.setItem("guardian_token", res.access_token);
        const payload = JSON.parse(atob(res.access_token.split(".")[1]));
        localStorage.setItem("guardian_id", payload.sub);
        router.push("/parent-dashboard"); // Parent dashboard
      }
    } catch (err) {
      setError(err.message || "Failed to log in");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="p-8 shadow-xl bg-white">
      <div className="text-center mb-6">
        <h1 className="text-3xl font-['Baloo_2'] text-[var(--text)] mb-2">Welcome Back!</h1>
        <p className="text-[var(--muted)]">Log in to continue learning</p>
      </div>

      <div className="flex bg-gray-100 p-1 rounded-lg mb-6">
        <button
          className={`flex-1 py-2 text-sm font-bold rounded-md ${!isParent ? "bg-white shadow" : "text-gray-500"}`}
          onClick={() => setIsParent(false)}
        >
          Learner
        </button>
        <button
          className={`flex-1 py-2 text-sm font-bold rounded-md ${isParent ? "bg-white shadow" : "text-gray-500"}`}
          onClick={() => setIsParent(true)}
        >
          Parent / Guardian
        </button>
      </div>

      {error && <div className="bg-red-50 text-red-600 p-3 rounded-md mb-4 text-sm">{error}</div>}

      <form onSubmit={handleLogin} className="space-y-4">
        {isParent ? (
          <>
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
          </>
        ) : (
          <div className="text-center py-4 text-gray-500 flex flex-col gap-3">
            <p>Learner login flow is under construction.</p>
            <Button 
              onClick={() => {
                setLearner({
                  learner_id: "550e8400-e29b-41d4-a716-446655440000",
                  nickname: "DevLearner",
                  grade: 3,
                  avatar: 0
                });
                router.push("/dashboard");
              }} 
              variant="secondary" 
              className="bg-green-50 text-green-700 border-green-200"
            >
              Bypass Login (Dev) →
            </Button>
          </div>
        )}

        {isParent && (
          <Button type="submit" fullWidth disabled={loading}>
            {loading ? "Logging in..." : "Log In"}
          </Button>
        )}
      </form>

      {isParent && (
        <div className="mt-4">
          <Button 
            onClick={() => {
              localStorage.setItem("guardian_token", "dev-token");
              router.push("/parent-dashboard");
            }} 
            variant="secondary" 
            fullWidth 
            className="bg-yellow-50 text-yellow-700 border-yellow-200"
          >
            Bypass Parent Login (Dev) →
          </Button>
        </div>
      )}

      {isParent && (
        <p className="text-center mt-4 text-sm text-gray-600">
          Don't have an account?{" "}
          <button onClick={() => router.push("/register")} className="text-blue-600 font-bold hover:underline">
            Register
          </button>
        </p>
      )}
    </Card>
  );
}
