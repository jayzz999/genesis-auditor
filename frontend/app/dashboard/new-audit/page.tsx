"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { api, type Domain } from "@/lib/api/client";

export default function NewAuditPage() {
  const router = useRouter();
  const [domains, setDomains] = useState<Domain[]>([]);
  const [selectedDomain, setSelectedDomain] = useState<string>("");
  const [apiName, setApiName] = useState("");
  const [apiUrl, setApiUrl] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchDomains = async () => {
      try {
        const data = await api.getDomains();
        setDomains(data);
      } catch (error) {
        console.error("Failed to fetch domains:", error);
      }
    };

    fetchDomains();
  }, []);

  const handleStartAudit = async () => {
    if (!selectedDomain) {
      alert("Please select a domain");
      return;
    }

    setLoading(true);

    try {
      const response = await api.startAudit({
        domain: selectedDomain,
        target_api_name: apiName || `${selectedDomain} API`,
        target_api_url: apiUrl || undefined,
      });

      // Redirect to audit results page
      router.push(`/dashboard/audit/${response.audit_id}`);
    } catch (error) {
      console.error("Failed to start audit:", error);
      alert("Failed to start audit. Please try again.");
      setLoading(false);
    }
  };

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Create New Audit</h1>
        <p className="text-gray-400">
          Select a compliance domain and configure your target API
        </p>
      </div>

      {/* Domain Selection */}
      <Card className="mb-8 border-gray-800 bg-slate-900">
        <CardHeader>
          <CardTitle className="text-white">Select Domain</CardTitle>
          <CardDescription>Choose the security compliance domain to test</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {domains.map((domain) => (
              <button
                key={domain.id}
                onClick={() => {
                  console.log("Selected domain:", domain.id);
                  setSelectedDomain(domain.id);
                }}
                className={`rounded-lg border-2 p-6 text-left transition-all hover:scale-105 ${
                  selectedDomain === domain.id
                    ? "border-cyan-500 bg-cyan-500/20 ring-2 ring-cyan-500/50"
                    : "border-gray-700 bg-slate-800 hover:border-cyan-600"
                }`}
              >
                <div className="mb-3 text-4xl">{domain.icon}</div>
                <h3 className="mb-2 text-lg font-semibold text-white">{domain.name}</h3>
                <p className="text-sm text-gray-400">{domain.description}</p>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* API Configuration */}
      <Card className="mb-8 border-gray-800 bg-slate-900">
        <CardHeader>
          <CardTitle className="text-white">Target API Configuration</CardTitle>
          <CardDescription>
            Provide details about the API you want to audit
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label htmlFor="api-name" className="text-white">
              API Name (Optional)
            </Label>
            <Input
              id="api-name"
              placeholder="e.g., Healthcare Patient Portal API"
              value={apiName}
              onChange={(e) => setApiName(e.target.value)}
              className="mt-2 border-gray-700 bg-slate-800 text-white"
            />
            <p className="mt-1 text-xs text-gray-400">
              Leave empty to use default name based on domain
            </p>
          </div>

          <div>
            <Label htmlFor="api-url" className="text-white">
              Base URL (Optional)
            </Label>
            <Input
              id="api-url"
              placeholder="e.g., https://api.example.com"
              value={apiUrl}
              onChange={(e) => setApiUrl(e.target.value)}
              className="mt-2 border-gray-700 bg-slate-800 text-white"
            />
            <p className="mt-1 text-xs text-gray-400">
              Leave empty to use example URL for testing
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Selected Configuration Summary */}
      {selectedDomain && (
        <Card className="mb-8 border-cyan-600/50 bg-cyan-950/20">
          <CardHeader>
            <CardTitle className="text-white">Audit Configuration</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="text-gray-400">Domain:</span>
                <Badge className="bg-cyan-600">
                  {domains.find((d) => d.id === selectedDomain)?.name}
                </Badge>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-gray-400">Target:</span>
                <span className="text-white">{apiName || `${selectedDomain} API`}</span>
              </div>
              {apiUrl && (
                <div className="flex items-center gap-2">
                  <span className="text-gray-400">URL:</span>
                  <span className="text-white">{apiUrl}</span>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Action Buttons */}
      <div className="flex gap-4">
        <Button
          onClick={handleStartAudit}
          disabled={!selectedDomain || loading}
          className="bg-cyan-600 hover:bg-cyan-700 disabled:opacity-50"
          size="lg"
        >
          {loading ? (
            <>
              <span className="mr-2">⏳</span>
              Starting Audit...
            </>
          ) : (
            <>
              <span className="mr-2">🚀</span>
              Start Audit
            </>
          )}
        </Button>

        <Button
          onClick={() => router.push("/dashboard")}
          variant="outline"
          size="lg"
          disabled={loading}
        >
          Cancel
        </Button>
      </div>

      {/* Info Box */}
      <Card className="mt-8 border-blue-600/50 bg-blue-950/20">
        <CardContent className="pt-6">
          <div className="flex gap-3">
            <span className="text-2xl">ℹ️</span>
            <div>
              <p className="mb-2 font-semibold text-white">How it works:</p>
              <ul className="space-y-1 text-sm text-gray-400">
                <li>1. Genesis queries Qdrant memory for relevant past attacks</li>
                <li>2. Google Gemini designs a specialized agent swarm for your domain</li>
                <li>3. Agents execute comprehensive security tests</li>
                <li>4. Results are analyzed and compliance score is calculated</li>
                <li>5. Successful attacks are stored in Qdrant for future improvements</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
