import React from "react";

import { Repeat } from "lucide-react";

import { SectionHeader } from "@/components/shared/section-header";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";

import { AnalysisResult } from "@/hooks/use-analysis";

import ResultsDashboard from "./results-dashboard";

interface ResultsSectionProps {
  result: AnalysisResult | null;
  loading: boolean;
  error: string | null;
  onRetry: () => void;
  onExportReport: () => void;
  canRetry: boolean;
}

export function ResultsSection({
  result,
  loading,
  error,
  onRetry,
  onExportReport,
  canRetry,
}: ResultsSectionProps) {
  return (
    <div id='results' className='space-y-4'>
      <SectionHeader title='Kết quả phân tích'>
        {result && !loading && (
          <div className='flex items-center gap-2'>
            <Button
              variant='outline'
              size='sm'
              onClick={onRetry}
              disabled={!canRetry}
            >
              <Repeat />
              Phân tích lại
            </Button>
          </div>
        )}
      </SectionHeader>

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
        loading={loading}
        error={error}
        onRetry={onRetry}
        onExportReport={onExportReport}
      />
    </div>
  );
}

export default ResultsSection;
