"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api/client";

export default function AuditHistoryPage() {
  const [audits, setAudits] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await api.getRecentAudits(20);
        setAudits(data.audits || []);
      } catch (error) {
        console.error("Failed to fetch audit history:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const getRiskBadge = (score: number | null) => {
    if (score === null) return <Badge variant="outline">Pending</Badge>;
    if (score >= 80) return <Badge className="bg-green-600">Low Risk</Badge>;
    if (score >= 50) return <Badge className="bg-yellow-600">Medium</Badge>;
    return <Badge className="bg-red-600">Critical</Badge>;
  };

  const formatDate = (isoString: string) => {
    return new Date(isoString).toLocaleString();
  };

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Audit History</h1>
        <p className="text-gray-400">View all your past security audits</p>
      </div>

      {/* Audits List */}
      <Card className="border-gray-800 bg-slate-900">
        <CardHeader>
          <CardTitle className="text-white">All Audits</CardTitle>
          <CardDescription>Complete history of security assessments</CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <p className="text-gray-400">Loading history...</p>
          ) : audits.length === 0 ? (
            <div className="py-12 text-center">
              <p className="mb-4 text-gray-400">No audits found</p>
              <Link href="/dashboard/new-audit">
                <Button className="bg-cyan-600 hover:bg-cyan-700">
                  Start Your First Audit
                </Button>
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {audits.map((audit) => (
                <div
                  key={audit.audit_id}
                  className="rounded-lg border border-gray-800 p-6 transition-colors hover:bg-gray-800/50"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="mb-2 flex items-center gap-3">
                        <h3 className="text-lg font-semibold text-white">{audit.target}</h3>
                        <Badge variant="outline">{audit.domain}</Badge>
                        {getRiskBadge(audit.compliance_score)}
                      </div>
                      <div className="space-y-1 text-sm text-gray-400">
                        <p>Audit ID: {audit.audit_id}</p>
                        <p>Started: {formatDate(audit.started_at)}</p>
                        {audit.compliance_score !== null && (
                          <p className="font-semibold text-white">
                            Score: {audit.compliance_score}/100
                          </p>
                        )}
                      </div>
                    </div>
                    <Link href={`/dashboard/audit/${audit.audit_id}`}>
                      <Button variant="outline">View Results</Button>
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
