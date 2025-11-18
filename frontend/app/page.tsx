"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useEffect, useState } from "react";

export default function Home() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* Binary Rain Background - 1s and 0s only */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-cyan-950/20 to-transparent"></div>
        {mounted && [...Array(40)].map((_, i) => (
          <div
            key={i}
            className="absolute top-0 text-cyan-500 text-xs font-mono opacity-30 animate-matrix-rain"
            style={{
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 5}s`,
              animationDuration: `${8 + Math.random() * 8}s`,
            }}
          >
            {Array.from({ length: 25 }, () =>
              Math.random() > 0.5 ? '1' : '0'
            ).join('\n')}
          </div>
        ))}
      </div>

      {/* Animated Grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#0ff1_1px,transparent_1px),linear-gradient(to_bottom,#0ff1_1px,transparent_1px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_50%,black,transparent)]"></div>

      {/* Floating Particles */}
      {mounted && [...Array(20)].map((_, i) => (
        <div
          key={i}
          className="absolute w-1 h-1 bg-cyan-400 rounded-full animate-float"
          style={{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 5}s`,
            animationDuration: `${15 + Math.random() * 10}s`,
          }}
        ></div>
      ))}

      {/* Cyber Scan Lines */}
      <div className="absolute inset-0 bg-[linear-gradient(transparent_50%,rgba(0,255,255,0.03)_50%)] bg-[length:100%_4px] pointer-events-none"></div>

      {/* Glowing Orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/20 rounded-full blur-[100px] animate-pulse-slow"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-[100px] animate-pulse-slow" style={{ animationDelay: '2s' }}></div>

      {/* Corner Accent Lines */}
      <div className="absolute top-0 left-0 w-40 h-40 border-l-2 border-t-2 border-cyan-500/50"></div>
      <div className="absolute top-0 right-0 w-40 h-40 border-r-2 border-t-2 border-cyan-500/50"></div>
      <div className="absolute bottom-0 left-0 w-40 h-40 border-l-2 border-b-2 border-cyan-500/50"></div>
      <div className="absolute bottom-0 right-0 w-40 h-40 border-r-2 border-b-2 border-cyan-500/50"></div>

      <div className="relative z-10">
      {/* Header */}
      <header className="border-b border-cyan-500/20 bg-black/40 backdrop-blur-md">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-2 text-2xl font-bold text-white">
            <span className="text-3xl">🛡️</span>
            <span>Genesis Auditor</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/dashboard">
              <Button variant="ghost" className="text-white hover:bg-white/10">
                Dashboard
              </Button>
            </Link>
            <Link href="/dashboard/new-audit">
              <Button className="bg-cyan-600 hover:bg-cyan-700">
                Start Free Audit
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-24 text-center">
        <div className="mx-auto max-w-4xl space-y-8">
          <h1 className="text-6xl font-bold tracking-tight text-white">
            AI Security Testing
            <br />
            That Actually Learns
          </h1>
          <p className="mx-auto max-w-2xl text-xl text-gray-300">
            Genesis Auditor uses Gemini 2.5 to design custom security tests for your APIs.
            Every successful attack is stored in vector memory, making each audit smarter than the last.
          </p>
          <div className="flex justify-center gap-4">
            <Link href="/dashboard/new-audit">
              <Button size="lg" className="bg-cyan-600 px-8 py-6 text-lg hover:bg-cyan-700">
                Start Free Audit
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button size="lg" className="bg-blue-600 px-8 py-6 text-lg hover:bg-blue-700">
                View Dashboard
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <Card className="border-cyan-500/20 bg-black/60 text-white backdrop-blur-sm hover:border-cyan-500/40 transition-all">
            <CardHeader>
              <div className="mb-2 text-4xl">🤖</div>
              <CardTitle className="text-cyan-400">AI Agent Design</CardTitle>
              <CardDescription className="text-gray-400">
                Gemini 2.5 creates specialized security agents tailored to your compliance domain
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-cyan-500/20 bg-black/60 text-white backdrop-blur-sm hover:border-cyan-500/40 transition-all">
            <CardHeader>
              <div className="mb-2 text-4xl">🧠</div>
              <CardTitle className="text-cyan-400">Vector Memory Learning</CardTitle>
              <CardDescription className="text-gray-400">
                Qdrant stores successful attack patterns. Each audit learns from past successes.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-cyan-500/20 bg-black/60 text-white backdrop-blur-sm hover:border-cyan-500/40 transition-all">
            <CardHeader>
              <div className="mb-2 text-4xl">📊</div>
              <CardTitle className="text-cyan-400">Executive Reports</CardTitle>
              <CardDescription className="text-gray-400">
                Compliance scores, vulnerability details, and PDF reports ready for stakeholders
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-cyan-500/20 bg-black/60 text-white backdrop-blur-sm hover:border-cyan-500/40 transition-all">
            <CardHeader>
              <div className="mb-2 text-4xl">🌐</div>
              <CardTitle className="text-cyan-400">5 Compliance Domains</CardTitle>
              <CardDescription className="text-gray-400">
                HIPAA, PCI-DSS, GDPR, Financial Fraud, and general API security coverage
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* How It Works */}
      <section className="container mx-auto px-4 py-16">
        <h2 className="mb-12 text-center text-4xl font-bold text-white">How It Works</h2>
        <div className="mx-auto max-w-3xl space-y-6">
          <Card className="border-cyan-500/30 bg-black/60 text-white backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-3">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-cyan-600 text-white font-bold">1</span>
                <span className="text-cyan-400">Memory Query</span>
              </CardTitle>
              <CardDescription className="text-gray-400">
                System retrieves relevant past attacks from Qdrant vector database based on your domain
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-cyan-500/30 bg-black/60 text-white backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-3">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-cyan-600 text-white font-bold">2</span>
                <span className="text-cyan-400">Agent Design</span>
              </CardTitle>
              <CardDescription className="text-gray-400">
                Gemini 2.5 designs specialized security agents based on your domain and target API
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-cyan-500/30 bg-black/60 text-white backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-3">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-cyan-600 text-white font-bold">3</span>
                <span className="text-cyan-400">Attack Execution</span>
              </CardTitle>
              <CardDescription className="text-gray-400">
                Agents execute comprehensive security tests and identify vulnerabilities
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-cyan-500/30 bg-black/60 text-white backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-3">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-cyan-600 text-white font-bold">4</span>
                <span className="text-cyan-400">Results & Learning</span>
              </CardTitle>
              <CardDescription className="text-gray-400">
                Get detailed compliance reports while successful attacks are stored for future use
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-24 text-center">
        <div className="mx-auto max-w-2xl space-y-6">
          <h2 className="text-4xl font-bold text-white">Ready to Secure Your API?</h2>
          <p className="text-xl text-gray-300">
            Start your first security audit in under 60 seconds. No credit card required.
          </p>
          <Link href="/dashboard/new-audit">
            <Button size="lg" className="bg-cyan-600 px-12 py-6 text-lg hover:bg-cyan-700">
              Launch Your First Audit
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-cyan-500/20 bg-black/40 py-8">
        <div className="container mx-auto px-4 text-center text-gray-400">
          <p>© 2025 Genesis Auditor. AI-Powered Security Platform.</p>
        </div>
      </footer>
      </div>
    </div>
  );
}
