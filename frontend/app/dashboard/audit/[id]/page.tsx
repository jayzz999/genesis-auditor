"use client";

import { useEffect, useState, use } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { CheckCircle } from "lucide-react";
import { api, type AuditStatus, type WebSocketMessage } from "@/lib/api/client";

type PageProps = {
  params: Promise<{ id: string }>;
};

export default function AuditResultsPage({ params }: PageProps) {
  const resolvedParams = use(params);
  const auditId = resolvedParams.id;
  const router = useRouter();

  const [auditStatus, setAuditStatus] = useState<AuditStatus | null>(null);
  const [progress, setProgress] = useState(0);
  const [currentPhase, setCurrentPhase] = useState("");
  const [phaseMessage, setPhaseMessage] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let ws: WebSocket | null = null;
    let pollInterval: NodeJS.Timeout | null = null;

    const fetchInitialStatus = async () => {
      try {
        const status = await api.getAuditStatus(auditId);
        setAuditStatus(status);

        if (status.status === "completed") {
          setProgress(100);
          setLoading(false);
        } else {
          // Try WebSocket first, but fall back to polling
          try {
            ws = api.connectWebSocket(
              auditId,
              (message: WebSocketMessage) => {
                handleWebSocketMessage(message);
              },
              (error) => {
                console.debug("WebSocket failed, using HTTP polling");
                startPolling();
              },
              () => {
                console.log("WebSocket closed, using HTTP polling");
                startPolling();
              }
            );
          } catch (error) {
            console.log("WebSocket not available, using HTTP polling");
            startPolling();
          }
        }
      } catch (error) {
        console.error("Failed to fetch audit status:", error);
        setLoading(false);
      }
    };

    const startPolling = () => {
      if (pollInterval) return; // Already polling

      pollInterval = setInterval(async () => {
        try {
          const status = await api.getAuditStatus(auditId);
          setAuditStatus(status);

          if (status.status === "completed" || status.status === "failed") {
            setProgress(100);
            setLoading(false);
            if (pollInterval) {
              clearInterval(pollInterval);
              pollInterval = null;
            }
          } else {
            // Simulate progress updates
            setProgress((prev) => Math.min(prev + 5, 90));
          }
        } catch (error) {
          console.error("Polling error:", error);
        }
      }, 2000); // Poll every 2 seconds
    };

    const handleWebSocketMessage = (message: WebSocketMessage) => {
      console.log("WebSocket message:", message);

      if (message.type === "audit_started") {
        setProgress(10);
        setCurrentPhase("Starting");
        setPhaseMessage("Audit initiated");
      } else if (message.type === "phase_update") {
        setCurrentPhase(message.phase || "");
        setPhaseMessage(message.message || "");

        // Update progress based on phase
        if (message.phase === "memory_query") {
          setProgress(25);
        } else if (message.phase === "agent_design") {
          setProgress(50);
        } else if (message.phase === "execution") {
          setProgress(75);
        }
      } else if (message.type === "audit_complete") {
        setProgress(100);
        setCurrentPhase("Completed");
        setPhaseMessage("Audit completed successfully");

        // Update final statistics
        setAuditStatus((prev) => ({
          ...prev!,
          status: "completed",
          statistics: {
            compliance_score: message.compliance_score || 0,
            vulnerabilities_found: message.vulnerabilities_found || 0,
            critical_findings: message.critical_findings || 0,
          },
        }));

        setLoading(false);

        // Fetch complete results after a short delay
        setTimeout(async () => {
          const finalStatus = await api.getAuditStatus(auditId);
          setAuditStatus(finalStatus);
        }, 1000);
      } else if (message.type === "audit_error") {
        setCurrentPhase("Error");
        setPhaseMessage(message.error || "An error occurred");
        setLoading(false);
      }
    };

    fetchInitialStatus();

    return () => {
      if (ws) {
        ws.close();
      }
      if (pollInterval) {
        clearInterval(pollInterval);
      }
    };
  }, [auditId]);

  const getRiskLevel = (score: number) => {
    if (score >= 80) return { label: "Low Risk", color: "bg-green-600" };
    if (score >= 50) return { label: "Medium Risk", color: "bg-yellow-600" };
    return { label: "Critical", color: "bg-red-600" };
  };

  const getPhaseIcon = (phase: string) => {
    switch (phase.toLowerCase()) {
      case "memory_query":
        return "🔍";
      case "agent_design":
        return "🤖";
      case "execution":
        return "⚔️";
      case "completed":
        return "✅";
      case "error":
        return "❌";
      default:
        return "⏳";
    }
  };

  const downloadPDF = async () => {
    try {
      const response = await fetch(`${api.baseUrl}/api/audit/${auditId}/download-pdf`);
      if (!response.ok) {
        throw new Error("Failed to download PDF");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `genesis_audit_${auditId}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error downloading PDF:", error);
      alert("Failed to download PDF report. Please try again.");
    }
  };

  if (!auditStatus) {
    return (
      <div className="flex h-screen items-center justify-center">
        <p className="text-gray-400">Loading audit...</p>
      </div>
    );
  }

  const isCompleted = auditStatus.status === "completed";
  const score = auditStatus.statistics?.compliance_score ?? 0;
  const riskLevel = getRiskLevel(score);

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Audit Results</h1>
          <p className="text-gray-400">
            {auditStatus.target} - {auditStatus.domain}
          </p>
        </div>
        <Button variant="outline" onClick={() => router.push("/dashboard")}>
          Back to Dashboard
        </Button>
      </div>

      {/* Progress Section (shown while running) */}
      {!isCompleted && (
        <Card className="mb-8 border-cyan-600/50 bg-cyan-950/20">
          <CardHeader>
            <CardTitle className="text-white">Audit in Progress</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Progress value={progress} className="h-2" />
            <div className="flex items-center gap-3">
              <span className="text-3xl">{getPhaseIcon(currentPhase)}</span>
              <div>
                <p className="font-semibold text-white">{currentPhase}</p>
                <p className="text-sm text-gray-400">{phaseMessage}</p>
              </div>
            </div>
            <div className="rounded-lg border border-gray-700 bg-slate-800 p-4">
              <p className="mb-2 text-sm font-semibold text-white">Live Status:</p>
              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2">
                  <span>{progress >= 25 ? "✓" : "⏳"}</span>
                  <span className={progress >= 25 ? "text-green-400" : "text-gray-400"}>
                    Querying memory...
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span>{progress >= 50 ? "✓" : "⏳"}</span>
                  <span className={progress >= 50 ? "text-green-400" : "text-gray-400"}>
                    Designing agent swarm...
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span>{progress >= 75 ? "✓" : "⏳"}</span>
                  <span className={progress >= 75 ? "text-green-400" : "text-gray-400"}>
                    Executing attacks...
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span>{progress === 100 ? "✓" : "⏳"}</span>
                  <span className={progress === 100 ? "text-green-400" : "text-gray-400"}>
                    Analyzing results...
                  </span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Results Section (shown when completed) */}
      {isCompleted && auditStatus.statistics && (
        <>
          {/* Compliance Score */}
          <Card className="mb-8 border-gray-800 bg-slate-900">
            <CardContent className="pt-6">
              <div className="text-center">
                <p className="mb-4 text-sm text-gray-400">Compliance Score</p>
                <div className="mb-4">
                  <span className="text-6xl font-bold text-white">{score}</span>
                  <span className="text-2xl text-gray-400">/100</span>
                </div>
                <Badge className={`${riskLevel.color} text-lg px-4 py-2`}>
                  {riskLevel.label}
                </Badge>

                {/* Noveum Evaluation Badge */}
                <div className="mt-6 flex justify-center">
                  <div className="flex items-center gap-2 px-4 py-2 bg-blue-50 border border-blue-200 rounded-full">
                    <span className="text-sm font-medium text-blue-700">
                      Evaluated by Noveum
                    </span>
                    <CheckCircle className="w-5 h-5 text-blue-600" />
                  </div>
                </div>

                <Progress value={score} className="mt-6 h-3" />
              </div>
            </CardContent>
          </Card>

          {/* Statistics Grid */}
          <div className="mb-8 grid gap-6 md:grid-cols-3">
            <Card className="border-gray-800 bg-slate-900">
              <CardHeader>
                <CardTitle className="text-white">Vulnerabilities Found</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-4xl font-bold text-white">
                  {auditStatus.statistics.vulnerabilities_found}
                </p>
              </CardContent>
            </Card>

            <Card className="border-gray-800 bg-slate-900">
              <CardHeader>
                <CardTitle className="text-white">Critical Issues</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-4xl font-bold text-red-500">
                  {auditStatus.statistics.critical_findings}
                </p>
              </CardContent>
            </Card>

            <Card className="border-gray-800 bg-slate-900">
              <CardHeader>
                <CardTitle className="text-white">Risk Level</CardTitle>
              </CardHeader>
              <CardContent>
                <Badge className={`${riskLevel.color} text-xl px-3 py-1`}>
                  {riskLevel.label}
                </Badge>
              </CardContent>
            </Card>
          </div>

          {/* Vulnerabilities List */}
          {auditStatus.vulnerabilities && auditStatus.vulnerabilities.length > 0 && (
            <Card className="mb-8 border-gray-800 bg-slate-900">
              <CardHeader>
                <CardTitle className="text-white">Critical Findings</CardTitle>
                <CardDescription>
                  Top vulnerabilities discovered during the audit
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {auditStatus.vulnerabilities.slice(0, 10).map((vuln, idx) => (
                    <div
                      key={idx}
                      className="rounded-lg border border-red-900/50 bg-red-950/20 p-4"
                    >
                      <div className="mb-2 flex items-center justify-between">
                        <h4 className="font-semibold text-white">
                          {idx + 1}. {vuln.attack_type || "Security Vulnerability"}
                        </h4>
                        <Badge className="bg-red-600">High</Badge>
                      </div>
                      <p className="text-sm text-gray-400">
                        {vuln.description || vuln.payload || "No description available"}
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Actions */}
          <div className="flex gap-4">
            <Button
              className="bg-cyan-600 hover:bg-cyan-700"
              onClick={downloadPDF}
            >
              📄 Download PDF Report
            </Button>
            <Button variant="outline">📧 Email Report</Button>
            <Button
              variant="outline"
              onClick={() => router.push("/dashboard/new-audit")}
            >
              🔁 Run New Audit
            </Button>
          </div>
        </>
      )}
    </div>
  );
}
