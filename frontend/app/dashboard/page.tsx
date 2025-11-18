"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { api, type MemoryStats } from "@/lib/api/client";

export default function DashboardPage() {
  const [memoryStats, setMemoryStats] = useState<MemoryStats | null>(null);
  const [recentAudits, setRecentAudits] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [stats, audits] = await Promise.all([
          api.getMemoryStats(),
          api.getRecentAudits(5),
        ]);
        setMemoryStats(stats);
        setRecentAudits(audits.audits || []);
      } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const getRiskBadge = (score: number | null) => {
    if (score === null) return <Badge variant="outline">Pending</Badge>;
    if (score >= 80) return <Badge className="bg-green-600">Low Risk</Badge>;
    if (score >= 50) return <Badge className="bg-yellow-600">Medium Risk</Badge>;
    return <Badge className="bg-red-600">Critical</Badge>;
  };

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Dashboard</h1>
        <p className="text-gray-400">Overview of your security audits and system status</p>
      </div>

      {/* Stats Grid */}
      <div className="mb-8 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card className="border-gray-800 bg-slate-900">
          <CardHeader>
            <CardTitle className="text-white">Total Audits</CardTitle>
            <CardDescription>All time audit count</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-4xl font-bold text-white">{recentAudits.length}</p>
          </CardContent>
        </Card>

        <Card className="border-gray-800 bg-slate-900">
          <CardHeader>
            <CardTitle className="text-white">Memory Patterns</CardTitle>
            <CardDescription>Stored attack patterns</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-4xl font-bold text-white">
              {loading ? "..." : memoryStats?.total_patterns || 0}
            </p>
          </CardContent>
        </Card>

        <Card className="border-gray-800 bg-slate-900">
          <CardHeader>
            <CardTitle className="text-white">System Status</CardTitle>
            <CardDescription>API and memory health</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <div className="h-3 w-3 rounded-full bg-green-500"></div>
              <span className="text-lg font-semibold text-white">
                {memoryStats?.status === "operational" ? "Operational" : "Unavailable"}
              </span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Audits */}
      <Card className="border-gray-800 bg-slate-900">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-white">Recent Audits</CardTitle>
              <CardDescription>Your latest security assessments</CardDescription>
            </div>
            <Link href="/dashboard/new-audit">
              <Button className="bg-cyan-600 hover:bg-cyan-700">
                New Audit
              </Button>
            </Link>
          </div>
        </CardHeader>
        <CardContent>
          {loading ? (
            <p className="text-gray-400">Loading audits...</p>
          ) : recentAudits.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-400 mb-4">No audits yet</p>
              <Link href="/dashboard/new-audit">
                <Button className="bg-cyan-600 hover:bg-cyan-700">
                  Start Your First Audit
                </Button>
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {recentAudits.map((audit) => (
                <div
                  key={audit.audit_id}
                  className="flex items-center justify-between rounded-lg border border-gray-800 p-4 hover:bg-gray-800/50"
                >
                  <div>
                    <h3 className="font-semibold text-white">{audit.target}</h3>
                    <p className="text-sm text-gray-400">{audit.domain}</p>
                  </div>
                  <div className="flex items-center gap-4">
                    {getRiskBadge(audit.compliance_score)}
                    <Link href={`/dashboard/audit/${audit.audit_id}`}>
                      <Button variant="outline" size="sm">
                        View Details
                      </Button>
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <div className="mt-8 grid gap-6 md:grid-cols-2">
        <Card className="border-gray-800 bg-slate-900 hover:bg-slate-800/50 cursor-pointer">
          <Link href="/dashboard/new-audit">
            <CardHeader>
              <div className="mb-2 text-4xl">🛡️</div>
              <CardTitle className="text-white">Start New Audit</CardTitle>
              <CardDescription>
                Launch a new security assessment for your API
              </CardDescription>
            </CardHeader>
          </Link>
        </Card>

        <Card className="border-gray-800 bg-slate-900 hover:bg-slate-800/50 cursor-pointer">
          <Link href="/dashboard/memory">
            <CardHeader>
              <div className="mb-2 text-4xl">💾</div>
              <CardTitle className="text-white">Explore Memory</CardTitle>
              <CardDescription>
                View stored attack patterns and system learning
              </CardDescription>
            </CardHeader>
          </Link>
        </Card>
      </div>
    </div>
  );
}
