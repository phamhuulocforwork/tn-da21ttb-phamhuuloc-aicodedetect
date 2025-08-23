"use client";

import React from "react";

import { Layers, Sparkles } from "lucide-react";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { RadioGroup } from "@/components/ui/radio-group";

import { useAnalysisMethods } from "@/hooks/use-analysis-methods";

import { AnalysisMethodCard } from "./analysis-method-card";
import { AnalysisSelectorLoading } from "./analysis-selector-loading";
import {
  AnalysisMethodConfig,
  AnalysisMode,
  AnalysisSelectorProps,
} from "./types";

const ANALYSIS_MODES: Record<AnalysisMode, AnalysisMethodConfig> = {
  combined: {
    icon: Layers,
    title: "Phân tích đặc trưng",
    description: "Phân tích đặc trưng code và so sánh với baseline dataset",
    features: [
      "Structure Analysis",
      "Style Analysis",
      "Complexity Analysis",
      "Baseline Comparison",
    ],
    timeEstimate: "2-5 giây",
  },
  ai: {
    icon: Sparkles,
    title: "AI Analysis",
    description:
      "Phân tích thông minh với khả năng phát hiện patterns và reasoning chi tiết",
    features: [
      "AI Code Detection",
      "Probability Analysis",
      "Pattern Recognition",
      "Detailed Reasoning",
    ],
    timeEstimate: "3-8 giây",
  },
};

export function AnalysisSelector({
  value,
  onChange,
  disabled = false,
}: AnalysisSelectorProps) {
  const { methods, loading, error } = useAnalysisMethods();

  if (loading) {
    return <AnalysisSelectorLoading />;
  }

  if (error) {
    return (
      <Card className='border-destructive'>
        <CardHeader>
          <CardTitle className='text-destructive'>
            Không thể tải danh sách phương thức phân tích
          </CardTitle>
          <CardDescription>{error}</CardDescription>
        </CardHeader>
        <CardContent>
          <p className='text-sm text-muted-foreground'>
            Đang sử dụng các chế độ phân tích mặc định. Một số tính năng có thể
            không hoạt động.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className='space-y-6'>
      <div className='flex items-center justify-between'>
        <div>
          <h3 className='text-lg font-semibold'>Phương thức phân tích</h3>
        </div>

        {methods && (
          <div className='text-right text-sm text-muted-foreground'>
            <div>
              Ngôn ngữ: {methods.supported_languages.join(", ").toUpperCase()}
            </div>
            <div>Kích thước tối đa: {methods.max_file_size}</div>
          </div>
        )}
      </div>

      <RadioGroup
        value={value}
        onValueChange={(newValue) => onChange(newValue as AnalysisMode)}
        disabled={disabled}
        className='grid gap-4 md:grid-cols-2'
      >
        {Object.entries(ANALYSIS_MODES).map(([mode, config]) => (
          <AnalysisMethodCard
            key={mode}
            mode={mode as AnalysisMode}
            config={config}
            isSelected={value === mode}
            disabled={disabled}
          />
        ))}
      </RadioGroup>
    </div>
  );
}

export default AnalysisSelector;
