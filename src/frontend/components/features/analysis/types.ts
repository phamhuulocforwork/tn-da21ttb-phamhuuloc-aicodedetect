export type AnalysisMode = "combined" | "ai";

export interface AnalysisMethodConfig {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  description: string;
  features: string[];
  timeEstimate: string;
  badge?: string;
}

export interface AnalysisSelectorProps {
  value: AnalysisMode;
  onChange: (mode: AnalysisMode) => void;
  disabled?: boolean;
}

export interface AnalysisMethodsInfo {
  supported_languages: string[];
  max_file_size: string;
}
