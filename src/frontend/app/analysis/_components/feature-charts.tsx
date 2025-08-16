"use client";

import { useEffect, useMemo, useRef } from "react";

import { BoxAndWiskers, BoxPlotChart } from "@sgratzl/chartjs-chart-boxplot";
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Tooltip as ChartTooltip,
  Legend,
  LinearScale,
  Title,
} from "chart.js";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

import { FeatureGroup } from "@/lib/api-types";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  ChartTooltip,
  Legend,
  BoxAndWiskers,
);

interface FeatureChartsProps {
  featureGroups: Record<string, FeatureGroup>;
  className?: string;
}

const CHART_COLORS = {
  primary: "#3b82f6",
  secondary: "#ef4444",
  accent: "#10b981",
  warning: "#f59e0b",
  muted: "#6b7280",
};

const prepareDataForVisualization = (group: FeatureGroup) => {
  switch (group.visualization_type) {
    case "bar":
      return group.features.map((feature) => ({
        name: feature.name.replace(/_/g, " "),
        value: feature.value,
        interpretation: feature.interpretation,
        normalized: feature.normalized,
      }));

    case "radar":
      return group.features.map((feature) => ({
        subject: feature.name.replace(/_/g, " "),
        value: feature.normalized ? feature.value * 100 : feature.value,
        fullMark: 100,
      }));

    case "line":
      return group.features.map((feature, index) => ({
        index: index + 1,
        name: feature.name.replace(/_/g, " "),
        value: feature.value,
        interpretation: feature.interpretation,
      }));

    default:
      return group.features.map((feature) => ({
        name: feature.name.replace(/_/g, " "),
        value: feature.value,
        interpretation: feature.interpretation,
      }));
  }
};

const BarChartVisualization = ({ group }: { group: FeatureGroup }) => {
  const data = prepareDataForVisualization(group);

  return (
    <ResponsiveContainer width='100%' height={300}>
      <BarChart
        data={data}
        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray='3 3' className='stroke-muted' />
        <XAxis
          dataKey='name'
          angle={-45}
          textAnchor='end'
          height={80}
          className='text-xs fill-muted-foreground'
        />
        <YAxis className='text-xs fill-muted-foreground' />
        <Tooltip
          contentStyle={{
            backgroundColor: "hsl(var(--background))",
            border: "1px solid hsl(var(--border))",
            borderRadius: "6px",
          }}
          formatter={(value: number, name: string) => [
            `${value.toFixed(3)}`,
            name,
          ]}
        />
        <Bar
          dataKey='value'
          fill={CHART_COLORS.primary}
          radius={[2, 2, 0, 0]}
        />
      </BarChart>
    </ResponsiveContainer>
  );
};

const RadarChartVisualization = ({ group }: { group: FeatureGroup }) => {
  const { strongFeatures, summary } = useMemo(() => {
    const sortedFeatures = [...group.features].sort((a, b) => {
      const aScore = a.baseline_comparison
        ? Math.abs(
            a.baseline_comparison.ai_similarity -
              a.baseline_comparison.human_similarity,
          ) * a.baseline_comparison.confidence
        : Math.abs(a.value);
      const bScore = b.baseline_comparison
        ? Math.abs(
            b.baseline_comparison.ai_similarity -
              b.baseline_comparison.human_similarity,
          ) * b.baseline_comparison.confidence
        : Math.abs(b.value);
      return bScore - aScore;
    });

    const strongFeatures = sortedFeatures.slice(
      0,
      Math.min(8, sortedFeatures.length),
    );
    const weakFeatures = sortedFeatures.slice(8);

    let summary = null;
    if (weakFeatures.length > 0) {
      const avgWeakValue =
        weakFeatures.reduce((sum, f) => sum + f.value, 0) / weakFeatures.length;
      summary = {
        name: `Other Features (${weakFeatures.length})`,
        value: avgWeakValue,
        description: `Average of ${weakFeatures.length} additional features`,
      };
    }

    return { strongFeatures, summary };
  }, [group.features]);

  const radarData = useMemo(() => {
    const data = strongFeatures.map((feature) => {
      let subjectName = feature.name
        .replace(/_/g, " ")
        .replace(/\b\w/g, (l) => l.toUpperCase())
        .replace(/Ratio$/, "")
        .replace(/Score$/, "")
        .replace(/Consistency$/, "Cons.");

      if (
        feature.baseline_comparison &&
        Math.abs(
          feature.baseline_comparison.ai_similarity -
            feature.baseline_comparison.human_similarity,
        ) > 0.3
      ) {
        subjectName += " *";
      }

      return {
        subject: subjectName,
        current: feature.normalized
          ? feature.value * 100
          : Math.min(feature.value * 100, 100),
        aiBaseline: feature.baseline_comparison
          ? feature.baseline_comparison.ai_baseline * 100
          : null,
        humanBaseline: feature.baseline_comparison
          ? feature.baseline_comparison.human_baseline * 100
          : null,
        originalValue: feature.value,
        fullMark: 100,
        baseline: feature.baseline_comparison,
        interpretation: feature.interpretation,
      };
    });

    if (summary) {
      data.push({
        subject: summary.name,
        current: summary.value * 100,
        aiBaseline: null,
        humanBaseline: null,
        originalValue: summary.value,
        fullMark: 100,
        baseline: undefined,
        interpretation: summary.description,
      });
    }

    return data;
  }, [strongFeatures, summary]);

  return (
    <div className='space-y-4'>
      <div className='text-xs text-muted-foreground text-center'>
        Showing top {strongFeatures.length} features
        {summary && ` (${summary.name.match(/\d+/)?.[0]} others grouped)`}
        {strongFeatures.some((f) => f.baseline_comparison) && (
          <span className='block mt-1'>
            * = Strong baseline difference (AI vs Human)
          </span>
        )}
      </div>

      <ResponsiveContainer width='100%' height={320}>
        <RadarChart
          data={radarData}
          margin={{ top: 20, right: 40, bottom: 20, left: 40 }}
          style={{ backgroundColor: "transparent" }}
        >
          <PolarGrid className='stroke-muted' />
          <PolarAngleAxis
            dataKey='subject'
            className='text-xs fill-muted-foreground'
            tick={{ fontSize: 10 }}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            className='text-xs fill-muted-foreground'
            tick={{ fontSize: 9 }}
          />

          {/* Current Values */}
          <Radar
            name='Current'
            dataKey='current'
            stroke={CHART_COLORS.primary}
            fill={CHART_COLORS.primary}
            fillOpacity={0.1}
            strokeWidth={3}
            dot={{ fill: CHART_COLORS.primary, strokeWidth: 2, r: 4 }}
          />

          {/* AI Baseline */}
          <Radar
            name='AI Baseline'
            dataKey='aiBaseline'
            stroke={CHART_COLORS.secondary}
            fill={CHART_COLORS.secondary}
            fillOpacity={0.05}
            strokeWidth={2}
            strokeDasharray='5 5'
            dot={{ fill: CHART_COLORS.secondary, strokeWidth: 1, r: 2 }}
          />

          {/* Human Baseline */}
          <Radar
            name='Human Baseline'
            dataKey='humanBaseline'
            stroke={CHART_COLORS.accent}
            fill={CHART_COLORS.accent}
            fillOpacity={0.05}
            strokeWidth={2}
            strokeDasharray='8 3'
            dot={{ fill: CHART_COLORS.accent, strokeWidth: 1, r: 2 }}
          />

          <Tooltip
            contentStyle={{
              backgroundColor: "rgba(255, 255, 255, 0.95)",
              border: "1px solid hsl(var(--border))",
              borderRadius: "6px",
              backdropFilter: "blur(4px)",
            }}
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            formatter={(value: number, name: string, props: any) => {
              const data = props.payload;
              const lines = [];

              if (name === "Current") {
                lines.push(
                  `Current: ${data.originalValue?.toFixed(3)} (${value.toFixed(1)}%)`,
                );
              } else if (name === "AI Baseline" && value) {
                lines.push(`AI Baseline: ${value.toFixed(1)}%`);
              } else if (name === "Human Baseline" && value) {
                lines.push(`Human Baseline: ${value.toFixed(1)}%`);
              }

              if (
                name === "Current" &&
                data.baseline &&
                data.baseline.verdict !== "neutral"
              ) {
                lines.push(
                  `Verdict: ${data.baseline.verdict} (${(data.baseline.confidence * 100).toFixed(0)}%)`,
                );
              }

              if (name === "Current" && data.interpretation) {
                lines.push(`Info: ${data.interpretation}`);
              }

              return [lines.join("\n"), name];
            }}
          />
        </RadarChart>
      </ResponsiveContainer>

      {strongFeatures.some((f) => f.baseline_comparison) && (
        <div className='mt-4 p-3 bg-muted/30 rounded-lg'>
          <h5 className='text-xs font-medium mb-2'>
            Legend & Baseline Insights:
          </h5>

          {/* Legend */}
          <div className='flex items-center gap-4 mb-3 text-xs'>
            <div className='flex items-center gap-1'>
              <div className='w-3 h-0.5 bg-blue-500'></div>
              <span>Current</span>
            </div>
            <div className='flex items-center gap-1'>
              <div className='w-3 h-0.5 bg-red-500 border-dashed border-t'></div>
              <span>AI Baseline</span>
            </div>
            <div className='flex items-center gap-1'>
              <div className='w-3 h-0.5 bg-green-500 border-dashed border-t'></div>
              <span>Human Baseline</span>
            </div>
          </div>

          <div className='grid gap-1 text-xs'>
            {strongFeatures
              .filter(
                (f) =>
                  f.baseline_comparison &&
                  f.baseline_comparison.verdict !== "neutral",
              )
              .slice(0, 3)
              .map((feature, index) => (
                <div key={index} className='flex justify-between'>
                  <span className='truncate'>
                    {feature.name.replace(/_/g, " ")}
                  </span>
                  <Badge
                    variant={
                      feature.baseline_comparison!.verdict === "ai-like"
                        ? "destructive"
                        : "secondary"
                    }
                    className='text-xs h-4'
                  >
                    {feature.baseline_comparison!.verdict}
                  </Badge>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  );
};

const LineChartVisualization = ({ group }: { group: FeatureGroup }) => {
  const data = prepareDataForVisualization(group);

  return (
    <ResponsiveContainer width='100%' height={300}>
      <LineChart
        data={data}
        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray='3 3' className='stroke-muted' />
        <XAxis
          dataKey='name'
          angle={-45}
          textAnchor='end'
          height={80}
          className='text-xs fill-muted-foreground'
        />
        <YAxis className='text-xs fill-muted-foreground' />
        <Tooltip
          contentStyle={{
            backgroundColor: "hsl(var(--background))",
            border: "1px solid hsl(var(--border))",
            borderRadius: "6px",
          }}
        />
        <Line
          type='monotone'
          dataKey='value'
          stroke={CHART_COLORS.primary}
          strokeWidth={2}
          dot={{ fill: CHART_COLORS.primary, strokeWidth: 2, r: 4 }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

const BoxPlotVisualization = ({ group }: { group: FeatureGroup }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const chartRef = useRef<BoxPlotChart | null>(null);

  const chartData = useMemo(() => {
    const features = group.features.filter(
      (f) => f.value !== null && f.value !== undefined,
    );

    return {
      labels: [group.group_name],
      datasets: [
        {
          label: "Feature Values",
          data: [features.map((f) => f.value)], // Array of arrays as required by the library
          backgroundColor: "rgba(59, 130, 246, 0.5)",
          borderColor: "rgb(59, 130, 246)",
          borderWidth: 1,
          outlierColor: "rgb(239, 68, 68)",
          padding: 10,
          itemRadius: 2,
        },
      ],
    };
  }, [group.features, group.group_name]);

  useEffect(() => {
    if (!canvasRef.current) return;

    if (chartRef.current) {
      chartRef.current.destroy();
    }

    chartRef.current = new BoxPlotChart(canvasRef.current, {
      data: chartData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: `${group.group_name} - Feature Distribution`,
          },
          legend: {
            display: false,
          },
          tooltip: {
            callbacks: {
              title: () => group.group_name,
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              label: (context: any) => {
                const stats = context.parsed;
                return [
                  `Min: ${stats.min?.toFixed(3)}`,
                  `Q1: ${stats.q1?.toFixed(3)}`,
                  `Median: ${stats.median?.toFixed(3)}`,
                  `Q3: ${stats.q3?.toFixed(3)}`,
                  `Max: ${stats.max?.toFixed(3)}`,
                ].join("\n");
              },
            },
          },
        },
        scales: {
          y: {
            title: {
              display: true,
              text: "Feature Values",
            },
          },
        },
      },
    });

    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
      }
    };
  }, [chartData, group.group_name]);

  return (
    <div className='h-[300px] w-full'>
      <canvas ref={canvasRef} />
    </div>
  );
};

const ChartVisualization = ({ group }: { group: FeatureGroup }) => {
  switch (group.visualization_type) {
    case "bar":
      return <BarChartVisualization group={group} />;
    case "radar":
      return <RadarChartVisualization group={group} />;
    case "line":
      return <LineChartVisualization group={group} />;
    case "boxplot":
      return <BoxPlotVisualization group={group} />;
    default:
      return <BarChartVisualization group={group} />;
  }
};

export function FeatureCharts({
  featureGroups,
  className,
}: FeatureChartsProps) {
  // FIXME: mockdata
  const mockFeatureGroups: Record<string, FeatureGroup> = {
    structure_metrics: {
      group_name: "Cấu trúc Code",
      description: "Phân tích cấu trúc tổ chức code và patterns",
      visualization_type: "radar",
      group_score: 0.75,
      features: [
        {
          name: "class_complexity",
          value: 0.65,
          normalized: true,
          interpretation: "Độ phức tạp class trung bình",
          weight: 0.8,
          baseline_comparison: {
            ai_baseline: 0.4,
            human_baseline: 0.7,
            current_value: 0.65,
            deviation_from_ai: 0.25,
            deviation_from_human: -0.05,
            ai_similarity: 0.3,
            human_similarity: 0.85,
            verdict: "human-like",
            confidence: 0.82,
            explanation:
              "Code structure shows typical human organization patterns",
          },
        },
        {
          name: "function_density",
          value: 0.82,
          normalized: true,
          interpretation: "Mật độ hàm trong module",
          weight: 0.7,
          baseline_comparison: {
            ai_baseline: 0.9,
            human_baseline: 0.6,
            current_value: 0.82,
            deviation_from_ai: -0.08,
            deviation_from_human: 0.22,
            ai_similarity: 0.75,
            human_similarity: 0.45,
            verdict: "ai-like",
            confidence: 0.68,
            explanation: "High function density typical of AI-generated code",
          },
        },
        {
          name: "inheritance_depth",
          value: 0.45,
          normalized: true,
          interpretation: "Độ sâu kế thừa",
          weight: 0.6,
        },
        {
          name: "module_coupling",
          value: 0.38,
          normalized: true,
          interpretation: "Mức độ liên kết giữa modules",
          weight: 0.75,
        },
        {
          name: "code_organization",
          value: 0.71,
          normalized: true,
          interpretation: "Chất lượng tổ chức code",
          weight: 0.85,
        },
        {
          name: "pattern_consistency",
          value: 0.89,
          normalized: true,
          interpretation: "Tính nhất quán trong pattern",
          weight: 0.9,
          baseline_comparison: {
            ai_baseline: 0.95,
            human_baseline: 0.65,
            current_value: 0.89,
            deviation_from_ai: -0.06,
            deviation_from_human: 0.24,
            ai_similarity: 0.85,
            human_similarity: 0.35,
            verdict: "ai-like",
            confidence: 0.92,
            explanation: "Extremely consistent patterns indicate AI generation",
          },
        },
      ],
    },
    style_metrics: {
      group_name: "Phong cách Code",
      description: "Phân tích style coding và naming conventions",
      visualization_type: "bar",
      group_score: 0.68,
      features: [
        {
          name: "variable_naming_consistency",
          value: 0.92,
          normalized: true,
          interpretation: "Tính nhất quán trong đặt tên biến",
          weight: 0.8,
          baseline_comparison: {
            ai_baseline: 0.95,
            human_baseline: 0.72,
            current_value: 0.92,
            deviation_from_ai: -0.03,
            deviation_from_human: 0.2,
            ai_similarity: 0.88,
            human_similarity: 0.45,
            verdict: "ai-like",
            confidence: 0.76,
            explanation: "Perfect naming consistency suggests AI generation",
          },
        },
        {
          name: "comment_density",
          value: 0.35,
          normalized: true,
          interpretation: "Mật độ comment trong code",
          weight: 0.7,
        },
        {
          name: "indentation_consistency",
          value: 0.98,
          normalized: true,
          interpretation: "Tính nhất quán indentation",
          weight: 0.6,
        },
        {
          name: "line_length_variance",
          value: 0.42,
          normalized: true,
          interpretation: "Độ biến thiên độ dài dòng",
          weight: 0.5,
        },
        {
          name: "bracket_style_consistency",
          value: 0.88,
          normalized: true,
          interpretation: "Nhất quán style đặt bracket",
          weight: 0.65,
        },
      ],
    },
    complexity_metrics: {
      group_name: "Độ phức tạp",
      description: "Đo lường độ phức tạp thuật toán và logic",
      visualization_type: "line",
      group_score: 0.59,
      features: [
        {
          name: "cyclomatic_complexity",
          value: 0.47,
          normalized: true,
          interpretation: "Độ phức tạp cyclomatic",
          weight: 0.9,
        },
        {
          name: "cognitive_complexity",
          value: 0.52,
          normalized: true,
          interpretation: "Độ phức tạp nhận thức",
          weight: 0.85,
        },
        {
          name: "nesting_depth",
          value: 0.38,
          normalized: true,
          interpretation: "Độ sâu lồng nhau",
          weight: 0.7,
        },
        {
          name: "control_flow_complexity",
          value: 0.64,
          normalized: true,
          interpretation: "Phức tạp luồng điều khiển",
          weight: 0.8,
        },
        {
          name: "algorithm_sophistication",
          value: 0.71,
          normalized: true,
          interpretation: "Độ tinh vi thuật toán",
          weight: 0.95,
          baseline_comparison: {
            ai_baseline: 0.85,
            human_baseline: 0.55,
            current_value: 0.71,
            deviation_from_ai: -0.14,
            deviation_from_human: 0.16,
            ai_similarity: 0.65,
            human_similarity: 0.68,
            verdict: "neutral",
            confidence: 0.58,
            explanation: "Moderate algorithm complexity, unclear pattern",
          },
        },
      ],
    },
    ai_detection_metrics: {
      group_name: "Chỉ số AI",
      description: "Các đặc trưng đặc biệt để phát hiện code AI-generated",
      visualization_type: "boxplot",
      group_score: 0.83,
      features: [
        {
          name: "template_pattern_score",
          value: 0.87,
          normalized: true,
          interpretation: "Điểm template patterns",
          weight: 0.95,
          baseline_comparison: {
            ai_baseline: 0.9,
            human_baseline: 0.4,
            current_value: 0.87,
            deviation_from_ai: -0.03,
            deviation_from_human: 0.47,
            ai_similarity: 0.94,
            human_similarity: 0.25,
            verdict: "ai-like",
            confidence: 0.91,
            explanation:
              "Strong template-based patterns indicate AI generation",
          },
        },
        {
          name: "error_handling_uniformity",
          value: 0.94,
          normalized: true,
          interpretation: "Tính đồng đều xử lý lỗi",
          weight: 0.8,
        },
        {
          name: "documentation_completeness",
          value: 0.76,
          normalized: true,
          interpretation: "Độ hoàn thiện tài liệu",
          weight: 0.7,
        },
        {
          name: "code_verbosity",
          value: 0.68,
          normalized: true,
          interpretation: "Độ dài dòng code",
          weight: 0.6,
        },
        {
          name: "api_usage_patterns",
          value: 0.91,
          normalized: true,
          interpretation: "Patterns sử dụng API",
          weight: 0.85,
          baseline_comparison: {
            ai_baseline: 0.92,
            human_baseline: 0.58,
            current_value: 0.91,
            deviation_from_ai: -0.01,
            deviation_from_human: 0.33,
            ai_similarity: 0.97,
            human_similarity: 0.42,
            verdict: "ai-like",
            confidence: 0.89,
            explanation: "API usage follows typical AI-generated patterns",
          },
        },
        {
          name: "redundancy_score",
          value: 0.79,
          normalized: true,
          interpretation: "Điểm trùng lặp code",
          weight: 0.75,
        },
      ],
    },
  };

  // Use mockdata instead of props for demonstration
  const displayGroups =
    Object.keys(mockFeatureGroups).length > 0
      ? mockFeatureGroups
      : featureGroups;
  const groupEntries = Object.entries(displayGroups);

  if (groupEntries.length === 0) {
    return (
      <Card className={className}>
        <CardContent className='flex items-center justify-center py-12'>
          <div className='text-center'>
            <BarChart className='h-12 w-12 text-muted-foreground mx-auto mb-4' />
            <h3 className='font-semibold mb-2'>Không có dữ liệu để hiển thị</h3>
            <p className='text-sm text-muted-foreground'>
              Hãy hoàn tất một lần phân tích để xem trực quan hóa đặc trưng.
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className={`space-y-6 ${className}`}>
      <div className='flex items-center justify-between'>
        <div>
          <h3 className='text-lg font-semibold'>Trực quan hóa đặc trưng</h3>
          <p className='text-sm text-muted-foreground'>
            Biểu đồ tương tác hiển thị kết quả phân tích theo các nhóm đặc trưng
            khác nhau
          </p>
        </div>
        <Badge variant='outline'>{groupEntries.length} nhóm</Badge>
      </div>

      <Tabs defaultValue={groupEntries[0]?.[0]} className='w-full'>
        <TabsList className='grid grid-cols-4 w-full'>
          {groupEntries.map(([groupName, group]) => (
            <TabsTrigger key={groupName} value={groupName} className='text-xs'>
              {group.group_name}
            </TabsTrigger>
          ))}
        </TabsList>

        {groupEntries.map(([groupName, group]) => (
          <TabsContent key={groupName} value={groupName} className='space-y-4'>
            <Card>
              <CardHeader>
                <div className='flex items-center justify-between'>
                  <div>
                    <CardTitle className='flex items-center gap-2'>
                      {group.group_name}
                      <Badge variant='secondary'>
                        {group.visualization_type}
                      </Badge>
                    </CardTitle>
                    <CardDescription>{group.description}</CardDescription>
                  </div>
                  <div className='text-right'>
                    <div className='text-2xl font-bold'>
                      {Math.round(group.group_score * 100)}%
                    </div>
                    <div className='text-xs text-muted-foreground'>
                      Group Score
                    </div>
                  </div>
                </div>
              </CardHeader>

              <CardContent>
                <ChartVisualization group={group} />

                <div className='mt-6 space-y-2'>
                  <h4 className='font-medium text-sm'>Đặc trưng chính:</h4>
                  <div className='grid gap-2 md:grid-cols-2'>
                    {group.features.slice(0, 6).map((feature, index) => (
                      <div
                        key={index}
                        className='flex items-center justify-between p-2 bg-muted/50 rounded'
                      >
                        <span className='text-xs font-medium'>
                          {feature.name.replace(/_/g, " ")}
                        </span>
                        <span className='text-xs font-mono'>
                          {feature.value.toFixed(3)}
                        </span>
                      </div>
                    ))}
                  </div>

                  {group.features.length > 6 && (
                    <p className='text-xs text-muted-foreground text-center'>
                      +{group.features.length - 6} more features
                    </p>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
}

export default FeatureCharts;
