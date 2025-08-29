import {
  AIMDXResponse,
  AnalysisMethodsResponse,
  AnalysisResponse,
  ApiEndpoints,
  ApiError,
  BatchAnalysisRequest,
  BatchAnalysisResponse,
  CodeAnalysisRequest,
} from "./api-types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const defaultOptions: RequestInit = {
      headers: {
        "Content-Type": "application/json",
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
          //TODO:
        }

        throw new Error(errorMessage);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }

      throw new Error(
        `Request failed: ${error instanceof Error ? error.message : "Unknown error"}`,
      );
    }
  }

  async healthCheck(): Promise<{
    status: string;
    timestamp: string;
    modules: Record<string, boolean>;
  }> {
    return this.request(ApiEndpoints.HEALTH);
  }

  async getAnalysisMethods(): Promise<AnalysisMethodsResponse> {
    return this.request(ApiEndpoints.METHODS);
  }

  async analyzeCombined(
    request: CodeAnalysisRequest,
  ): Promise<AnalysisResponse> {
    return this.request(ApiEndpoints.COMBINED_ANALYSIS, {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  async analyzeAI(request: CodeAnalysisRequest): Promise<AIMDXResponse> {
    return this.request(ApiEndpoints.AI_ANALYSIS, {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  async analyzeFile(
    file: File,
    analysisType: "combined" | "ai" = "combined",
    language: string = "c",
  ): Promise<AnalysisResponse | AIMDXResponse> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("analysis_type", analysisType);
    formData.append("language", language);

    return this.request(ApiEndpoints.UPLOAD_FILE, {
      method: "POST",
      body: formData,
      headers: {},
    });
  }

  // Batch Analysis Methods
  async uploadBatchZip(
    file: File,
    batchName: string = "Batch Analysis",
  ): Promise<BatchAnalysisResponse> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("batch_name", batchName);

    return this.request(ApiEndpoints.BATCH_UPLOAD_ZIP, {
      method: "POST",
      body: formData,
      headers: {},
    });
  }

  async analyzeBatchGoogleDrive(
    request: BatchAnalysisRequest,
  ): Promise<BatchAnalysisResponse> {
    return this.request(ApiEndpoints.BATCH_GOOGLE_DRIVE, {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  async getBatchStatus(batchId: string): Promise<BatchAnalysisResponse> {
    const endpoint = ApiEndpoints.BATCH_STATUS.replace("{batch_id}", batchId);
    return this.request(endpoint);
  }

  async getBatchResults(batchId: string): Promise<BatchAnalysisResponse> {
    const endpoint = ApiEndpoints.BATCH_RESULTS.replace("{batch_id}", batchId);
    return this.request(endpoint);
  }

  async getBatchMethods(): Promise<{
    methods: Array<{
      id: string;
      name: string;
      description: string;
      supported_formats?: string[];
      supported_languages?: string[];
      max_file_size?: string;
      features?: string[];
    }>;
  }> {
    return this.request(ApiEndpoints.BATCH_METHODS);
  }
}

export const apiClient = new ApiClient();

export const isAnalysisResponse = (
  response: AnalysisResponse | AIMDXResponse,
): response is AnalysisResponse => {
  return "feature_groups" in response && "assessment" in response;
};

export const isAIMDXResponse = (
  response: AnalysisResponse | AIMDXResponse,
): response is AIMDXResponse => {
  return (
    "mdx_content" in response &&
    "analysis_type" in response &&
    (response as AIMDXResponse).analysis_type === "ai_mdx"
  );
};

export const handleApiError = (error: unknown): string => {
  if (error instanceof Error) {
    return error.message;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "An unexpected error occurred";
};

export const isApiError = (error: unknown): error is Error => {
  return error instanceof Error;
};

export const cacheAnalysisResult = (
  key: string,
  result: AnalysisResponse | AIMDXResponse,
): void => {
  try {
    const cached = {
      result,
      timestamp: Date.now(),
      expires: Date.now() + 60 * 60 * 1000,
    };
    localStorage.setItem(`analysis_${key}`, JSON.stringify(cached));
  } catch (error) {
    console.warn("Failed to cache analysis result:", error);
  }
};

export const getCachedAnalysisResult = (
  key: string,
): AnalysisResponse | AIMDXResponse | null => {
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
    console.warn("Failed to get cached analysis result:", error);
    return null;
  }
};

export type { ApiError };
