import React from "react";

import { AppLayout } from "./app-layout";
import { GradientBackground } from "./gradient-background";

interface AnalysisLayoutProps {
  children: React.ReactNode;
  showBackground?: boolean;
  title?: string;
  subtitle?: string;
}

export function AnalysisLayout({
  children,
  showBackground = false,
  title = "HỆ THỐNG PHÂN TÍCH MÃ NGUỒN",
  subtitle = "Phát hiện AI-generated code trong bài tập lập trình của sinh viên",
}: AnalysisLayoutProps) {
  if (showBackground) {
    return <GradientBackground>{children}</GradientBackground>;
  }

  return (
    <AppLayout title={title} subtitle={subtitle}>
      {children}
    </AppLayout>
  );
}

export default AnalysisLayout;
