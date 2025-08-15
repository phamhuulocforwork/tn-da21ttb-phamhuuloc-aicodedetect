"use client";

import { useState } from "react";

import {
  AlertCircle,
  BarChart3,
  Brain,
  Code,
  Download,
  FileText,
  Info,
  Loader2,
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

import { isAnalysisResponse } from "@/lib/api-client";
import { AnalysisResponse, IndividualAnalysisResponse } from "@/lib/api-types";
import FeatureCharts from "./feature-charts";

interface ResultsDashboardProps {
  result: AnalysisResponse | IndividualAnalysisResponse | null;
  loading?: boolean;
  error?: string | null;
  onRetry?: () => void;
  onExportReport?: () => void;
}

// Helper function to get score color
const getScoreColor = (score: number): string => {
  if (score <= 0.3) return "text-green-600 dark:text-green-400";
  if (score <= 0.6) return "text-yellow-600 dark:text-yellow-400";
  return "text-red-600 dark:text-red-400";
};

// Helper function to get score label
const getScoreLabel = (score: number): string => {
  if (score <= 0.3) return "Human-like";
  if (score <= 0.6) return "Mixed";
  return "AI-like";
};

export function ResultsDashboard({
  result,
  loading = false,
  error = null,
  onRetry,
  onExportReport,
}: ResultsDashboardProps) {
  const [activeTab, setActiveTab] = useState("overview");

  // Loading state
  if (loading) {
    return (
      <Card>
        <CardHeader>
          <div className='flex items-center gap-2'>
            <Loader2 className='h-5 w-5 animate-spin' />
            <CardTitle>Analyzing Code...</CardTitle>
          </div>
          <CardDescription>
            Please wait while we analyze your code for AI-generated patterns.
          </CardDescription>
        </CardHeader>
        <CardContent className='space-y-4'>
          <div className='space-y-2'>
            <div className='flex justify-between text-sm'>
              <span>Processing...</span>
              <span>Please wait</span>
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

  // Error state
  if (error) {
    return (
      <Alert variant='destructive'>
        <AlertCircle className='h-4 w-4' />
        <AlertTitle>Analysis Failed</AlertTitle>
        <AlertDescription className='mt-2'>
          {error}
          {onRetry && (
            <Button
              variant='outline'
              size='sm'
              onClick={onRetry}
              className='ml-4'
            >
              Try Again
            </Button>
          )}
        </AlertDescription>
      </Alert>
    );
  }

  // No result state
  if (!result) {
    return (
      <Card className='border-dashed'>
        <CardContent className='flex flex-col items-center justify-center py-12 text-center'>
          <BarChart3 className='h-12 w-12 text-muted-foreground mb-4' />
          <h3 className='text-lg font-semibold mb-2'>No Analysis Yet</h3>
          <p className='text-muted-foreground max-w-md'>
            Choose an analysis method and submit your code to see detailed
            results and insights.
          </p>
        </CardContent>
      </Card>
    );
  }

  // Check if it's a comprehensive analysis or individual analysis
  const isComprehensive = isAnalysisResponse(result);

  return (
    <div className='space-y-6'>
      {/* Header with overall assessment */}
      <Card>
        <CardHeader>
          <div className='flex items-start justify-between'>
            <div>
              <CardTitle className='flex items-center gap-2'>
                <FileText className='h-5 w-5' />
                Analysis Results
              </CardTitle>
              <CardDescription>
                {result.code_info.filename} •{" "}
                {result.code_info.language.toUpperCase()} •{" "}
                {result.code_info.loc} lines
              </CardDescription>
            </div>

            {onExportReport && (
              <Button variant='outline' size='sm' onClick={onExportReport}>
                <Download className='h-4 w-4 mr-2' />
                Export Report
              </Button>
            )}
          </div>

          {isComprehensive && (
            <div className='mt-4 p-4 bg-muted/50 rounded-lg'>
              <div className='flex items-center justify-between mb-3'>
                <h4 className='font-semibold'>Overall Assessment</h4>
                <Badge variant='outline'>
                  Confidence: {Math.round(result.assessment.confidence * 100)}%
                </Badge>
              </div>

              <div className='space-y-3'>
                <div>
                  <div className='flex items-center justify-between mb-2'>
                    <span className='text-sm font-medium'>
                      AI Likelihood Score
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

      {/* Tabs for different views */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className='grid w-full grid-cols-5'>
          <TabsTrigger value='overview'>Overview</TabsTrigger>
          <TabsTrigger value='features'>Features</TabsTrigger>
          <TabsTrigger value='charts'>Charts</TabsTrigger>
          <TabsTrigger value='details'>Details</TabsTrigger>
          <TabsTrigger value='raw'>Raw Data</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value='overview' className='space-y-6'>
          {isComprehensive ? (
            // Comprehensive analysis overview
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
                              {group.features.length} features
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
            // Individual analysis overview
            <Card>
              <CardHeader>
                <CardTitle>
                  {result.analysis_type
                    .replace("_", " ")
                    .replace(/\b\w/g, (l) => l.toUpperCase())}{" "}
                  Analysis
                </CardTitle>
                <CardDescription>{result.summary}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className='grid gap-4 md:grid-cols-3'>
                  <div className='text-center p-4 bg-muted/50 rounded-lg'>
                    <div className='text-2xl font-bold text-primary'>
                      {Object.keys(result.features).length}
                    </div>
                    <div className='text-sm text-muted-foreground'>
                      Features Extracted
                    </div>
                  </div>

                  <div className='text-center p-4 bg-muted/50 rounded-lg'>
                    <div className='text-2xl font-bold text-primary'>
                      {result.code_info.loc}
                    </div>
                    <div className='text-sm text-muted-foreground'>
                      Lines of Code
                    </div>
                  </div>

                  <div className='text-center p-4 bg-muted/50 rounded-lg'>
                    <div className='text-2xl font-bold text-primary'>
                      {Math.round((result.code_info.file_size / 1024) * 10) /
                        10}
                      KB
                    </div>
                    <div className='text-sm text-muted-foreground'>
                      File Size
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Features Tab */}
        <TabsContent value='features' className='space-y-6'>
          {isComprehensive ? (
            // Feature groups for comprehensive analysis
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
                            className='flex items-center justify-between p-3 bg-muted/50 rounded-lg'
                          >
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
                              {feature.normalized && (
                                <Badge variant='secondary' className='text-xs'>
                                  Normalized
                                </Badge>
                              )}
                            </div>
                          </div>
                        ))}

                        {group.features.length > 5 && (
                          <div className='text-center'>
                            <Badge variant='outline'>
                              +{group.features.length - 5} more features
                            </Badge>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ),
              )}
            </div>
          ) : (
            // Individual features
            <Card>
              <CardHeader>
                <CardTitle>Extracted Features</CardTitle>
                <CardDescription>
                  All {Object.keys(result.features).length} features from{" "}
                  {result.analysis_type} analysis
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className='grid gap-3 md:grid-cols-2'>
                  {Object.entries(result.features).map(([name, value]) => (
                    <div
                      key={name}
                      className='flex items-center justify-between p-3 bg-muted/50 rounded-lg'
                    >
                      <span className='font-medium text-sm'>{name}</span>
                      <span className='font-mono text-sm'>
                        {typeof value === "number" ? value.toFixed(3) : value}
                      </span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Charts Tab */}
        <TabsContent value='charts' className='space-y-6'>
          {isComprehensive ? (
            <FeatureCharts featureGroups={result.feature_groups} />
          ) : (
            <Card>
              <CardHeader>
                <CardTitle>Visualization Not Available</CardTitle>
                <CardDescription>
                  Charts are only available for comprehensive analysis. Use
                  Combined Analysis to see feature visualizations.
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

        {/* Details Tab */}
        <TabsContent value='details' className='space-y-6'>
          <div className='grid gap-6 md:grid-cols-2'>
            {/* Analysis Info */}
            <Card>
              <CardHeader>
                <CardTitle className='flex items-center gap-2'>
                  <Info className='h-4 w-4' />
                  Analysis Information
                </CardTitle>
              </CardHeader>
              <CardContent className='space-y-3'>
                <div className='flex justify-between'>
                  <span className='text-sm text-muted-foreground'>
                    Analysis ID:
                  </span>
                  <span className='font-mono text-sm'>
                    {result.analysis_id}
                  </span>
                </div>
                <Separator />
                <div className='flex justify-between'>
                  <span className='text-sm text-muted-foreground'>
                    Timestamp:
                  </span>
                  <span className='text-sm'>
                    {new Date(result.timestamp).toLocaleString()}
                  </span>
                </div>
                <Separator />
                <div className='flex justify-between'>
                  <span className='text-sm text-muted-foreground'>
                    Analysis Type:
                  </span>
                  <Badge variant='outline'>
                    {isComprehensive ? "Combined" : result.analysis_type}
                  </Badge>
                </div>
                <Separator />
                <div className='flex justify-between'>
                  <span className='text-sm text-muted-foreground'>
                    Success:
                  </span>
                  <Badge variant={result.success ? "default" : "destructive"}>
                    {result.success ? "Yes" : "No"}
                  </Badge>
                </div>
              </CardContent>
            </Card>

            {/* Code Info */}
            <Card>
              <CardHeader>
                <CardTitle className='flex items-center gap-2'>
                  <FileText className='h-4 w-4' />
                  Code Information
                </CardTitle>
              </CardHeader>
              <CardContent className='space-y-3'>
                <div className='flex justify-between'>
                  <span className='text-sm text-muted-foreground'>
                    Filename:
                  </span>
                  <span className='font-mono text-sm'>
                    {result.code_info.filename}
                  </span>
                </div>
                <Separator />
                <div className='flex justify-between'>
                  <span className='text-sm text-muted-foreground'>
                    Language:
                  </span>
                  <Badge variant='secondary'>
                    {result.code_info.language.toUpperCase()}
                  </Badge>
                </div>
                <Separator />
                <div className='flex justify-between'>
                  <span className='text-sm text-muted-foreground'>
                    Lines of Code:
                  </span>
                  <span className='font-bold'>{result.code_info.loc}</span>
                </div>
                <Separator />
                <div className='flex justify-between'>
                  <span className='text-sm text-muted-foreground'>
                    File Size:
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

        {/* Raw Data Tab */}
        <TabsContent value='raw' className='space-y-6'>
          <Card>
            <CardHeader>
              <CardTitle>Raw Analysis Data</CardTitle>
              <CardDescription>
                Complete JSON response from the analysis API
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

export default ResultsDashboard;
