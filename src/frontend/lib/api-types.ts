export interface CodeAnalysisRequest {
  code: string;
  filename?: string;
  language: string;
}

export interface BaselineComparison {
  ai_baseline: number;
  human_baseline: number;
  current_value: number;
  deviation_from_ai: number;
  deviation_from_human: number;
  ai_similarity: number;
  human_similarity: number;
  verdict: "ai-like" | "human-like" | "neutral";
  confidence: number;
  explanation: string;
}

export interface FeatureInfo {
  name: string;
  value: number;
  normalized: boolean;
  interpretation: string;
  weight: number;
  baseline_comparison?: BaselineComparison;
}

export interface FeatureGroup {
  group_name: string;
  description: string;
  features: FeatureInfo[];
  group_score: number;
  visualization_type: "bar" | "radar" | "boxplot" | "line";
}

export interface BaselineSummary {
  total_features_compared: number;
  ai_like_features: number;
  human_like_features: number;
  neutral_features: number;
  strongest_ai_indicators: string[];
  strongest_human_indicators: string[];
  overall_ai_similarity: number;
  overall_human_similarity: number;
}

export interface AssessmentResult {
  overall_score: number;
  confidence: number;
  key_indicators: string[];
  summary: string;
  baseline_summary?: BaselineSummary;
}

export interface CodeInfo {
  filename: string;
  language: string;
  loc: number;
  file_size: number;
}

export interface AnalysisResponse {
  success: boolean;
  analysis_id: string;
  timestamp: string;
  code_info: CodeInfo;
  feature_groups: {
    structure_metrics: FeatureGroup;
    style_metrics: FeatureGroup;
    complexity_metrics: FeatureGroup;
    ai_detection_metrics: FeatureGroup;
  };
  assessment: AssessmentResult;
  raw_features?: Record<string, number>;
}

export interface IndividualAnalysisResponse {
  success: boolean;
  analysis_id: string;
  timestamp: string;
  analysis_type: string;
  code_info: CodeInfo;
  features: Record<string, number>;
  summary: string;
}

export interface GeminiProbabilityAnalysis {
  ai_likelihood: number;
  human_likelihood: number;
  uncertainty_level: number;
}

export interface GeminiDetailedAnalysis {
  style_assessment: string;
  structure_assessment: string;
  syntax_assessment: string;
  overall_assessment: string;
}

export interface GeminiAnalysisResult {
  prediction: "AI-generated" | "Human-written";
  confidence: number;
  probability_analysis: GeminiProbabilityAnalysis;
  reasoning: string[];
  key_indicators: string[];
  ai_patterns_detected: string[];
  human_patterns_detected: string[];
  detailed_analysis: GeminiDetailedAnalysis;
  confidence_explanation: string;
  additional_notes: string;
}

export interface GeminiResponse {
  success: boolean;
  ai_analysis?: GeminiAnalysisResult;
  raw_response?: string;
  model?: string;
  error?: string;
  fallback_analysis?: GeminiAnalysisResult;
}

export interface AIMDXResponse {
  success: boolean;
  analysis_id: string;
  timestamp: string;
  analysis_type: "ai_mdx";
  code_info: CodeInfo;
  mdx_content: string;
  model: string;
  summary: string;
}

export interface AnalysisMethod {
  id: string;
  name: string;
  description: string;
  features: string[];
  estimated_time: string;
}

export interface AnalysisMethodsResponse {
  methods: AnalysisMethod[];
  supported_languages: string[];
  supported_extensions: string[];
  max_file_size: string;
  max_code_length: number;
}

export interface ApiError {
  detail: string;
}

export enum ApiEndpoints {
  HEALTH = "/health",
  COMBINED_ANALYSIS = "/api/analysis/combined-analysis",
  AST_ANALYSIS = "/api/analysis/ast-analysis",
  HUMAN_STYLE = "/api/analysis/human-style",
  ADVANCED_FEATURES = "/api/analysis/advanced-features",
  AI_ANALYSIS = "/api/analysis/ai-analysis",
  UPLOAD_FILE = "/api/analysis/upload-file",
  METHODS = "/api/analysis/methods",
}
