"use client";

import { useEffect, useState } from "react";

import { apiClient, handleApiError } from "@/lib/api-client";
import { AnalysisMethodsResponse } from "@/lib/api-types";

export interface UseAnalysisMethodsReturn {
  methods: AnalysisMethodsResponse | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export function useAnalysisMethods(): UseAnalysisMethodsReturn {
  const [methods, setMethods] = useState<AnalysisMethodsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchMethods = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.getAnalysisMethods();
      setMethods(response);
    } catch (err) {
      setError(handleApiError(err));
      console.error("Failed to fetch analysis methods:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMethods();
  }, []);

  return {
    methods,
    loading,
    error,
    refetch: fetchMethods,
  };
}
