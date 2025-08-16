"use client";

import { useCallback, useState } from "react";

import { Repeat } from "lucide-react";
import { toast } from "sonner";

import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

import {
  apiClient,
  handleApiError,
  isAnalysisResponse,
  isGeminiCombinedResponse,
} from "@/lib/api-client";
import {
  AnalysisResponse,
  GeminiCombinedResponse,
  IndividualAnalysisResponse,
} from "@/lib/api-types";

import AnalysisSelector, {
  AnalysisMode,
} from "./_components/analysis-selector";
import { CodeEditor } from "./_components/code-editor";
import Header from "./_components/header";
import oneDarkPro from "./_components/onedarkpro.json";
import ResultsDashboard from "./_components/results-dashboard";

export default function AnalysisPage() {
  const [code, setCode] = useState(`#include <stdio.h>
#include <stdlib.h>

int main() {
    int n, i;
    int sum = 0;
    
    printf("Enter a number: ");
    scanf("%d", &n);
    
    for (i = 1; i <= n; i++) {
        sum += i;
    }
    
    printf("Sum = %d\n", sum);
    return 0;
}`);

  const [analysisMode, setAnalysisMode] = useState<AnalysisMode>("combined");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<
    | AnalysisResponse
    | IndividualAnalysisResponse
    | GeminiCombinedResponse
    | null
  >(null);
  const [error, setError] = useState<string | null>(null);

  const handleCodeChange = useCallback(
    (value: string | undefined) => {
      if (value !== undefined) {
        setCode(value);
        if (result) {
          setResult(null);
        }
      }
    },
    [result],
  );

  const handleAnalysisModeChange = useCallback(
    (mode: AnalysisMode) => {
      setAnalysisMode(mode);
      if (result) {
        setResult(null);
      }
    },
    [result],
  );

  const handleSubmitCode = useCallback(
    async (
      code: string,
      language: string,
    ): Promise<
      AnalysisResponse | IndividualAnalysisResponse | GeminiCombinedResponse
    > => {
      setIsAnalyzing(true);
      setError(null);

      try {
        const request = {
          code,
          filename: `code.${language}`,
          language,
        };

        let response:
          | AnalysisResponse
          | IndividualAnalysisResponse
          | GeminiCombinedResponse;

        switch (analysisMode) {
          case "combined":
            response = await apiClient.analyzeCombined(request);
            break;
          case "ast":
            response = await apiClient.analyzeAst(request);
            break;
          case "human-style":
            response = await apiClient.analyzeHumanStyle(request);
            break;
          case "advanced":
            response = await apiClient.analyzeAdvanced(request);
            break;
          case "gemini":
            response = await apiClient.analyzeGemini(request);
            break;
          default:
            throw new Error(`Unsupported analysis mode: ${analysisMode}`);
        }

        setResult(response);

        const isComprehensive = isAnalysisResponse(response);
        const isGemini = isGeminiCombinedResponse(response);

        if (isGemini) {
          const geminiResponse = response as GeminiCombinedResponse;
          const prediction =
            geminiResponse.gemini_analysis.ai_analysis?.prediction || "Unknown";
          const confidence =
            geminiResponse.gemini_analysis.ai_analysis?.confidence || 0;

          toast.success("Gemini AI Analysis hoàn tất", {
            description: `Prediction: ${prediction} (${Math.round(confidence * 100)}% confidence)`,
          });
        } else if (isComprehensive) {
          toast.success("Phân tích hoàn tất, có", {
            description: `Điểm tổng: ${Math.round(
              (response as AnalysisResponse).assessment.overall_score * 100,
            )}% giống AI`,
          });
        } else {
          toast.success("Phân tích hoàn tất, có", {
            description: `${
              Object.keys((response as IndividualAnalysisResponse).features)
                .length
            } đặc trưng đã được trích xuất`,
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
    [analysisMode],
  );

  const handleRetry = useCallback(() => {
    if (code.trim()) {
      handleSubmitCode(code, "c");
    }
  }, [code, handleSubmitCode]);

  const handleExportReport = useCallback(() => {
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

  return (
    <div className='min-h-screen bg-background'>
      <Header />

      <div id='analysis' className='container mx-auto p-4 space-y-6'>
        <div className='space-y-6'>
          <AnalysisSelector
            value={analysisMode}
            onChange={handleAnalysisModeChange}
            disabled={isAnalyzing}
          />

          <Separator />

          <div className='space-y-4'>
            <div className='flex items-center justify-between'>
              <h3 className='text-lg font-semibold'>Mã nguồn</h3>
              {code.trim() && (
                <div className='text-sm text-muted-foreground'>
                  {code.split("\n").length} dòng • Kích thước:{" "}
                  {Math.round((code.length / 1024) * 10) / 10} KB
                </div>
              )}
            </div>

            <CodeEditor
              value={code}
              height='400px'
              onChange={handleCodeChange}
              onSubmit={handleSubmitCode}
              isSubmitting={isAnalyzing}
              placeholder='Dán mã C/C++ vào đây để phân tích...'
              customDarkTheme={{
                base: "vs-dark",
                inherit: true,
                ...oneDarkPro,
              }}
            />
          </div>
        </div>

        <Separator />

        <div id='results' className='space-y-4'>
          <div className='flex items-center justify-between'>
            <h3 className='text-lg font-semibold'>Kết quả phân tích</h3>

            {result && !isAnalyzing && (
              <div className='flex items-center gap-2'>
                <Button
                  variant='outline'
                  size='sm'
                  onClick={handleRetry}
                  disabled={!code.trim()}
                >
                  <Repeat />
                  Phân tích lại
                </Button>
              </div>
            )}
          </div>

          {error && (
            <Alert variant='destructive'>
              <AlertDescription>
                <strong>Lỗi kết nối:</strong> {error}
                <br />
                <span className='text-sm mt-1 block'>
                  Hãy đảm bảo backend server đang chạy tại{" "}
                  {process.env.NEXT_PUBLIC_API_URL}
                </span>
              </AlertDescription>
            </Alert>
          )}

          <ResultsDashboard
            result={result}
            loading={isAnalyzing}
            error={error}
            onRetry={handleRetry}
            onExportReport={handleExportReport}
          />
        </div>
      </div>
    </div>
  );
}
