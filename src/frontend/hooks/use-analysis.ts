"use client";

import { useCallback, useState } from "react";

import { toast } from "sonner";

import { AnalysisMode } from "@/components/features/analysis/types";

import {
  apiClient,
  handleApiError,
  isAIMDXResponse,
  isAnalysisResponse,
} from "@/lib/api-client";
import {
  AIMDXResponse,
  AnalysisResponse,
  IndividualAnalysisResponse,
} from "@/lib/api-types";

export type AnalysisResult =
  | AnalysisResponse
  | IndividualAnalysisResponse
  | AIMDXResponse;

export interface UseAnalysisReturn {
  isAnalyzing: boolean;
  result: AnalysisResult | null;
  error: string | null;
  submitCode: (
    code: string,
    language: string,
    mode: AnalysisMode,
  ) => Promise<AnalysisResult>;
  retry: (code: string, language: string, mode: AnalysisMode) => Promise<void>;
  exportReport: () => void;
  clearResult: () => void;
  clearError: () => void;
}

export function useAnalysis(): UseAnalysisReturn {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const submitCode = useCallback(
    async (
      code: string,
      language: string,
      mode: AnalysisMode,
    ): Promise<AnalysisResult> => {
      setIsAnalyzing(true);
      setError(null);

      try {
        const request = {
          code,
          filename: `code.${language}`,
          language,
        };

        let response: AnalysisResult;

        switch (mode) {
          case "combined":
            response = await apiClient.analyzeCombined(request);
            break;
          case "ai":
            response = await apiClient.analyzeAI(request);
            break;
          default:
            throw new Error(`Unsupported analysis mode: ${mode}`);
        }

        setResult(response);

        const isComprehensive = isAnalysisResponse(response);
        const isAI = isAIMDXResponse(response);

        if (isAI) {
          toast.success("AI Analysis hoàn tất", {
            description:
              "Phân tích AI đã hoàn thành, xem kết quả ở tab AI Analysis",
          });
        } else if (isComprehensive) {
          toast.success("Phân tích hoàn tất", {
            description: `Điểm tổng: ${Math.round(
              (response as AnalysisResponse).assessment.overall_score * 100,
            )}% giống AI`,
          });
        }

        return response;
      } catch (err) {
        const errorMessage = handleApiError(err);
        setError(errorMessage);

        toast.error("Không thể phân tích", {
          description: errorMessage,
        });

        throw err;
      } finally {
        setIsAnalyzing(false);
      }
    },
    [],
  );

  const retry = useCallback(
    async (code: string, language: string, mode: AnalysisMode) => {
      if (code.trim()) {
        await submitCode(code, language, mode);
      }
    },
    [submitCode],
  );

  const exportReport = useCallback(() => {
    if (!result) return;

    try {
      const reportData = {
        analysis: result,
        exported_at: new Date().toISOString(),
        export_version: "1.0",
      };

      const blob = new Blob([JSON.stringify(reportData, null, 2)], {
        type: "application/json",
      });

      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `analysis-report-${result.analysis_id}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      toast.success("Đã xuất báo cáo", {
        description: "Tải xuống báo cáo phân tích thành công",
      });
    } catch {
      toast.error("Không thể xuất báo cáo", {
        description: "Không thể xuất báo cáo phân tích",
      });
    }
  }, [result]);

  const clearResult = useCallback(() => {
    setResult(null);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    isAnalyzing,
    result,
    error,
    submitCode,
    retry,
    exportReport,
    clearResult,
    clearError,
  };
}
