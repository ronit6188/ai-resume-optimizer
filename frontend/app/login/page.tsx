"use client";

import { ArrowRightIcon, LockClosedIcon } from "@heroicons/react/24/outline";
import Link from "next/link";
import { useRouter } from "next/navigation";
import type { FormEvent } from "react";
import { useState } from "react";
import { motion } from "framer-motion";

import { login } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      await login(email, password);
      router.push("/dashboard");
    } catch (err) {
      console.error("Login error:", err);
      const message = err instanceof Error ? err.message : "Could not sign in.";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-gradient-to-br from-surface-primary via-surface-secondary to-surface-primary" />
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-accent-gold/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent-violet/10 rounded-full blur-3xl" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative w-full max-w-md mx-4"
      >
        <div className="card-premium p-8">
          <div className="mb-8 flex items-center gap-4">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-accent-gold/20 to-accent-gold/5 flex items-center justify-center">
              <LockClosedIcon className="w-7 h-7 text-accent-gold" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">Welcome back</h1>
              <p className="text-gray-500">Sign in to your account</p>
            </div>
          </div>

          <form className="space-y-5" onSubmit={onSubmit}>
            <div>
              <label className="label-premium">Email</label>
              <input
                className="input-premium"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="you@example.com"
                required
              />
            </div>
            <div>
              <label className="label-premium">Password</label>
              <input
                className="input-premium"
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="••••••••"
                required
              />
            </div>

            {error && (
              <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
                {error}
              </div>
            )}

            <button
              className="btn-primary w-full py-3.5"
              type="submit"
              disabled={loading}
            >
              {loading ? "Signing in..." : "Sign in"}
              <ArrowRightIcon className="w-5 h-5" />
            </button>
          </form>

          <div className="mt-8 flex items-center justify-between text-sm">
            <Link className="text-accent-gold hover:text-accent-goldLight font-medium" href="/signup">
              Create account
            </Link>
            <Link className="text-gray-500 hover:text-gray-300" href="/reset">
              Forgot password?
            </Link>
          </div>
        </div>

        <p className="text-center text-gray-500 text-sm mt-6">
          Don't have an account?{" "}
          <Link className="text-accent-gold hover:text-accent-goldLight font-medium" href="/signup">
            Sign up free
          </Link>
        </p>
      </motion.div>
    </main>
  );
}