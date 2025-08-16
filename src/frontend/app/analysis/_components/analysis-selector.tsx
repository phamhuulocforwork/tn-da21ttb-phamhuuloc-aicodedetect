"use client";

import { useEffect, useState } from "react";

import { Clock, Layers, Sparkles } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Skeleton } from "@/components/ui/skeleton";

import { apiClient, handleApiError } from "@/lib/api-client";
import { AnalysisMethodsResponse } from "@/lib/api-types";

export type AnalysisMode =
  | "combined"
  // | "ast"
  // | "human-style"
  // | "advanced"
  | "gemini";

interface AnalysisSelectorProps {
  value: AnalysisMode;
  onChange: (mode: AnalysisMode) => void;
  disabled?: boolean;
}

const ANALYSIS_MODES: Record<
  AnalysisMode,
  {
    icon: React.ComponentType<{ className?: string }>;
    title: string;
    description: string;
    features: string[];
    timeEstimate: string;
    badge?: string;
  }
> = {
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
  // ast: {
  //   icon: BarChart3,
  //   title: "Phân tích cấu trúc",
  //   description: "Cấu trúc mã, luồng điều khiển và mẫu đặt tên",
  //   features: [
  //     "Structure metrics",
  //     "Control flow",
  //     "Function analysis",
  //     "Variable naming",
  //   ],
  //   timeEstimate: "1-2 giây",
  // },
  // "human-style": {
  //   icon: Brain,
  //   title: "Phân tích phong cách",
  //   description: "Phong cách mã và các điểm không nhất quán kiểu human",
  //   features: [
  //     "Spacing issues",
  //     "Indentation consistency",
  //     "Naming patterns",
  //     "Formatting",
  //   ],
  //   timeEstimate: "1-2 giây",
  // },
  // advanced: {
  //   icon: Zap,
  //   title: "Phân tích độ phức tạp",
  //   description: "Độ phức tạp mã, dư thừa, và phát hiện mẫu AI",
  //   features: [
  //     "Complexity metrics",
  //     "Code redundancy",
  //     "AI patterns",
  //     "Maintainability",
  //   ],
  //   timeEstimate: "2-3 giây",
  // },
  gemini: {
    icon: Sparkles,
    title: "Gemini AI Analysis",
    description:
      "Phân tích bằng Google Gemini AI với khả năng phát hiện patterns",
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
  const [methods, setMethods] = useState<AnalysisMethodsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
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

    fetchMethods();
  }, []);

  if (loading) {
    return (
      <div className='space-y-4'>
        <div className='flex items-center gap-2 mb-4'>
          <Skeleton className='h-5 w-32' />
          <Skeleton className='h-4 w-24' />
        </div>
        <div className='grid gap-4 md:grid-cols-2'>
          {Array.from({ length: 4 }).map((_, i) => (
            <Card key={i}>
              <CardHeader>
                <div className='flex items-start justify-between'>
                  <div className='space-y-2 flex-1'>
                    <Skeleton className='h-5 w-32' />
                    <Skeleton className='h-4 w-full' />
                  </div>
                  <Skeleton className='h-4 w-16' />
                </div>
              </CardHeader>
              <CardContent>
                <div className='space-y-2'>
                  <Skeleton className='h-4 w-24' />
                  <div className='flex flex-wrap gap-1'>
                    {Array.from({ length: 3 }).map((_, j) => (
                      <Skeleton key={j} className='h-6 w-20' />
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
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
        {Object.entries(ANALYSIS_MODES).map(([mode, config]) => {
          const Icon = config.icon;
          const isSelected = value === mode;

          return (
            <div key={mode} className='relative'>
              <RadioGroupItem value={mode} id={mode} className='peer sr-only' />
              <Label
                htmlFor={mode}
                className={`
                  block cursor-pointer
                  ${disabled ? "cursor-not-allowed opacity-50" : ""}
                `}
              >
                <Card
                  className={`
                  transition-all duration-200 hover:shadow-md border-2
                  ${isSelected ? "border-primary ring-2 ring-primary/20" : "border-border hover:border-primary/50"}
                  ${disabled ? "hover:shadow-none hover:border-border" : ""}
                `}
                >
                  <CardHeader className='pb-3'>
                    <div className='flex items-start justify-between'>
                      <div className='flex items-center gap-3'>
                        <div
                          className={`
                          p-2 rounded-md 
                          ${isSelected ? "bg-primary text-primary-foreground" : "bg-muted"}
                        `}
                        >
                          <Icon className='h-4 w-4' />
                        </div>
                        <div>
                          <CardTitle className='text-base'>
                            {config.title}
                          </CardTitle>
                          {config.badge && (
                            <Badge variant='secondary' className='mt-1 text-xs'>
                              {config.badge}
                            </Badge>
                          )}
                        </div>
                      </div>

                      <div className='flex items-center gap-1 text-muted-foreground'>
                        <Clock className='h-3 w-3' />
                        <span className='text-xs'>{config.timeEstimate}</span>
                      </div>
                    </div>

                    <CardDescription className='text-sm'>
                      {config.description}
                    </CardDescription>
                  </CardHeader>

                  <CardContent className='pt-0'>
                    <div className='space-y-3'>
                      <div>
                        <p className='text-xs font-medium text-muted-foreground mb-2'>
                          Gồm các phương pháp:
                        </p>
                        <div className='flex flex-wrap gap-1'>
                          {config.features.map((feature, index) => (
                            <Badge
                              key={index}
                              variant='outline'
                              className='text-xs py-0.5 px-2'
                            >
                              {feature}
                            </Badge>
                          ))}
                        </div>
                      </div>

                      {methods && mode !== "custom" && (
                        <div className='text-xs text-muted-foreground'>
                          {methods.methods.find((m) => m.id === mode)
                            ?.description || config.description}
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </Label>
            </div>
          );
        })}
      </RadioGroup>
    </div>
  );
}

export default AnalysisSelector;
