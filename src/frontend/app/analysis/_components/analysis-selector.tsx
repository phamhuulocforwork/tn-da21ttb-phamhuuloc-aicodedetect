"use client";

import { useEffect, useState } from "react";

import { BarChart3, Brain, Clock, Layers, Zap } from "lucide-react";

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
  | "ast"
  | "human-style"
  | "advanced"
  | "custom";

interface AnalysisSelectorProps {
  value: AnalysisMode;
  onChange: (mode: AnalysisMode) => void;
  disabled?: boolean;
}

// Predefined analysis modes với descriptions
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
    title: "Deep Analysis",
    description:
      "Comprehensive analysis using all available methods (80+ features)",
    features: [
      "AST Analysis",
      "Human Style",
      "Advanced Features",
      "AI Detection",
    ],
    timeEstimate: "2-5 seconds",
    badge: "Recommended",
  },
  ast: {
    icon: BarChart3,
    title: "Structure Analysis",
    description: "Code structure, control flow, and naming pattern analysis",
    features: [
      "Structure metrics",
      "Control flow",
      "Function analysis",
      "Variable naming",
    ],
    timeEstimate: "1-2 seconds",
  },
  "human-style": {
    icon: Brain,
    title: "Style Analysis",
    description: "Coding style and human-like inconsistency detection",
    features: [
      "Spacing issues",
      "Indentation consistency",
      "Naming patterns",
      "Formatting",
    ],
    timeEstimate: "1-2 seconds",
  },
  advanced: {
    icon: Zap,
    title: "Complexity Analysis",
    description: "Code complexity, redundancy, and AI pattern detection",
    features: [
      "Complexity metrics",
      "Code redundancy",
      "AI patterns",
      "Maintainability",
    ],
    timeEstimate: "2-3 seconds",
  },
  custom: {
    icon: Layers,
    title: "Custom Analysis",
    description: "Select specific analysis methods to combine",
    features: ["Choose your own", "Multiple methods", "Flexible options"],
    timeEstimate: "Variable",
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
            Failed to Load Analysis Methods
          </CardTitle>
          <CardDescription>{error}</CardDescription>
        </CardHeader>
        <CardContent>
          <p className='text-sm text-muted-foreground'>
            Using default analysis modes. Some features may not be available.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className='space-y-6'>
      <div className='flex items-center justify-between'>
        <div>
          <h3 className='text-lg font-semibold'>Analysis Method</h3>
          <p className='text-sm text-muted-foreground'>
            Choose how you want to analyze your code
          </p>
        </div>

        {methods && (
          <div className='text-right text-sm text-muted-foreground'>
            <div>
              Languages: {methods.supported_languages.join(", ").toUpperCase()}
            </div>
            <div>Max size: {methods.max_file_size}</div>
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
                          Features included:
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

                      {/* Show method details from API if available */}
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

      {/* Quick analysis info */}
      {value !== "custom" && (
        <Card className='bg-muted/50'>
          <CardContent className='pt-4'>
            <div className='flex items-start gap-3'>
              <div className='p-2 rounded-md bg-primary/10'>
                <Zap className='h-4 w-4 text-primary' />
              </div>
              <div className='flex-1'>
                <h4 className='font-medium text-sm'>Quick Start</h4>
                <p className='text-xs text-muted-foreground mt-1'>
                  {value === "combined" &&
                    "Get the most comprehensive analysis with all features combined. Best for detailed code review."}
                  {value === "ast" &&
                    "Focus on code structure and organization. Good for checking algorithmic complexity."}
                  {value === "human-style" &&
                    "Detect human coding patterns and inconsistencies. Useful for style analysis."}
                  {value === "advanced" &&
                    "Advanced metrics and AI pattern detection. Best for detecting sophisticated generation."}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

export default AnalysisSelector;
