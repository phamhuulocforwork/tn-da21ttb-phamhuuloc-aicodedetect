"use client";

import { useCallback, useState } from "react";

import { toast } from "sonner";

import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

import {
  apiClient,
  handleApiError,
  isAnalysisResponse,
} from "@/lib/api-client";
import { AnalysisResponse, IndividualAnalysisResponse } from "@/lib/api-types";

import AnalysisSelector, {
  AnalysisMode,
} from "./_components/analysis-selector";
import { CodeEditor } from "./_components/code-editor";
import Header from "./_components/header";
import oneDarkPro from "./_components/onedarkpro.json";
import ResultsDashboard from "./_components/results-dashboard";

export default function AnalysisPage() {
  // State management
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
    AnalysisResponse | IndividualAnalysisResponse | null
  >(null);
  const [error, setError] = useState<string | null>(null);

  // Handle code change
  const handleCodeChange = useCallback(
    (value: string | undefined) => {
      if (value !== undefined) {
        setCode(value);
        // Clear previous results when code changes
        if (result) {
          setResult(null);
        }
      }
    },
    [result],
  );

  // Handle analysis mode change
  const handleAnalysisModeChange = useCallback(
    (mode: AnalysisMode) => {
      setAnalysisMode(mode);
      // Clear previous results when mode changes
      if (result) {
        setResult(null);
      }
    },
    [result],
  );

  // Handle code submission
  const handleSubmitCode = useCallback(
    async (
      code: string,
      language: string,
    ): Promise<AnalysisResponse | IndividualAnalysisResponse> => {
      setIsAnalyzing(true);
      setError(null);

      try {
        // Prepare request
        const request = {
          code,
          filename: `code.${language}`,
          language,
        };

        // Call appropriate API endpoint based on analysis mode
        let response: AnalysisResponse | IndividualAnalysisResponse;

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
          default:
            throw new Error(`Unsupported analysis mode: ${analysisMode}`);
        }

        setResult(response);

        // Show success toast
        const isComprehensive = isAnalysisResponse(response);
        if (isComprehensive) {
          toast.success("Analysis Complete", {
            description: `Overall score: ${Math.round(
              (response as AnalysisResponse).assessment.overall_score * 100,
            )}% AI-like`,
          });
        } else {
          toast.success("Analysis Complete", {
            description: `${
              Object.keys((response as IndividualAnalysisResponse).features)
                .length
            } features extracted`,
          });
        }

        return response;
      } catch (err) {
        const errorMessage = handleApiError(err);
        setError(errorMessage);

        // Show error toast
        toast.error("Analysis Failed", {
          description: errorMessage,
        });

        throw err;
      } finally {
        setIsAnalyzing(false);
      }
    },
    [analysisMode],
  );

  // Handle retry
  const handleRetry = useCallback(() => {
    if (code.trim()) {
      handleSubmitCode(code, "c");
    }
  }, [code, handleSubmitCode]);

  // Handle export report
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

      toast.success("Report Exported", {
        description: "Analysis report downloaded successfully",
      });
    } catch {
      toast.error("Export Failed", {
        description: "Failed to export analysis report",
      });
    }
  }, [result]);

  return (
    <div className='min-h-screen bg-background'>
      <Header />

      <div className='container mx-auto p-4 space-y-6'>
        {/* Analysis Configuration */}
        <div className='space-y-6'>
          <div>
            <h2 className='text-2xl font-bold tracking-tight mb-2'>
              AI Code Detection Analysis
            </h2>
            <p className='text-muted-foreground'>
              Analyze your code to detect AI-generated patterns and assess
              coding style characteristics.
            </p>
          </div>

          {/* Analysis Method Selector */}
          <AnalysisSelector
            value={analysisMode}
            onChange={handleAnalysisModeChange}
            disabled={isAnalyzing}
          />

          <Separator />

          {/* Code Editor */}
          <div className='space-y-4'>
            <div className='flex items-center justify-between'>
              <h3 className='text-lg font-semibold'>Code Input</h3>
              {code.trim() && (
                <div className='text-sm text-muted-foreground'>
                  {code.split("\n").length} lines •{" "}
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
              placeholder='Paste your C/C++ code here to analyze for AI-generated patterns...'
              customDarkTheme={{
                base: "vs-dark",
                inherit: true,
                ...oneDarkPro,
              }}
            />
          </div>
        </div>

        <Separator />

        {/* Results Section */}
        <div className='space-y-4'>
          <div className='flex items-center justify-between'>
            <h3 className='text-lg font-semibold'>Analysis Results</h3>

            {result && !isAnalyzing && (
              <div className='flex items-center gap-2'>
                <Button
                  variant='outline'
                  size='sm'
                  onClick={handleRetry}
                  disabled={!code.trim()}
                >
                  Re-analyze
                </Button>
              </div>
            )}
          </div>

          {/* API Error Alert */}
          {error && (
            <Alert variant='destructive'>
              <AlertDescription>
                <strong>Connection Error:</strong> {error}
                <br />
                <span className='text-sm mt-1 block'>
                  Make sure the backend server is running at
                  http://localhost:8000
                </span>
              </AlertDescription>
            </Alert>
          )}

          {/* Results Dashboard */}
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
