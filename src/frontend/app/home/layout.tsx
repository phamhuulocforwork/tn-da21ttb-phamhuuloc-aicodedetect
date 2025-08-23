import { AnalysisLayout } from "@/components/layout/analysis-layout";

export default function HomeLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <AnalysisLayout showBackground>{children}</AnalysisLayout>;
}
