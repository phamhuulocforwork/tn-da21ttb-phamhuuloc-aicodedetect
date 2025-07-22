import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// API Types and utilities for code analysis
export interface CodeAnalysisRequest {
  code: string;
  language: string;
  metadata?: {
    studentId?: string;
    assignmentId?: string;
    timestamp?: string;
  };
}

export interface CodeFeatures {
  complexity: number;
  redundancy: number;
  namingPatterns: number;
  comments: number;
  astNodes?: number;
  uniqueTokens?: number;
  averageLineLength?: number;
}

export interface AnalysisResponse {
  isAiGenerated: boolean;
  confidence: number;
  features: CodeFeatures;
  reasons: string[];
  model?: string;
  timestamp?: string;
}

// API endpoints
export const API_ENDPOINTS = {
  ANALYZE_CODE: "/api/analyze",
  GET_HISTORY: "/api/history",
  GET_STATS: "/api/stats",
} as const;

// Utility function to call analysis API
export async function analyzeCode(
  request: CodeAnalysisRequest,
): Promise<AnalysisResponse> {
  const response = await fetch(API_ENDPOINTS.ANALYZE_CODE, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Analysis failed: ${response.statusText}`);
  }

  return response.json();
}

// Language detection utilities
export const LANGUAGE_PATTERNS = {
  c: {
    patterns: [
      /#include\s*<.*\.h>/,
      /int\s+main\s*\(/,
      /printf\s*\(/,
      /scanf\s*\(/,
      /\bmalloc\s*\(/,
      /\bfree\s*\(/,
    ],
    keywords: [
      "int",
      "char",
      "float",
      "double",
      "void",
      "struct",
      "union",
      "enum",
    ],
  },
  cpp: {
    patterns: [
      /#include\s*<iostream>/,
      /std::/,
      /cout\s*<</,
      /cin\s*>>/,
      /namespace\s+std/,
      /class\s+\w+/,
    ],
    keywords: [
      "class",
      "public",
      "private",
      "protected",
      "template",
      "namespace",
    ],
  },
  java: {
    patterns: [
      /public\s+class\s+\w+/,
      /public\s+static\s+void\s+main/,
      /System\.out\./,
      /import\s+java\./,
      /\bnew\s+\w+\s*\(/,
    ],
    keywords: ["public", "private", "protected", "static", "final", "abstract"],
  },
  python: {
    patterns: [
      /def\s+\w+\s*\(/,
      /import\s+\w+/,
      /from\s+\w+\s+import/,
      /print\s*\(/,
      /if\s+__name__\s*==\s*["']__main__["']/,
    ],
    keywords: [
      "def",
      "class",
      "import",
      "from",
      "if",
      "elif",
      "else",
      "for",
      "while",
    ],
  },
  javascript: {
    patterns: [
      /\b(const|let|var)\s+\w+/,
      /function\s+\w+\s*\(/,
      /=>\s*{/,
      /console\.log\s*\(/,
      /require\s*\(/,
    ],
    keywords: ["const", "let", "var", "function", "class", "import", "export"],
  },
  typescript: {
    patterns: [
      /\b(interface|type)\s+\w+/,
      /:\s*(string|number|boolean)/,
      /\bnamespace\s+\w+/,
      /\bas\s+\w+/,
    ],
    keywords: ["interface", "type", "namespace", "enum", "readonly", "keyof"],
  },
} as const;

export function detectLanguage(code: string): string {
  const scores: Record<string, number> = {};

  for (const [lang, config] of Object.entries(LANGUAGE_PATTERNS)) {
    let score = 0;

    // Check patterns
    for (const pattern of config.patterns) {
      if (pattern.test(code)) {
        score += 2;
      }
    }

    // Check keywords
    for (const keyword of config.keywords) {
      const keywordRegex = new RegExp(`\\b${keyword}\\b`, "g");
      const matches = code.match(keywordRegex);
      if (matches) {
        score += matches.length;
      }
    }

    scores[lang] = score;
  }

  const detectedLang = Object.entries(scores).reduce((a, b) =>
    scores[a[0]] > scores[b[0]] ? a : b,
  )[0];

  return scores[detectedLang] > 0 ? detectedLang : "c";
}

// Validation utilities
export function validateCode(code: string): {
  isValid: boolean;
  errors: string[];
} {
  const errors: string[] = [];

  if (!code.trim()) {
    errors.push("Code cannot be empty");
  }

  if (code.length > 50000) {
    errors.push("Code is too long (maximum 50,000 characters)");
  }

  if (code.length < 10) {
    errors.push("Code is too short (minimum 10 characters)");
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

// Format confidence as percentage
export function formatConfidence(confidence: number): string {
  return `${(confidence * 100).toFixed(1)}%`;
}

// Get confidence level description
export function getConfidenceLevel(confidence: number): {
  level: "low" | "medium" | "high";
  description: string;
  color: string;
} {
  if (confidence >= 0.8) {
    return {
      level: "high",
      description: "Rất có thể được tạo bởi AI",
      color: "text-red-500",
    };
  } else if (confidence >= 0.6) {
    return {
      level: "medium",
      description: "Nghi ngờ có sự hỗ trợ của AI",
      color: "text-yellow-500",
    };
  } else {
    return {
      level: "low",
      description: "Có thể là code viết bởi sinh viên",
      color: "text-green-500",
    };
  }
}
