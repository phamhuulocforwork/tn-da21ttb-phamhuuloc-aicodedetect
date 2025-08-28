"use client";

import { useCallback, useState } from "react";

import { AnalysisSelector } from "@/components/features/analysis/analysis-selector";
import { CodeInputSection } from "@/components/features/analysis/code-input-section";
import { FloatingMenu } from "@/components/features/analysis/floating-menu";
import { ResultsSection } from "@/components/features/analysis/results-section";
import { AnalysisMode } from "@/components/features/analysis/types";
import { AnalysisLayout } from "@/components/layout/analysis-layout";
import { Separator } from "@/components/ui/separator";

import { useAnalysis } from "@/hooks/use-analysis";

const DEFAULT_CODE = `#include <stdio.h>
#include <stdlib.h>

int main() {
    int n, i;
    int sum = 0;
    
    printf("Enter a number: ");
    scanf("%d", &n);
    
    for (i = 1; i <= n; i++) {
        sum += i;
    }
    
    printf("Sum = %d", sum);
    return 0;
}`;

export default function AnalysisPage() {
  const [code, setCode] = useState(DEFAULT_CODE);
  const [analysisMode, setAnalysisMode] = useState<AnalysisMode>("combined");

  const {
    isAnalyzing,
    result,
    error,
    submitCode,
    retry,
    exportReport,
    clearResult,
  } = useAnalysis();

  const handleCodeChange = useCallback(
    (value: string | undefined) => {
      if (value !== undefined) {
        setCode(value);
        if (result) {
          clearResult();
        }
      }
    },
    [result, clearResult],
  );

  const handleAnalysisModeChange = useCallback(
    (mode: AnalysisMode) => {
      setAnalysisMode(mode);
      if (result) {
        clearResult();
      }
    },
    [result, clearResult],
  );

  const handleSubmitCode = useCallback(
    async (code: string, language: string) => {
      return await submitCode(code, language, analysisMode);
    },
    [submitCode, analysisMode],
  );

  const handleRetry = useCallback(() => {
    retry(code, "c", analysisMode);
  }, [code, analysisMode, retry]);

  const handleFileContentLoaded = useCallback(
    (content: string, filename: string) => {
      setCode(content);
      if (
        filename.endsWith(".cpp") ||
        filename.endsWith(".c") ||
        filename.endsWith(".cxx")
      ) {
      }
    },
    [],
  );

  return (
    <AnalysisLayout>
      <div id='analysis' className='container mx-auto p-4 space-y-6'>
        <div className='space-y-6'>
          <AnalysisSelector
            value={analysisMode}
            onChange={handleAnalysisModeChange}
            disabled={isAnalyzing}
          />

          <Separator />

          <CodeInputSection
            code={code}
            onCodeChange={handleCodeChange}
            onSubmit={handleSubmitCode}
            isSubmitting={isAnalyzing}
            analysisMode={analysisMode}
            onFileContentLoaded={handleFileContentLoaded}
          />
        </div>

        <Separator />

        <ResultsSection
          result={result}
          loading={isAnalyzing}
          error={error}
          onRetry={handleRetry}
          onExportReport={exportReport}
          canRetry={code.trim().length > 0}
        />

        <FloatingMenu />
      </div>
    </AnalysisLayout>
  );
}
