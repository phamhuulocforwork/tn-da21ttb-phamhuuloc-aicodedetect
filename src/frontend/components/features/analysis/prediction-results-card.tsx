"use client";

import React from "react";

import {
  AlertCircle,
  Brain,
  FileText,
  TrendingDown,
  TrendingUp,
} from "lucide-react";

import { Alert, AlertDescription } from "@/components/ui/alert";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";

interface PredictionResults {
  prediction: string;
  confidence: string;
  aiProbability: string;
  humanProbability: string;
}

interface PredictionResultsCardProps {
  mdxContent: string;
  className?: string;
}

export function PredictionResultsCard({
  mdxContent,
  className = "",
}: PredictionResultsCardProps) {
  const parsePredictionResults = (
    content: string,
  ): PredictionResults | null => {
    try {
      const lines = content.split("\n");

      let inPredictionSection = false;
      const results: Partial<PredictionResults> = {};

      for (const line of lines) {
        const trimmedLine = line.trim();

        if (trimmedLine.includes("## Kết quả dự đoán")) {
          inPredictionSection = true;
          continue;
        }

        if (
          inPredictionSection &&
          trimmedLine.startsWith("## ") &&
          !trimmedLine.includes("Kết quả dự đoán")
        ) {
          break;
        }

        if (inPredictionSection) {
          if (trimmedLine.startsWith("**Dự đoán:**")) {
            results.prediction = trimmedLine.replace("**Dự đoán:**", "").trim();
          } else if (trimmedLine.startsWith("**Độ tin cậy:**")) {
            results.confidence = trimmedLine
              .replace("**Độ tin cậy:**", "")
              .replace("%", "")
              .trim();
          } else if (trimmedLine.startsWith("**Xác suất là AI viết:**")) {
            results.aiProbability = trimmedLine
              .replace("**Xác suất là AI viết:**", "")
              .replace("%", "")
              .trim();
          } else if (trimmedLine.startsWith("**Xác suất là người viết:**")) {
            results.humanProbability = trimmedLine
              .replace("**Xác suất là người viết:**", "")
              .replace("%", "")
              .trim();
          }
        }
      }

      if (
        results.prediction &&
        results.confidence &&
        results.aiProbability &&
        results.humanProbability
      ) {
        return results as PredictionResults;
      }

      return null;
    } catch (error) {
      console.error("Error parsing prediction results:", error);
      return null;
    }
  };

  const predictionResults = parsePredictionResults(mdxContent);

  if (!predictionResults) {
    return (
      <Alert>
        <AlertCircle className='h-4 w-4' />
        <AlertDescription>
          Không thể phân tích kết quả dự đoán từ nội dung MDX. Vui lòng thử lại.
        </AlertDescription>
      </Alert>
    );
  }

  const aiProb = parseInt(predictionResults.aiProbability) || 0;
  const humanProb = parseInt(predictionResults.humanProbability) || 0;

  return (
    <div className={`space-y-6 ${className}`}>
      <Card className='border-2 border-primary/20 bg-gradient-to-br from-primary/5 to-primary/10'>
        <CardContent className='space-y-8'>
          <div className='grid grid-cols-1 md:grid-cols-2 gap-6'>
            <div className='space-y-4'>
              <div className='flex items-center gap-3'>
                <div className='p-2 rounded-full bg-red-100 dark:bg-red-900/20'>
                  <Brain className='h-4 w-4 text-red-600 dark:text-red-400' />
                </div>
                <div className='flex-1'>
                  <div className='text-lg font-bold text-red-600 dark:text-red-400'>
                    {predictionResults.aiProbability}%
                  </div>
                  <div className='text-xs text-muted-foreground'>
                    Xác suất AI viết
                  </div>
                </div>
              </div>
              <Progress
                value={aiProb}
                className='h-2 bg-red-100 dark:bg-red-900/20'
              />
            </div>

            <div className='space-y-4'>
              <div className='flex items-center gap-3'>
                <div className='p-2 rounded-full bg-green-100 dark:bg-green-900/20'>
                  <FileText className='h-4 w-4 text-green-600 dark:text-green-400' />
                </div>
                <div className='flex-1'>
                  <div className='text-lg font-bold text-green-600 dark:text-green-400'>
                    {predictionResults.humanProbability}%
                  </div>
                  <div className='text-xs text-muted-foreground'>
                    Xác suất người viết
                  </div>
                </div>
              </div>
              <Progress
                value={humanProb}
                className='h-2 bg-green-100 dark:bg-green-900/20'
              />
            </div>
          </div>

          <div className='flex items-center justify-center gap-2 pt-2'>
            {aiProb > humanProb ? (
              <TrendingUp className='h-4 w-4 text-red-600' />
            ) : (
              <TrendingDown className='h-4 w-4 text-green-600' />
            )}
            <span className='text-sm text-muted-foreground'>
              {aiProb > humanProb
                ? "Xu hướng nghiêng về AI"
                : "Xu hướng nghiêng về Human"}
            </span>
          </div>
        </CardContent>
      </Card>

      <Alert className='border-amber-200 bg-amber-50 dark:border-amber-800 dark:bg-amber-900/10'>
        <AlertCircle className='h-4 w-4 text-amber-600' />
        <AlertDescription className='text-amber-800 dark:text-amber-200'>
          <strong>Lưu ý quan trọng:</strong> Kết quả dự đoán này chỉ mang tính
          chất tham khảo và không nên được sử dụng làm cơ sở để đánh giá tuyệt
          đối. AI có thể đưa ra kết quả không chính xác. Hãy luôn kết hợp với
          đánh giá chủ quan và kinh nghiệm của bạn để có kết luận chính xác
          nhất.
        </AlertDescription>
      </Alert>

      <Separator />

      <div className='text-center text-sm text-muted-foreground bg-muted/30 p-4 rounded-lg'>
        <p>
          Phân tích được thực hiện bởi AI Code Detector với focus vào patterns
          đặc trưng của AI vs Human code. Kết quả có thể thay đổi tùy thuộc vào
          chất lượng và đặc điểm của mã nguồn được phân tích.
        </p>
      </div>
    </div>
  );
}

export default PredictionResultsCard;
