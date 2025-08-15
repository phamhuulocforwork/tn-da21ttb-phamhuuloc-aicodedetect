// API Client for AI Code Detection Backend

import { 
  AnalysisMethodsResponse, 
  AnalysisResponse, 
  ApiEndpoints, 
  ApiError,
  CodeAnalysisRequest,
  IndividualAnalysisResponse 
} from './api-types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    const requestOptions = { ...defaultOptions, ...options };

    try {
      const response = await fetch(url, requestOptions);
      
      if (!response.ok) {
        let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
        
        try {
          const errorData: ApiError = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch {
          // If JSON parsing fails, use the default error message
        }
        
        throw new ApiError(response.status, errorMessage);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      
      // Network or other errors
      throw new Error(`Request failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  // Health check
  async healthCheck(): Promise<{ status: string; timestamp: string; modules: Record<string, boolean> }> {
    return this.request(ApiEndpoints.HEALTH);
  }

  // Get available analysis methods
  async getAnalysisMethods(): Promise<AnalysisMethodsResponse> {
    return this.request(ApiEndpoints.METHODS);
  }

  // Combined analysis (all features)
  async analyzeCombined(request: CodeAnalysisRequest): Promise<AnalysisResponse> {
    return this.request(ApiEndpoints.COMBINED_ANALYSIS, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // AST analysis only
  async analyzeAst(request: CodeAnalysisRequest): Promise<IndividualAnalysisResponse> {
    return this.request(ApiEndpoints.AST_ANALYSIS, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Human style analysis only
  async analyzeHumanStyle(request: CodeAnalysisRequest): Promise<IndividualAnalysisResponse> {
    return this.request(ApiEndpoints.HUMAN_STYLE, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Advanced features analysis only
  async analyzeAdvanced(request: CodeAnalysisRequest): Promise<IndividualAnalysisResponse> {
    return this.request(ApiEndpoints.ADVANCED_FEATURES, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // File upload analysis
  async analyzeFile(
    file: File, 
    analysisType: 'combined' | 'ast' | 'human-style' | 'advanced' = 'combined',
    language: string = 'c'
  ): Promise<AnalysisResponse | IndividualAnalysisResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('analysis_type', analysisType);
    formData.append('language', language);

    return this.request(ApiEndpoints.UPLOAD_FILE, {
      method: 'POST',
      body: formData,
      headers: {
        // Don't set Content-Type for FormData, let the browser set it with boundary
      },
    });
  }

  // Generic analysis method
  async analyze(
    request: CodeAnalysisRequest,
    method: 'combined' | 'ast' | 'human-style' | 'advanced' = 'combined'
  ): Promise<AnalysisResponse | IndividualAnalysisResponse> {
    switch (method) {
      case 'combined':
        return this.analyzeCombined(request);
      case 'ast':
        return this.analyzeAst(request);
      case 'human-style':
        return this.analyzeHumanStyle(request);
      case 'advanced':
        return this.analyzeAdvanced(request);
      default:
        throw new Error(`Unknown analysis method: ${method}`);
    }
  }
}

// Default API client instance
export const apiClient = new ApiClient();

// Utility functions
export const isAnalysisResponse = (
  response: AnalysisResponse | IndividualAnalysisResponse
): response is AnalysisResponse => {
  return 'feature_groups' in response && 'assessment' in response;
};

export const isIndividualAnalysisResponse = (
  response: AnalysisResponse | IndividualAnalysisResponse
): response is IndividualAnalysisResponse => {
  return 'analysis_type' in response && 'features' in response;
};

// Error handling utilities
export const handleApiError = (error: unknown): string => {
  if (error instanceof ApiError) {
    return error.message;
  }
  
  if (error instanceof Error) {
    return error.message;
  }
  
  return 'An unexpected error occurred';
};

// Type guards
export const isApiError = (error: unknown): error is ApiError => {
  return error instanceof ApiError;
};

// Local storage utilities for caching
export const cacheAnalysisResult = (key: string, result: AnalysisResponse | IndividualAnalysisResponse): void => {
  try {
    const cached = {
      result,
      timestamp: Date.now(),
      expires: Date.now() + (60 * 60 * 1000), // 1 hour
    };
    localStorage.setItem(`analysis_${key}`, JSON.stringify(cached));
  } catch (error) {
    console.warn('Failed to cache analysis result:', error);
  }
};

export const getCachedAnalysisResult = (key: string): AnalysisResponse | IndividualAnalysisResponse | null => {
  try {
    const cached = localStorage.getItem(`analysis_${key}`);
    if (!cached) return null;
    
    const { result, expires } = JSON.parse(cached);
    if (Date.now() > expires) {
      localStorage.removeItem(`analysis_${key}`);
      return null;
    }
    
    return result;
  } catch (error) {
    console.warn('Failed to get cached analysis result:', error);
    return null;
  }
};

export { ApiError };