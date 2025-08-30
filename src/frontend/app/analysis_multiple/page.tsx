"use client";

import { FloatingMenu } from "@/components/features/analysis_multiple/floating-menu";
import { MultipleAnalysisPage } from "@/components/features/analysis_multiple/multiple-analysis-page";
import { AnalysisLayout } from "@/components/layout/analysis-layout";

export default function AnalysisMultiplePage() {
  return (
    <AnalysisLayout>
      <MultipleAnalysisPage />
      <FloatingMenu />
    </AnalysisLayout>
  );
}
