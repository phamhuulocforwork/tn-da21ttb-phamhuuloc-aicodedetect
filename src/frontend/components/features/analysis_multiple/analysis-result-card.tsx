import { DynamicLink } from "@/components/shared/dynamic-link";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

import type { FileAnalysisResult } from "@/lib/api-types";

import { FileInfo } from "./file-info";

function encodeFileContent(content: string): string {
  return encodeURIComponent(content);
}

interface AnalysisResultCardProps {
  result: FileAnalysisResult;
}

export function AnalysisResultCard({ result }: AnalysisResultCardProps) {
  return (
    <Card
      key={result.analysis_id || result.filename}
      className='hover:shadow-2xl shadow transition-shadow p-0'
    >
      <CardContent className='p-4 flex w-full justify-between'>
        <div className='flex items-start gap-2'>
          <FileInfo
            filename={result.filename}
            language={result.language}
            file_size={result.file_size}
            loc={result.loc}
          />
        </div>

        <Tooltip>
          <TooltipTrigger>
            <DynamicLink
              href={`/analysis?code=${encodeFileContent(result.code_content || "")}`}
              isExternal
            />
          </TooltipTrigger>
          <TooltipContent>Xem chi tiết</TooltipContent>
        </Tooltip>
      </CardContent>
    </Card>
  );
}

export function AnalysisResultCardSkeleton() {
  return (
    <Card className='hover:shadow-2xl shadow transition-shadow p-0'>
      <CardContent className='p-4 flex w-full justify-between'>
        <div className='flex items-start gap-2'>
          <Skeleton className='h-8 w-8' />
          <Skeleton className='h-8 w-8' />
        </div>
      </CardContent>
    </Card>
  );
}

export default AnalysisResultCard;
