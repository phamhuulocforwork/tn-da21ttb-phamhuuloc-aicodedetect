// API Types for AI Code Detection Backend
// Based on backend API specification

export interface CodeAnalysisRequest {
  code: string;
  filename?: string;
  language: string;
}

export interface FeatureInfo {
  name: string;
  value: number;
  normalized: boolean;
  interpretation: string;
  weight: number;
}

export interface FeatureGroup {
  group_name: string;
  description: string;
  features: FeatureInfo[];
  group_score: number;
  visualization_type: 'bar' | 'radar' | 'boxplot' | 'line';
}

export interface AssessmentResult {
  overall_score: number; // 0=human-like, 1=AI-like
  confidence: number;    // confidence level
  key_indicators: string[];
  summary: string;
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

// Individual analysis response types
export interface IndividualAnalysisResponse {
  success: boolean;
  analysis_id: string;
  timestamp: string;
  analysis_type: string;
  code_info: CodeInfo;
  features: Record<string, number>;
  summary: string;
}

// Analysis methods info
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

// Error response
export interface ApiError {
  detail: string;
}

// API endpoints enum
export enum ApiEndpoints {
  HEALTH = '/health',
  COMBINED_ANALYSIS = '/api/analysis/combined-analysis',
  AST_ANALYSIS = '/api/analysis/ast-analysis',
  HUMAN_STYLE = '/api/analysis/human-style',
  ADVANCED_FEATURES = '/api/analysis/advanced-features',
  UPLOAD_FILE = '/api/analysis/upload-file',
  METHODS = '/api/analysis/methods'
}