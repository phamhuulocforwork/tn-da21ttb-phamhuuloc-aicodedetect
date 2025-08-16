"use client";

import { Minus, TrendingDown, TrendingUp } from "lucide-react";

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

import { BaselineSummary, FeatureInfo } from "@/lib/api-types";

interface BaselineComparisonProps {
  baselineSummary?: BaselineSummary;
  featuresWithComparison: FeatureInfo[];
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
    <div className='space-y-6'>
      {baselineSummary && <BaselineSummaryCard summary={baselineSummary} />}

      {featuresWithComparison.length > 0 && (
        <div className='space-y-4'>
          <div className='flex items-center justify-between'>
            <h3 className='text-lg font-semibold'>So sánh đặc trưng</h3>
            <Badge variant='outline'>
              {featuresWithComparison.length} đặc trưng đã phân tích
            </Badge>
          </div>

          <div className='grid gap-4 md:grid-cols-2 lg:grid-cols-3'>
            {featuresWithComparison.map((feature, index) => (
              <FeatureComparisonCard key={index} feature={feature} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default BaselineComparisonView;
