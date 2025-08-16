"use client";

import { useState, useEffect } from "react";

import {
  AlertCircle,
  BarChart3,
  Brain,
  Code,
  Download,
  FileText,
  Info,
  Loader2,
  Sparkles,
  TrendingUp,
  Zap,
} from "lucide-react";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
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

import { isAIMDXResponse, isAnalysisResponse } from "@/lib/api-client";
import {
  AIMDXResponse,
  AnalysisResponse,
  IndividualAnalysisResponse,
} from "@/lib/api-types";

import BaselineComparisonView from "./baseline-comparison";
import FeatureCharts from "./feature-charts";
import { MDXRenderer } from "@/lib/mdx-utils";
interface ResultsDashboardProps {
  result: AnalysisResponse | IndividualAnalysisResponse | AIMDXResponse | null;
  loading?: boolean;
  error?: string | null;
  onRetry?: () => void;
  onExportReport?: () => void;
}

const getScoreColor = (score: number): string => {
  if (score <= 0.3) return "text-green-600 dark:text-green-400";
  if (score <= 0.6) return "text-yellow-600 dark:text-yellow-400";
  return "text-red-600 dark:text-red-400";
};

const getScoreLabel = (score: number): string => {
  if (score <= 0.3) return "Giống human";
  if (score <= 0.6) return "Hỗn hợp";
  return "Giống AI";
};

export default function ResultsDashboard({
  result,
  loading = false,
  error = null,
  onRetry,
  onExportReport,
}: ResultsDashboardProps) {
  const [activeTab, setActiveTab] = useState("overview");

  // Handle MDX content for AI analysis
  const aiMdxContent = result && isAIMDXResponse(result) ? result.mdx_content : "";

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <div className='flex items-center gap-2'>
            <Loader2 className='h-5 w-5 animate-spin' />
            <CardTitle>Đang phân tích...</CardTitle>
          </div>
          <CardDescription>
            Vui lòng chờ trong khi hệ thống phân tích
          </CardDescription>
        </CardHeader>
        <CardContent className='space-y-4'>
          <div className='space-y-2'>
            <div className='flex justify-between text-sm'>
              <span>Đang xử lý...</span>
              <span>Vui lòng chờ</span>
            </div>
            <Progress value={65} className='h-2' />
          </div>

          <div className='grid gap-4 md:grid-cols-3'>
            {Array.from({ length: 3 }).map((_, i) => (
              <Card key={i} className='p-4'>
                <div className='flex items-center gap-2'>
                  <div className='w-4 h-4 bg-muted rounded animate-pulse' />
                  <div className='h-4 bg-muted rounded flex-1 animate-pulse' />
                </div>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Alert variant='destructive'>
        <AlertCircle className='h-4 w-4' />
        <AlertTitle>Phân tích thất bại</AlertTitle>
        <AlertDescription className='mt-2'>
          {error}
          {onRetry && (
            <Button
              variant='outline'
              size='sm'
              onClick={onRetry}
              className='ml-4'
            >
              Thử lại
            </Button>
          )}
        </AlertDescription>
      </Alert>
    );
  }

  if (!result) {
    return (
      <Card className='border-dashed'>
        <CardContent className='flex flex-col items-center justify-center py-12 text-center'>
          <BarChart3 className='h-12 w-12 text-muted-foreground mb-4' />
          <h3 className='text-lg font-semibold mb-2'>Chưa có phân tích</h3>
          <p className='text-muted-foreground max-w-md'>
            Chọn phương thức phân tích và gửi mã để xem kết quả chi tiết.
          </p>
        </CardContent>
      </Card>
    );
  }

  const isComprehensive = isAnalysisResponse(result);
  const isAIAnalysis = isAIMDXResponse(result);

  return (
    <div className='space-y-6'>
      <Card>
        <CardHeader>
          <div className='flex items-start justify-between'>
            <div>
              <CardTitle className='flex items-center gap-2'>
                <FileText className='h-5 w-5' />
                Kết quả phân tích
              </CardTitle>
              <CardDescription>
                {result.code_info.filename} •{" "}
                {result.code_info.language.toUpperCase()} •{" "}
                {result.code_info.loc} dòng
              </CardDescription>
            </div>

            {onExportReport && (
              <Button variant='outline' size='sm' onClick={onExportReport}>
                <Download className='h-4 w-4 mr-2' />
                Xuất báo cáo
              </Button>
            )}
          </div>

          {isComprehensive && (
            <div className='mt-4 p-4 bg-muted/50 rounded-lg'>
              <div className='flex items-center justify-between mb-3'>
                <div>
                  <h4 className='font-semibold'>Đánh giá Feature Analysis</h4>
                  <p className='text-xs text-muted-foreground'>
                    Kết quả từ phân tích đặc trưng và so sánh baseline dataset
                  </p>
                </div>
                <Badge variant='outline'>
                  Độ tin cậy: {Math.round(result.assessment.confidence * 100)}%
                </Badge>
              </div>

              <div className='space-y-3'>
                <div>
                  <div className='flex items-center justify-between mb-2'>
                    <span className='text-sm font-medium'>
                      Điểm khả năng giống AI
                    </span>
                    <span
                      className={`text-lg font-bold ${getScoreColor(result.assessment.overall_score)}`}
                    >
                      {getScoreLabel(result.assessment.overall_score)} (
                      {Math.round(result.assessment.overall_score * 100)}%)
                    </span>
                  </div>
                  <Progress
                    value={result.assessment.overall_score * 100}
                    className='h-2'
                  />
                </div>

                {result.assessment.baseline_summary && (
                  <div className='p-3 bg-background/50 rounded-lg border'>
                    <div className='flex items-center justify-between mb-2'>
                      <h5 className='text-xs font-medium text-muted-foreground'>
                        So sánh với Dataset Baseline:
                      </h5>
                      <Badge variant='secondary' className='text-xs'>
                        {
                          result.assessment.baseline_summary
                            .total_features_compared
                        }{" "}
                        features
                      </Badge>
                    </div>
                    <div className='grid gap-3 md:grid-cols-2'>
                      <div className='text-center'>
                        <div className='text-sm font-medium text-red-600 dark:text-red-400'>
                          {Math.round(
                            result.assessment.baseline_summary
                              .overall_ai_similarity * 100,
                          )}
                          %
                        </div>
                        <div className='text-xs text-muted-foreground'>
                          Tương đồng với AI samples
                        </div>
                      </div>
                      <div className='text-center'>
                        <div className='text-sm font-medium text-green-600 dark:text-green-400'>
                          {Math.round(
                            result.assessment.baseline_summary
                              .overall_human_similarity * 100,
                          )}
                          %
                        </div>
                        <div className='text-xs text-muted-foreground'>
                          Tương đồng với Human samples
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                <p className='text-sm text-muted-foreground'>
                  {result.assessment.summary}
                </p>

                {result.assessment.key_indicators.length > 0 && (
                  <div className='flex flex-wrap gap-2'>
                    {result.assessment.key_indicators.map(
                      (indicator, index) => (
                        <Badge
                          key={index}
                          variant='secondary'
                          className='text-xs'
                        >
                          {indicator}
                        </Badge>
                      ),
                    )}
                  </div>
                )}
              </div>
            </div>
          )}
        </CardHeader>
      </Card>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList
          className={`grid w-full ${isAIAnalysis ? "grid-cols-4" : "grid-cols-6"}`}
        >
          <TabsTrigger value='overview'>Tổng quan</TabsTrigger>
          {isAIAnalysis ? (
            <>
              <TabsTrigger value='ai'>AI Analysis</TabsTrigger>
              <TabsTrigger value='details'>Chi tiết</TabsTrigger>
              <TabsTrigger value='raw'>Dữ liệu thô</TabsTrigger>
            </>
          ) : (
            <>
              <TabsTrigger value='features'>Đặc trưng</TabsTrigger>
              <TabsTrigger value='baseline'>So sánh baseline</TabsTrigger>
              <TabsTrigger value='charts'>Biểu đồ</TabsTrigger>
              <TabsTrigger value='details'>Chi tiết</TabsTrigger>
              <TabsTrigger value='raw'>Dữ liệu thô</TabsTrigger>
            </>
          )}
        </TabsList>

        <TabsContent value='overview' className='space-y-6'>
          {isComprehensive ? (
            <div className='grid gap-6 md:grid-cols-2 lg:grid-cols-4'>
              {Object.entries(result.feature_groups).map(
                ([groupName, group]) => {
                  const icons: Record<
                    string,
                    React.ComponentType<{ className?: string }>
                  > = {
                    structure_metrics: Code,
                    style_metrics: Brain,
                    complexity_metrics: TrendingUp,
                    ai_detection_metrics: Zap,
                  };

                  const Icon = icons[groupName] || BarChart3;

                  return (
                    <Card key={groupName}>
                      <CardContent className='p-6'>
                        <div className='flex items-center gap-3 mb-3'>
                          <div className='p-2 bg-primary/10 rounded-md'>
                            <Icon className='h-4 w-4 text-primary' />
                          </div>
                          <h3 className='font-semibold text-sm'>
                            {group.group_name}
                          </h3>
                        </div>

                        <div className='space-y-2'>
                          <div className='flex items-center justify-between'>
                            <span className='text-2xl font-bold'>
                              {Math.round(group.group_score * 100)}%
                            </span>
                            <Badge variant='outline' className='text-xs'>
                              {group.features.length} đặc trưng
                            </Badge>
                          </div>

                          <Progress
                            value={group.group_score * 100}
                            className='h-1'
                          />

                          <p className='text-xs text-muted-foreground'>
                            {group.description}
                          </p>
                        </div>
                      </CardContent>
                    </Card>
                  );
                },
              )}
            </div>
          ) : (
            <Card>
              <CardHeader>
                <CardTitle>
                  {result.analysis_type
                    .replace("_", " ")
                    .replace(/\b\w/g, (l) => l.toUpperCase())}{" "}
                  Phân tích
                </CardTitle>
                <CardDescription>{result.summary}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className='grid gap-4 md:grid-cols-3'>
                  <div className='text-center p-4 bg-muted/50 rounded-lg'>
                    <div className='text-2xl font-bold text-primary'>
                      {isAIAnalysis
                        ? "AI"
                        : Object.keys(
                            (result as IndividualAnalysisResponse).features,
                          ).length}
                    </div>
                    <div className='text-sm text-muted-foreground'>
                      {isAIAnalysis ? "AI Analysis" : "Đặc trưng đã trích xuất"}
                    </div>
                  </div>

                  <div className='text-center p-4 bg-muted/50 rounded-lg'>
                    <div className='text-2xl font-bold text-primary'>
                      {result.code_info.loc}
                    </div>
                    <div className='text-sm text-muted-foreground'>Số dòng</div>
                  </div>

                  <div className='text-center p-4 bg-muted/50 rounded-lg'>
                    <div className='text-2xl font-bold text-primary'>
                      {Math.round((result.code_info.file_size / 1024) * 10) /
                        10}
                      KB
                    </div>
                    <div className='text-sm text-muted-foreground'>
                      Kích thước
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value='baseline' className='space-y-6'>
          {isComprehensive ? (
            <BaselineComparisonView
              baselineSummary={result.assessment.baseline_summary}
              featuresWithComparison={Object.values(result.feature_groups)
                .flatMap((group) => group.features)
                .filter((feature) => feature.baseline_comparison)}
            />
          ) : (
            <Card>
              <CardHeader>
                <CardTitle>Không có so sánh Baseline</CardTitle>
                <CardDescription>
                  So sánh baseline không có sẵn cho phức phân tích đang được
                  chọn
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className='flex items-center justify-center py-8 text-muted-foreground'>
                  <TrendingUp className='h-12 w-12 mb-4' />
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value='features' className='space-y-6'>
          {isComprehensive && (
            <div className='space-y-6'>
              {Object.entries(result.feature_groups).map(
                ([groupName, group]) => (
                  <Card key={groupName}>
                    <CardHeader>
                      <CardTitle className='flex items-center justify-between'>
                        {group.group_name}
                        <Badge variant='outline'>
                          {group.visualization_type}
                        </Badge>
                      </CardTitle>
                      <CardDescription>{group.description}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className='space-y-3'>
                        {group.features.slice(0, 5).map((feature, index) => (
                          <div
                            key={index}
                            className='p-3 bg-muted/50 rounded-lg space-y-2'
                          >
                            <div className='flex items-center justify-between'>
                              <div>
                                <div className='font-medium text-sm'>
                                  {feature.name}
                                </div>
                                <div className='text-xs text-muted-foreground'>
                                  {feature.interpretation}
                                </div>
                              </div>
                              <div className='text-right'>
                                <div className='font-bold'>
                                  {feature.value.toFixed(3)}
                                </div>
                              </div>
                            </div>

                            {feature.baseline_comparison && (
                              <div className='pt-2 border-t space-y-1'>
                                <div className='flex items-center justify-between text-xs'>
                                  <span className='text-muted-foreground'>
                                    So sánh với baseline:
                                  </span>
                                  <Badge
                                    variant='outline'
                                    className={`text-xs ${
                                      feature.baseline_comparison.verdict ===
                                      "ai-like"
                                        ? "text-red-600 dark:text-red-400"
                                        : feature.baseline_comparison
                                              .verdict === "human-like"
                                          ? "text-green-600 dark:text-green-400"
                                          : "text-yellow-600 dark:text-yellow-400"
                                    }`}
                                  >
                                    {feature.baseline_comparison.verdict}
                                  </Badge>
                                </div>
                                <div className='text-xs text-muted-foreground'>
                                  AI:{" "}
                                  {feature.baseline_comparison.ai_baseline.toFixed(
                                    3,
                                  )}{" "}
                                  | Human:{" "}
                                  {feature.baseline_comparison.human_baseline.toFixed(
                                    3,
                                  )}
                                </div>
                              </div>
                            )}
                          </div>
                        ))}

                        {group.features.length > 5 && (
                          <div className='text-center'>
                            <Badge variant='outline'>
                              +{group.features.length - 5} đặc trưng khác
                            </Badge>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ),
              )}
            </div>
          )}
        </TabsContent>

        <TabsContent value='ai' className='space-y-6'>
          {isAIAnalysis ? (
            <Card>
              <CardHeader>
                <CardTitle className='flex items-center gap-2'>
                  <Sparkles className='h-5 w-5' />
                  AI Analysis
                </CardTitle>
                <CardDescription>
                  Kết quả phân tích từ AI với đánh giá chi tiết về patterns và
                  reasoning
                </CardDescription>
              </CardHeader>
              <CardContent>
                <MDXRenderer 
                  content={aiMdxContent}
                  loadingText="Đang xử lý nội dung phân tích AI..."
                  errorTitle="Lỗi xử lý nội dung phân tích"
                  errorDescription="Không thể hiển thị kết quả phân tích AI. Vui lòng thử lại."
                />
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardHeader>
                <CardTitle>AI Analysis</CardTitle>
                <CardDescription>
                  Phân tích AI chỉ có sẵn cho loại phân tích AI
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className='flex items-center justify-center py-8 text-muted-foreground'>
                  <Sparkles className='h-12 w-12 mb-4' />
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value='charts' className='space-y-6'>
          {isComprehensive ? (
            <FeatureCharts featureGroups={result.feature_groups} />
          ) : (
            <Card>
              <CardHeader>
                <CardTitle>Không có trực quan hóa</CardTitle>
                <CardDescription>
                  Biểu đồ chỉ không có sẵn cho phân tích đang được chọn
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className='flex items-center justify-center py-8 text-muted-foreground'>
                  <BarChart3 className='h-12 w-12 mb-4' />
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value='details' className='space-y-6'>
          <div className='grid gap-6 md:grid-cols-2'>
            <Card>
              <CardHeader>
                <CardTitle className='flex items-center gap-2'>
                  <Info className='h-4 w-4' />
                  Thông tin phân tích
                </CardTitle>
              </CardHeader>
              <CardContent className='space-y-3'>
                <div className='flex justify-between'>
                  <span className='text-sm text-muted-foreground'>
                    ID phân tích:
                  </span>
                  <span className='font-mono text-sm'>
                    {result.analysis_id}
                  </span>
                </div>
                <Separator />
                <div className='flex justify-between'>
                  <span className='text-sm text-muted-foreground'>
                    Thời gian:
                  </span>
                  <span className='text-sm'>
                    {new Date(result.timestamp).toLocaleString()}
                  </span>
                </div>
                <Separator />
                <div className='flex justify-between'>
                  <span className='text-sm text-muted-foreground'>
                    Loại phân tích:
                  </span>
                  <Badge variant='outline'>
                    {isComprehensive ? "Combined" : result.analysis_type}
                  </Badge>
                </div>
                <Separator />
                <div className='flex justify-between'>
                  <span className='text-sm text-muted-foreground'>
                    Thành công:
                  </span>
                  <Badge variant={result.success ? "default" : "destructive"}>
                    {result.success ? "Yes" : "No"}
                  </Badge>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className='flex items-center gap-2'>
                  <FileText className='h-4 w-4' />
                  Thông tin code
                </CardTitle>
              </CardHeader>
              <CardContent className='space-y-3'>
                <div className='flex justify-between'>
                  <span className='text-sm text-muted-foreground'>
                    Tên file:
                  </span>
                  <span className='font-mono text-sm'>
                    {result.code_info.filename}
                  </span>
                </div>
                <Separator />
                <div className='flex justify-between'>
                  <span className='text-sm text-muted-foreground'>
                    Ngôn ngữ:
                  </span>
                  <Badge variant='secondary'>
                    {result.code_info.language.toUpperCase()}
                  </Badge>
                </div>
                <Separator />
                <div className='flex justify-between'>
                  <span className='text-sm text-muted-foreground'>
                    Số dòng:
                  </span>
                  <span className='font-bold'>{result.code_info.loc}</span>
                </div>
                <Separator />
                <div className='flex justify-between'>
                  <span className='text-sm text-muted-foreground'>
                    Kích thước:
                  </span>
                  <span className='text-sm'>
                    {Math.round((result.code_info.file_size / 1024) * 10) / 10}{" "}
                    KB
                  </span>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value='raw' className='space-y-6'>
          <Card>
            <CardHeader>
              <CardTitle>Dữ liệu phân tích</CardTitle>
              <CardDescription>
                JSON đầy đủ trả về từ API phân tích
              </CardDescription>
            </CardHeader>
            <CardContent>
              <pre className='text-xs bg-muted p-4 rounded-lg overflow-auto max-h-96'>
                {JSON.stringify(result, null, 2)}
              </pre>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
