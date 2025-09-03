import React from "react";

import type { FileAnalysisResult } from "@/lib/api-types";

interface AnalysisStatsProps {
  result: FileAnalysisResult;
  className?: string;
}

export function AnalysisStats({ result, className = "" }: AnalysisStatsProps) {
  const aiSimilarity = result.ai_similarity || 0;
  const humanSimilarity = result.human_similarity || 0;

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <div className='flex items-center gap-1 bg-red-50 border border-red-200 rounded-full px-3 py-1 min-w-0'>
        <span className='text-xs font-medium text-red-700'>AI:</span>
        <span className='font-bold text-red-600'>
          {Math.round(aiSimilarity)}%
        </span>
      </div>

      <div className='flex items-center gap-1 bg-green-50 border border-green-200 rounded-full px-3 py-1 min-w-0'>
        <span className='text-xs font-medium text-green-700'>Human:</span>
        <span className='font-bold text-green-600'>
          {Math.round(humanSimilarity)}%
        </span>
      </div>
    </div>
  );
}

export default AnalysisStats;
