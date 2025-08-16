"use client";

import { useState } from "react";

import {
  AlertCircle,
  BarChart3,
  Brain,
  CheckCircle,
  Info,
  Sparkles,
  Target,
  TrendingDown,
  TrendingUp,
  XCircle,
} from "lucide-react";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

import { GeminiAnalysisResult, GeminiCombinedResponse } from "@/lib/api-types";

interface GeminiAnalysisProps {
  result: GeminiCombinedResponse;
  className?: string;
}

const getPredictionColor = (prediction: string): string => {
  return prediction === "AI-generated"
    ? "text-red-600 dark:text-red-400"
    : "text-green-600 dark:text-green-400";
};

const getPredictionIcon = (prediction: string) => {
  return prediction === "AI-generated" ? (
    <XCircle className='h-4 w-4' />
  ) : (
    <CheckCircle className='h-4 w-4' />
  );
};

const getConfidenceLevel = (confidence: number): string => {
  if (confidence >= 0.8) return "Cao";
  if (confidence >= 0.6) return "Trung bình";
  return "Thấp";
};

const getConfidenceColor = (confidence: number): string => {
  if (confidence >= 0.8) return "text-green-600 dark:text-green-400";
  if (confidence >= 0.6) return "text-yellow-600 dark:text-yellow-400";
  return "text-red-600 dark:text-red-400";
};

function GeminiResultCard({ analysis }: { analysis: GeminiAnalysisResult }) {
  return (
    <Card className='border-primary/20'>
      <CardHeader>
        <div className='flex items-start justify-between'>
          <div className='flex items-center gap-3'>
            <div className='p-2 bg-primary/10 rounded-md'>
              <Sparkles className='h-5 w-5 text-primary' />
            </div>
            <div>
              <CardTitle className='flex items-center gap-2'>
                Gemini AI Analysis
                <Badge variant='outline' className='text-xs'>
                  {analysis.prediction}
                </Badge>
              </CardTitle>
              <CardDescription>
                Phân tích bằng Google Gemini AI với mô hình ngôn ngữ lớn
              </CardDescription>
            </div>
          </div>
        </div>
      </CardHeader>

      <CardContent className='space-y-6'>
        <div className='p-4 bg-muted/50 rounded-lg'>
          <div className='flex items-center justify-between mb-3'>
            <h4 className='font-semibold flex items-center gap-2'>
              {getPredictionIcon(analysis.prediction)}
              Kết quả dự đoán
            </h4>
            <Badge
              variant='outline'
              className={`${getPredictionColor(analysis.prediction)} border-current`}
            >
              {analysis.prediction === "AI-generated"
                ? "AI Generated"
                : "Human Written"}
            </Badge>
          </div>

          <div className='space-y-3'>
            <div>
              <div className='flex justify-between text-sm mb-1'>
                <span>Độ tin cậy tổng thể</span>
                <span
                  className={`font-medium ${getConfidenceColor(analysis.confidence)}`}
                >
                  {Math.round(analysis.confidence * 100)}% (
                  {getConfidenceLevel(analysis.confidence)})
                </span>
              </div>
              <Progress value={analysis.confidence * 100} className='h-2' />
            </div>

            <div className='text-sm text-muted-foreground'>
              {analysis.confidence_explanation}
            </div>
          </div>
        </div>

        {analysis.probability_analysis && (
          <div className='space-y-4'>
            <h4 className='font-semibold flex items-center gap-2'>
              <Target className='h-4 w-4' />
              Phân tích xác suất
            </h4>

            <div className='grid gap-3 md:grid-cols-3'>
              <div className='text-center p-3 bg-red-50 dark:bg-red-950/20 rounded-lg'>
                <div className='text-2xl font-bold text-red-600 dark:text-red-400'>
                  {Math.round(
                    analysis.probability_analysis.ai_likelihood * 100,
                  )}
                  %
                </div>
                <div className='text-xs text-muted-foreground'>
                  AI Likelihood
                </div>
              </div>

              <div className='text-center p-3 bg-green-50 dark:bg-green-950/20 rounded-lg'>
                <div className='text-2xl font-bold text-green-600 dark:text-green-400'>
                  {Math.round(
                    analysis.probability_analysis.human_likelihood * 100,
                  )}
                  %
                </div>
                <div className='text-xs text-muted-foreground'>
                  Human Likelihood
                </div>
              </div>

              <div className='text-center p-3 bg-yellow-50 dark:bg-yellow-950/20 rounded-lg'>
                <div className='text-2xl font-bold text-yellow-600 dark:text-yellow-400'>
                  {Math.round(
                    analysis.probability_analysis.uncertainty_level * 100,
                  )}
                  %
                </div>
                <div className='text-xs text-muted-foreground'>Uncertainty</div>
              </div>
            </div>
          </div>
        )}

        <div className='space-y-4'>
          <h4 className='font-semibold flex items-center gap-2'>
            <Brain className='h-4 w-4' />
            Lý do phân tích
          </h4>
          <div className='space-y-2'>
            {analysis.reasoning.map((reason, index) => (
              <div
                key={index}
                className='flex items-start gap-2 p-2 bg-muted/30 rounded'
              >
                <div className='w-1.5 h-1.5 rounded-full bg-primary mt-2 flex-shrink-0' />
                <span className='text-sm'>{reason}</span>
              </div>
            ))}
          </div>
        </div>

        <div className='space-y-4'>
          <h4 className='font-semibold flex items-center gap-2'>
            <Info className='h-4 w-4' />
            Chỉ số quan trọng
          </h4>
          <div className='flex flex-wrap gap-2'>
            {analysis.key_indicators.map((indicator, index) => (
              <Badge key={index} variant='secondary' className='text-xs'>
                {indicator}
              </Badge>
            ))}
          </div>
        </div>

        <div className='grid gap-4 md:grid-cols-2'>
          <div className='space-y-3'>
            <h5 className='font-medium text-red-600 dark:text-red-400 flex items-center gap-2'>
              <TrendingUp className='h-4 w-4' />
              AI Patterns ({analysis.ai_patterns_detected.length})
            </h5>
            <div className='space-y-1'>
              {analysis.ai_patterns_detected.length > 0 ? (
                analysis.ai_patterns_detected.map((pattern, index) => (
                  <div
                    key={index}
                    className='text-xs p-2 bg-red-50 dark:bg-red-950/20 rounded'
                  >
                    {pattern}
                  </div>
                ))
              ) : (
                <div className='text-xs text-muted-foreground italic'>
                  Không phát hiện patterns AI rõ ràng
                </div>
              )}
            </div>
          </div>

          <div className='space-y-3'>
            <h5 className='font-medium text-green-600 dark:text-green-400 flex items-center gap-2'>
              <TrendingDown className='h-4 w-4' />
              Human Patterns ({analysis.human_patterns_detected.length})
            </h5>
            <div className='space-y-1'>
              {analysis.human_patterns_detected.length > 0 ? (
                analysis.human_patterns_detected.map((pattern, index) => (
                  <div
                    key={index}
                    className='text-xs p-2 bg-green-50 dark:bg-green-950/20 rounded'
                  >
                    {pattern}
                  </div>
                ))
              ) : (
                <div className='text-xs text-muted-foreground italic'>
                  Không phát hiện patterns human rõ ràng
                </div>
              )}
            </div>
          </div>
        </div>

        {analysis.additional_notes && (
          <Alert>
            <Info className='h-4 w-4' />
            <AlertTitle>Ghi chú bổ sung</AlertTitle>
            <AlertDescription>{analysis.additional_notes}</AlertDescription>
          </Alert>
        )}
      </CardContent>
    </Card>
  );
}

function DetailedAnalysisCard({
  analysis,
}: {
  analysis: GeminiAnalysisResult;
}) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className='flex items-center gap-2'>
          <BarChart3 className='h-5 w-5' />
          Phân tích chi tiết
        </CardTitle>
        <CardDescription>
          Đánh giá chi tiết về các khía cạnh khác nhau của code
        </CardDescription>
      </CardHeader>

      <CardContent className='space-y-4'>
        <div className='space-y-4'>
          <div className='p-3 border rounded-lg'>
            <h5 className='font-medium text-sm mb-2'>Đánh giá phong cách</h5>
            <p className='text-sm text-muted-foreground'>
              {analysis.detailed_analysis.style_assessment}
            </p>
          </div>

          <div className='p-3 border rounded-lg'>
            <h5 className='font-medium text-sm mb-2'>Đánh giá cấu trúc</h5>
            <p className='text-sm text-muted-foreground'>
              {analysis.detailed_analysis.structure_assessment}
            </p>
          </div>

          <div className='p-3 border rounded-lg'>
            <h5 className='font-medium text-sm mb-2'>Đánh giá cú pháp</h5>
            <p className='text-sm text-muted-foreground'>
              {analysis.detailed_analysis.syntax_assessment}
            </p>
          </div>

          <div className='p-3 border rounded-lg bg-muted/30'>
            <h5 className='font-medium text-sm mb-2'>Đánh giá tổng quan</h5>
            <p className='text-sm text-muted-foreground'>
              {analysis.detailed_analysis.overall_assessment}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export function GeminiAnalysis({ result, className }: GeminiAnalysisProps) {
  const [activeTab, setActiveTab] = useState("overview");

  if (!result.gemini_analysis.success) {
    return (
      <div className={className}>
        <Alert variant='destructive'>
          <AlertCircle className='h-4 w-4' />
          <AlertTitle>Gemini Analysis Failed</AlertTitle>
          <AlertDescription>
            {result.gemini_analysis.error ||
              "Không thể thực hiện phân tích Gemini AI."}
            {result.gemini_analysis.fallback_analysis && (
              <div className='mt-2'>
                <p>Fallback analysis available with limited accuracy.</p>
              </div>
            )}
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  const analysis =
    result.gemini_analysis.ai_analysis ||
    result.gemini_analysis.fallback_analysis;

  if (!analysis) {
    return (
      <div className={className}>
        <Alert>
          <Info className='h-4 w-4' />
          <AlertTitle>No Analysis Data</AlertTitle>
          <AlertDescription>
            Gemini analysis completed but no structured data was returned.
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <div className={`space-y-6 ${className}`}>
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className='grid w-full grid-cols-3'>
          <TabsTrigger value='overview'>Tổng quan</TabsTrigger>
          <TabsTrigger value='detailed'>Chi tiết</TabsTrigger>
          <TabsTrigger value='combined'>So sánh Features</TabsTrigger>
        </TabsList>

        <TabsContent value='overview' className='space-y-6'>
          <GeminiResultCard analysis={analysis} />
        </TabsContent>

        <TabsContent value='detailed' className='space-y-6'>
          <DetailedAnalysisCard analysis={analysis} />
        </TabsContent>

        <TabsContent value='combined' className='space-y-6'>
          {result.feature_analysis && result.combined_assessment ? (
            <div className='space-y-4'>
              <Card>
                <CardHeader>
                  <CardTitle>Kết quả kết hợp Features + AI</CardTitle>
                  <CardDescription>
                    So sánh giữa Feature Analysis và Gemini AI analysis
                  </CardDescription>
                </CardHeader>
                <CardContent className='space-y-4'>
                  <div className='grid gap-4 md:grid-cols-2'>
                    <div className='p-4 bg-blue-50 dark:bg-blue-950/20 rounded-lg'>
                      <h5 className='font-medium text-blue-600 dark:text-blue-400 mb-2'>
                        Feature Analysis
                      </h5>
                      <div className='text-2xl font-bold'>
                        {Math.round(
                          result.feature_analysis.assessment.overall_score *
                            100,
                        )}
                        %
                      </div>
                      <div className='text-xs text-muted-foreground'>
                        Confidence:{" "}
                        {Math.round(
                          result.feature_analysis.assessment.confidence * 100,
                        )}
                        %
                      </div>
                    </div>

                    <div className='p-4 bg-purple-50 dark:bg-purple-950/20 rounded-lg'>
                      <h5 className='font-medium text-purple-600 dark:text-purple-400 mb-2'>
                        Gemini AI
                      </h5>
                      <div className='text-2xl font-bold'>
                        {analysis.prediction === "AI-generated"
                          ? Math.round(analysis.confidence * 100)
                          : Math.round((1 - analysis.confidence) * 100)}
                        %
                      </div>
                      <div className='text-xs text-muted-foreground'>
                        Confidence: {Math.round(analysis.confidence * 100)}%
                      </div>
                    </div>
                  </div>

                  <Separator />

                  <div className='p-4 bg-muted/50 rounded-lg'>
                    <h5 className='font-medium mb-2'>Combined Assessment</h5>
                    <div className='flex items-center justify-between mb-2'>
                      <span>Final Score:</span>
                      <span className='text-lg font-bold'>
                        {Math.round(
                          result.combined_assessment.overall_score * 100,
                        )}
                        %
                      </span>
                    </div>
                    <Progress
                      value={result.combined_assessment.overall_score * 100}
                      className='mb-2'
                    />
                    <p className='text-sm text-muted-foreground'>
                      {result.combined_assessment.summary}
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
          ) : (
            <Alert>
              <Info className='h-4 w-4' />
              <AlertTitle>No Feature Comparison Available</AlertTitle>
              <AlertDescription>
                Combined analysis with feature analysis is not available for
                this request.
              </AlertDescription>
            </Alert>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}

export default GeminiAnalysis;
