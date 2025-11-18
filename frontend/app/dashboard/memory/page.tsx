"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { api, type Domain, type MemoryStats } from "@/lib/api/client";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function MemoryPage() {
  const [memoryStats, setMemoryStats] = useState<MemoryStats | null>(null);
  const [domains, setDomains] = useState<Domain[]>([]);
  const [selectedDomain, setSelectedDomain] = useState<string>("");
  const [patterns, setPatterns] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [stats, domainsData] = await Promise.all([
          api.getMemoryStats(),
          api.getDomains(),
        ]);
        setMemoryStats(stats);
        setDomains(domainsData);
        if (domainsData.length > 0) {
          setSelectedDomain(domainsData[0].id);
        }
      } catch (error) {
        console.error("Failed to fetch memory data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    if (selectedDomain) {
      const fetchPatterns = async () => {
        try {
          const data = await api.getMemoryPatterns(selectedDomain, 20);
          setPatterns(data.patterns || []);
        } catch (error) {
          console.error("Failed to fetch patterns:", error);
        }
      };

      fetchPatterns();
    }
  }, [selectedDomain]);

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Memory System</h1>
        <p className="text-gray-400">
          Explore stored attack patterns and system learning
        </p>
      </div>

      {/* Stats Overview */}
      <div className="mb-8 grid gap-6 md:grid-cols-3">
        <Card className="border-gray-800 bg-slate-900">
          <CardHeader>
            <CardTitle className="text-white">Total Patterns</CardTitle>
            <CardDescription>Stored in vector database</CardDescription>
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
            <CardDescription>Qdrant memory system</CardDescription>
          </CardHeader>
          <CardContent>
            <Badge
              className={
                memoryStats?.status === "operational"
                  ? "bg-green-600"
                  : "bg-red-600"
              }
            >
              {memoryStats?.status || "Unknown"}
            </Badge>
          </CardContent>
        </Card>

        <Card className="border-gray-800 bg-slate-900">
          <CardHeader>
            <CardTitle className="text-white">Collection</CardTitle>
            <CardDescription>Vector collection name</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-white">
              {memoryStats?.collection_name || "genesis_attacks"}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Domain Tabs */}
      <Card className="border-gray-800 bg-slate-900">
        <CardHeader>
          <CardTitle className="text-white">Attack Patterns by Domain</CardTitle>
          <CardDescription>
            Browse stored successful attacks for each compliance domain
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs value={selectedDomain} onValueChange={setSelectedDomain}>
            <TabsList className="mb-6">
              {domains.map((domain) => (
                <TabsTrigger key={domain.id} value={domain.id}>
                  <span className="mr-2">{domain.icon}</span>
                  {domain.name}
                </TabsTrigger>
              ))}
            </TabsList>

            {domains.map((domain) => (
              <TabsContent key={domain.id} value={domain.id}>
                <div className="space-y-4">
                  {patterns.length === 0 ? (
                    <p className="py-8 text-center text-gray-400">
                      No patterns stored for this domain yet
                    </p>
                  ) : (
                    patterns.map((pattern, idx) => (
                      <div
                        key={idx}
                        className="rounded-lg border border-gray-700 bg-slate-800 p-4"
                      >
                        <div className="mb-2 flex items-center justify-between">
                          <h4 className="font-semibold text-white">
                            {pattern.metadata?.attack_type || "Attack Pattern"}
                          </h4>
                          <Badge variant="outline">
                            Score: {pattern.score?.toFixed(3) || "N/A"}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-400">
                          {pattern.payload?.description || pattern.payload || "No description"}
                        </p>
                      </div>
                    ))
                  )}
                </div>
              </TabsContent>
            ))}
          </Tabs>
        </CardContent>
      </Card>

      {/* Info Box */}
      <Card className="mt-8 border-cyan-600/50 bg-cyan-950/20">
        <CardContent className="pt-6">
          <div className="flex gap-3">
            <span className="text-2xl">🧠</span>
            <div>
              <p className="mb-2 font-semibold text-white">How Memory Works:</p>
              <ul className="space-y-1 text-sm text-gray-400">
                <li>
                  • Successful attacks are automatically stored in Qdrant vector database
                </li>
                <li>
                  • Each pattern is embedded using OpenAI embeddings for semantic search
                </li>
                <li>
                  • Future audits query memory to leverage past successful attacks
                </li>
                <li>
                  • System improves over time as more patterns are discovered
                </li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
