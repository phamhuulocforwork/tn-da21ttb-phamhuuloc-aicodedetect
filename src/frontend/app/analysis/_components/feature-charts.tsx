"use client";

import { useMemo } from "react";

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
  const data = prepareDataForVisualization(group);

  return (
    <ResponsiveContainer width='100%' height={300}>
      <RadarChart
        data={data}
        margin={{ top: 20, right: 30, bottom: 20, left: 30 }}
      >
        <PolarGrid className='stroke-muted' />
        <PolarAngleAxis
          dataKey='subject'
          className='text-xs fill-muted-foreground'
          tick={{ fontSize: 12 }}
        />
        <PolarRadiusAxis
          angle={90}
          domain={[0, 100]}
          className='text-xs fill-muted-foreground'
        />
        <Radar
          name={group.group_name}
          dataKey='value'
          stroke={CHART_COLORS.primary}
          fill={CHART_COLORS.primary}
          fillOpacity={0.2}
          strokeWidth={2}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: "hsl(var(--background))",
            border: "1px solid hsl(var(--border))",
            borderRadius: "6px",
          }}
        />
      </RadarChart>
    </ResponsiveContainer>
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
  const stats = useMemo(() => {
    const values = group.features.map((f) => f.value);
    values.sort((a, b) => a - b);

    const q1 = values[Math.floor(values.length * 0.25)];
    const median = values[Math.floor(values.length * 0.5)];
    const q3 = values[Math.floor(values.length * 0.75)];
    const min = values[0];
    const max = values[values.length - 1];

    return { min, q1, median, q3, max };
  }, [group.features]);

  return (
    <div className='h-[300px] flex items-center justify-center'>
      <div className='text-center space-y-4'>
        <div className='grid grid-cols-5 gap-4 text-sm'>
          <div className='space-y-1'>
            <div className='font-medium'>Min</div>
            <div className='text-muted-foreground'>{stats.min.toFixed(3)}</div>
          </div>
          <div className='space-y-1'>
            <div className='font-medium'>Q1</div>
            <div className='text-muted-foreground'>{stats.q1.toFixed(3)}</div>
          </div>
          <div className='space-y-1'>
            <div className='font-medium'>Median</div>
            <div className='text-muted-foreground'>
              {stats.median.toFixed(3)}
            </div>
          </div>
          <div className='space-y-1'>
            <div className='font-medium'>Q3</div>
            <div className='text-muted-foreground'>{stats.q3.toFixed(3)}</div>
          </div>
          <div className='space-y-1'>
            <div className='font-medium'>Max</div>
            <div className='text-muted-foreground'>{stats.max.toFixed(3)}</div>
          </div>
        </div>

        <div className='text-xs text-muted-foreground'>
          Box plot visualization coming soon with Chart.js integration
        </div>
      </div>
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
