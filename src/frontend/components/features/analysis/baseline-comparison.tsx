"use client";

import * as React from "react";

import * as echarts from "echarts/core";
import { ParallelChart } from "echarts/charts";
import {
  LegendComponent,
  ParallelComponent,
  TooltipComponent,
  VisualMapComponent,
} from "echarts/components";
import type { EChartsCoreOption } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { ChartLine, Minus, TrendingDown, TrendingUp } from "lucide-react";

import { CollapsibleFilter } from "@/components/customized/collapsible/collapsible";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";

import { BaselineSummary, FeatureGroup, FeatureInfo } from "@/lib/api-types";

interface BaselineComparisonProps {
  baselineSummary?: BaselineSummary;
  featuresWithComparison: FeatureInfo[];
  featureGroups?: Record<string, FeatureGroup>;
}

echarts.use([
  TooltipComponent,
  ParallelComponent,
  VisualMapComponent,
  LegendComponent,
  ParallelChart,
  CanvasRenderer,
]);

function useParallelChart(
  containerId: string,
  features: FeatureInfo[],
  title: string,
) {
  const ref = React.useRef<HTMLDivElement | null>(null);

  React.useEffect(() => {
    if (!ref.current) return;
    const chart = echarts.init(ref.current as HTMLDivElement, "dark");

    const CHART_COLORS = {
      red: "#ef4444",
      green: "#22c55e",
      blue: "#3b82f6",
    } as const;

    const filtered = features.filter((f) => {
      const current = f.baseline_comparison?.current_value ?? f.value;
      if (!Number.isFinite(current)) return false;
      if (current === 999 || current === 0) return false;
      return true;
    });

    const formatTick = (v: number) => {
      if (!Number.isFinite(v)) return "";
      const abs = Math.abs(v);
      if (abs >= 1000) return `${Math.round(v)}`;
      if (abs >= 100) return v.toFixed(0);
      if (abs >= 1) return v.toFixed(2);
      return v.toFixed(3);
    };

    const dims = filtered.map((f, i) => {
      const label = f.name.replace(/_/g, " ");
      const valsRaw = [
        f.baseline_comparison?.ai_baseline,
        f.baseline_comparison?.human_baseline,
        f.baseline_comparison?.current_value ?? f.value,
      ].filter((v) => typeof v === "number" && !Number.isNaN(v)) as number[];

      let min = valsRaw.length ? Math.min(...valsRaw) : 0;
      let max = valsRaw.length ? Math.max(...valsRaw) : 1;
      if (!Number.isFinite(min)) min = 0;
      if (!Number.isFinite(max)) max = 1;

      if (min === max) {
        if (max === 0) {
          max = 1;
        } else {
          const delta = Math.abs(max) * 0.1 || 1;
          min = max - delta;
          max = max + delta;
        }
      } else {
        const pad = (max - min) * 0.1;
        min = min - pad;
        max = max + pad;
      }

      const useLog = max > 100 && min > 0.0001;
      const axis: Record<string, unknown> = {
        dim: i,
        name: label,
        min: useLog ? Math.max(0.0001, min) : min,
        max,
        axisLabel: {
          color: "#bbb",
          fontSize: 10,
          formatter: (val: number) => formatTick(Number(val)),
        },
      };
      if (useLog) {
        axis.type = "log";
        (axis as any).logBase = 10;
      }
      return axis;
    });

    const aiRow = filtered.map(
      (f) => f.baseline_comparison?.ai_baseline ?? NaN,
    );
    const humanRow = filtered.map(
      (f) => f.baseline_comparison?.human_baseline ?? NaN,
    );
    const currentRow = filtered.map(
      (f) => f.baseline_comparison?.current_value ?? f.value,
    );

    const option: EChartsCoreOption = {
      backgroundColor: "transparent",
      tooltip: { trigger: "item" },
      legend: {
        bottom: 0,
        data: ["AI baseline", "Human baseline", "Current code"],
        textStyle: { color: "#bbb" },
      },
      color: [CHART_COLORS.red, CHART_COLORS.green, CHART_COLORS.blue],
      parallelAxis: dims,
      parallel: {
        left: "3%",
        right: "6%",
        height: 220,
        parallelAxisDefault: {
          nameLocation: "end",
          nameTextStyle: { color: "#bbb", fontSize: 10 },
          axisLine: { lineStyle: { color: "#666" } },
          axisLabel: { color: "#bbb", fontSize: 10 },
        },
      },
      series: [
        {
          name: "AI baseline",
          type: "parallel",
          lineStyle: { width: 1.5, opacity: 0.8, color: CHART_COLORS.red },
          data: [aiRow],
        },
        {
          name: "Human baseline",
          type: "parallel",
          lineStyle: { width: 1.5, opacity: 0.8, color: CHART_COLORS.green },
          data: [humanRow],
        },
        {
          name: "Current code",
          type: "parallel",
          lineStyle: { width: 2, opacity: 0.9, color: CHART_COLORS.blue },
          data: [currentRow],
        },
      ],
    };

    chart.setOption(option);

    const handler = () => chart.resize();
    window.addEventListener("resize", handler);
    return () => {
      window.removeEventListener("resize", handler);
      chart.dispose();
    };
  }, [containerId, features]);

  return ref;
}

const getVerdictColor = (verdict: string): string => {
  switch (verdict) {
    case "ai-like":
      return "text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-950/20";
    case "human-like":
      return "text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-950/20";
    default:
      return "text-yellow-600 dark:text-yellow-400 bg-yellow-50 dark:bg-yellow-950/20";
  }
};

const getVerdictIcon = (verdict: string) => {
  switch (verdict) {
    case "ai-like":
      return <TrendingUp className='h-4 w-4' />;
    case "human-like":
      return <TrendingDown className='h-4 w-4' />;
    default:
      return <Minus className='h-4 w-4' />;
  }
};

function FeatureComparisonCard({ feature }: { feature: FeatureInfo }) {
  if (!feature.baseline_comparison) {
    return null;
  }

  const comparison = feature.baseline_comparison;
  const verdictColorClass = getVerdictColor(comparison.verdict);

  return (
    <Card className='hover:shadow-md transition-shadow'>
      <CardHeader className='pb-3'>
        <div className='flex items-start justify-between'>
          <div>
            <CardTitle className='text-sm font-medium'>
              {feature.name}
            </CardTitle>
            <CardDescription className='text-xs'>
              Code hiện tại: {feature.value.toFixed(3)}
            </CardDescription>
          </div>
          <Badge className={`${verdictColorClass} border-0 text-xs`}>
            {getVerdictIcon(comparison.verdict)}
            <span className='ml-1'>{comparison.verdict}</span>
          </Badge>
        </div>
      </CardHeader>

      <CardContent className='space-y-4'>
        <div className='space-y-2'>
          <div className='flex justify-between text-xs text-muted-foreground'>
            <span>Baseline AI</span>
            <span>Baseline human</span>
          </div>

          <div className='relative h-8 bg-gradient-to-r from-red-100 to-green-100 dark:from-red-950/30 dark:to-green-950/30 rounded-md'>
            <div
              className='absolute top-0 bottom-0 w-0.5 bg-red-500'
              style={{ left: "10%" }}
            />

            <div
              className='absolute top-0 bottom-0 w-0.5 bg-green-500'
              style={{ left: "90%" }}
            />

            <div
              className='absolute top-1 bottom-1 w-1 bg-blue-500 rounded-sm'
              style={{
                left: `${
                  10 +
                  (comparison.ai_similarity > comparison.human_similarity
                    ? 10 + comparison.ai_similarity * 30
                    : 50 + comparison.human_similarity * 30)
                }%`,
              }}
            />
          </div>

          <div className='flex justify-between text-xs'>
            <span className='text-red-600 dark:text-red-400'>
              {comparison.ai_baseline.toFixed(3)}
            </span>
            <span className='text-blue-600 dark:text-blue-400 font-medium'>
              Code hiện tại: {comparison.current_value.toFixed(3)}
            </span>
            <span className='text-green-600 dark:text-green-400'>
              {comparison.human_baseline.toFixed(3)}
            </span>
          </div>
        </div>

        <Separator />

        <div className='space-y-3'>
          <div>
            <div className='flex justify-between text-xs mb-1'>
              <span>Độ tương đồng với AI</span>
              <span>{Math.round(comparison.ai_similarity * 100)}%</span>
            </div>
            <Progress value={comparison.ai_similarity * 100} className='h-2' />
          </div>

          <div>
            <div className='flex justify-between text-xs mb-1'>
              <span>Độ tương đồng với người</span>
              <span>{Math.round(comparison.human_similarity * 100)}%</span>
            </div>
            <Progress
              value={comparison.human_similarity * 100}
              className='h-2'
            />
          </div>
        </div>

        <div className='p-3 bg-muted/50 rounded-md'>
          <p className='text-xs text-muted-foreground'>
            {comparison.explanation}
          </p>
          <div className='flex justify-between mt-2 text-xs'>
            <span>Độ tin cậy: {Math.round(comparison.confidence * 100)}%</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function BaselineSummaryCard({ summary }: { summary: BaselineSummary }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className='flex items-center gap-2'>
          <TrendingUp className='h-5 w-5' />
          Tổng quan so sánh Baseline
        </CardTitle>
        <CardDescription>
          Mức độ tương đồng tổng quan giữa mẫu AI và người
        </CardDescription>
      </CardHeader>

      <CardContent className='space-y-6'>
        <div className='grid gap-4 md:grid-cols-2'>
          <div className='text-center p-4 bg-red-50 dark:bg-red-950/20 rounded-lg'>
            <div className='text-2xl font-bold text-red-600 dark:text-red-400'>
              {Math.round(summary.overall_ai_similarity * 100)}%
            </div>
            <div className='text-sm text-muted-foreground'>
              Độ tương đồng với AI
            </div>
          </div>

          <div className='text-center p-4 bg-green-50 dark:bg-green-950/20 rounded-lg'>
            <div className='text-2xl font-bold text-green-600 dark:text-green-400'>
              {Math.round(summary.overall_human_similarity * 100)}%
            </div>
            <div className='text-sm text-muted-foreground'>
              Độ tương đồng với người
            </div>
          </div>
        </div>

        <Separator />

        <div className='space-y-4'>
          <h4 className='font-semibold text-sm'>Phân rã đặc trưng</h4>

          <div className='grid gap-3 md:grid-cols-3'>
            <div className='text-center p-3 bg-muted/50 rounded-lg'>
              <div className='text-xl font-bold text-red-600 dark:text-red-400'>
                {summary.ai_like_features}
              </div>
              <div className='text-xs text-muted-foreground'>Giống AI</div>
            </div>

            <div className='text-center p-3 bg-muted/50 rounded-lg'>
              <div className='text-xl font-bold text-green-600 dark:text-green-400'>
                {summary.human_like_features}
              </div>
              <div className='text-xs text-muted-foreground'>Giống người</div>
            </div>

            <div className='text-center p-3 bg-muted/50 rounded-lg'>
              <div className='text-xl font-bold text-yellow-600 dark:text-yellow-400'>
                {summary.neutral_features}
              </div>
              <div className='text-xs text-muted-foreground'>Trung lập</div>
            </div>
          </div>
        </div>

        <Separator />

        <div className='space-y-4'>
          <h4 className='font-semibold text-sm'>Các đặc trưng mạnh</h4>

          <div className='grid gap-4 md:grid-cols-2'>
            <div>
              <h5 className='text-xs font-medium text-red-600 dark:text-red-400 mb-2'>
                Đặc trưng giống AI:
              </h5>
              <div className='space-y-1'>
                {summary.strongest_ai_indicators.map((feature, index) => (
                  <Badge key={index} variant='secondary' className='text-xs'>
                    {feature}
                  </Badge>
                ))}
                {summary.strongest_ai_indicators.length === 0 && (
                  <p className='text-xs text-muted-foreground'>
                    Không phát hiện
                  </p>
                )}
              </div>
            </div>

            <div>
              <h5 className='text-xs font-medium text-green-600 dark:text-green-400 mb-2'>
                Đặc trưng giống người:
              </h5>
              <div className='space-y-1'>
                {summary.strongest_human_indicators.map((feature, index) => (
                  <Badge key={index} variant='secondary' className='text-xs'>
                    {feature}
                  </Badge>
                ))}
                {summary.strongest_human_indicators.length === 0 && (
                  <p className='text-xs text-muted-foreground'>
                    Không phát hiện đặc trưng
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export function BaselineComparisonView({
  baselineSummary,
  featuresWithComparison,
  featureGroups,
}: BaselineComparisonProps) {
  if (!baselineSummary && featuresWithComparison.length === 0) {
    return (
      <Card className='border-dashed'>
        <CardContent className='flex flex-col items-center justify-center py-12 text-center'>
          <TrendingUp className='h-12 w-12 text-muted-foreground mb-4' />
          <h3 className='text-lg font-semibold mb-2'>
            Không có dữ liệu Baseline
          </h3>
          <p className='text-muted-foreground max-w-md'>
            So sánh baseline cần mô hình phân tích sâu. Hãy thử phân tích sâu để
            xem chi tiết.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className='divide-y-2 space-y-4'>
      {baselineSummary && <BaselineSummaryCard summary={baselineSummary} />}

      {featureGroups &&
        Object.keys(featureGroups).length > 0 &&
        (() => {
          const allWithBaseline: FeatureInfo[] = Object.values(featureGroups)
            .flatMap((g) => g.features)
            .filter((f) => !!f.baseline_comparison);
          if (allWithBaseline.length === 0) return null;

          const sorted = [...allWithBaseline].sort((a, b) => {
            const aDiff = a.baseline_comparison
              ? Math.abs(
                  a.baseline_comparison.ai_baseline -
                    a.baseline_comparison.human_baseline,
                ) * (a.baseline_comparison.confidence || 1)
              : 0;
            const bDiff = b.baseline_comparison
              ? Math.abs(
                  b.baseline_comparison.ai_baseline -
                    b.baseline_comparison.human_baseline,
                ) * (b.baseline_comparison.confidence || 1)
              : 0;
            return bDiff - aDiff;
          });

          const topK = 14;
          const topFeatures = sorted.slice(0, topK);
          const ref = useParallelChart(
            `top-parallel`,
            topFeatures,
            `Top features`,
          );

          return (
            <Card>
              <CardHeader>
                <CardTitle className='flex items-center justify-between'>
                  Top Features (Overall)
                  <Badge variant='secondary'>{topFeatures.length}</Badge>
                </CardTitle>
                <CardDescription>
                  Các đặc trưng phân biệt AI vs Human mạnh nhất theo baseline
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div ref={ref} className='w-full h-[380px] rounded-md border' />
              </CardContent>
            </Card>
          );
        })()}

      {featureGroups && Object.keys(featureGroups).length > 0 && (
        <div className='space-y-4'>
          <div className='space-y-6'>
            {Object.entries(featureGroups).map(([key, group]) => {
              const withBaseline = group.features.filter(
                (f) => !!f.baseline_comparison,
              );
              if (withBaseline.length === 0) return null;

              const sorted = [...withBaseline].sort((a, b) => {
                const aDiff = a.baseline_comparison
                  ? Math.abs(
                      a.baseline_comparison.ai_baseline -
                        a.baseline_comparison.human_baseline,
                    )
                  : 0;
                const bDiff = b.baseline_comparison
                  ? Math.abs(
                      b.baseline_comparison.ai_baseline -
                        b.baseline_comparison.human_baseline,
                    )
                  : 0;
                return bDiff - aDiff;
              });

              const chunkSize = 14;
              const chunks: FeatureInfo[][] = [];
              for (let i = 0; i < sorted.length; i += chunkSize) {
                chunks.push(sorted.slice(i, i + chunkSize));
              }

              return (
                <Card key={key}>
                  <CardHeader>
                    <CardTitle className='flex items-center justify-between'>
                      {group.group_name}
                      <Badge variant='secondary'>
                        {withBaseline.length} features
                      </Badge>
                    </CardTitle>
                    <CardDescription>
                      So sánh đa chiều giữa AI baseline, Human baseline và code
                      hiện tại
                    </CardDescription>
                  </CardHeader>
                  <CardContent className='space-y-4'>
                    {chunks.map((features, idx) => {
                      const ref = useParallelChart(
                        `${key}-parallel-${idx}`,
                        features,
                        `${group.group_name} #${idx + 1}`,
                      );
                      return (
                        <div key={idx} className='w-full'>
                          <div className='text-xs text-muted-foreground mb-2'>
                            Nhóm {idx + 1}/{chunks.length}
                          </div>
                          <div
                            ref={ref}
                            className='w-full h-[350px] rounded-md border'
                          />
                        </div>
                      );
                    })}
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      )}

      <CollapsibleFilter
        title='So sánh đặc trưng'
        icon={ChartLine}
        defaultOpen={false}
      >
        {featuresWithComparison.length > 0 && (
          <div className='space-y-4'>
            <div className='grid gap-4 md:grid-cols-2 lg:grid-cols-3'>
              {featuresWithComparison.map((feature, index) => (
                <FeatureComparisonCard key={index} feature={feature} />
              ))}
            </div>
          </div>
        )}
      </CollapsibleFilter>
    </div>
  );
}

export default BaselineComparisonView;
