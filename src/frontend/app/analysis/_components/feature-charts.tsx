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
        name: `Đặc trưng khác (${weakFeatures.length})`,
        value: avgWeakValue,
        description: `Trung bình của ${weakFeatures.length} đặc trưng khác`,
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
        value: feature.normalized
          ? feature.value * 100
          : Math.min(feature.value * 100, 100),
        originalValue: feature.value,
        fullMark: 100,
        baseline: feature.baseline_comparison,
        interpretation: feature.interpretation,
      };
    });

    if (summary) {
      data.push({
        subject: summary.name,
        value: summary.value * 100,
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
        Có {strongFeatures.length} đặc trưng mạnh
        {summary && ` (${summary.name.match(/\d+/)?.[0]} others grouped)`}
        {strongFeatures.some((f) => f.baseline_comparison) && (
          <span className='block mt-1'>
            * = Sự khác biệt code hiện tại và baseline
          </span>
        )}
      </div>

      <ResponsiveContainer width='100%' height={320}>
        <RadarChart
          data={radarData}
          margin={{ top: 20, right: 40, bottom: 20, left: 40 }}
        >
          <PolarGrid className='stroke-muted' />
          <PolarAngleAxis
            dataKey='subject'
            className='text-xs'
            tick={{ fontSize: 10 }}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            className='text-xs'
            tick={{ fontSize: 9 }}
          />
          <Radar
            name={group.group_name}
            dataKey='value'
            stroke={CHART_COLORS.primary}
            fill={CHART_COLORS.primary}
            fillOpacity={0.2}
            strokeWidth={2}
            dot={{ fill: CHART_COLORS.primary, strokeWidth: 2, r: 3 }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "hsl(var(--background))",
              border: "1px solid hsl(var(--border))",
              borderRadius: "6px",
            }}
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            formatter={(value: number, name: string, props: any) => {
              const data = props.payload;
              const lines = [
                `Value: ${data.originalValue?.toFixed(3)}`,
                `Normalized: ${value.toFixed(1)}%`,
              ];

              if (data.baseline && data.baseline.verdict !== "neutral") {
                lines.push(
                  `Baseline: ${data.baseline.verdict} (${(data.baseline.confidence * 100).toFixed(0)}%)`,
                );
              }

              if (data.interpretation) {
                lines.push(`Info: ${data.interpretation}`);
              }

              return [lines.join("\n"), name];
            }}
          />
        </RadarChart>
      </ResponsiveContainer>

      {strongFeatures.some((f) => f.baseline_comparison) && (
        <div className='mt-4 p-3 bg-muted/30 rounded-lg'>
          <h5 className='text-xs font-medium mb-2'>Nhận xét:</h5>
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
  const groupEntries = Object.entries(featureGroups);

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
        <TabsList>
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
