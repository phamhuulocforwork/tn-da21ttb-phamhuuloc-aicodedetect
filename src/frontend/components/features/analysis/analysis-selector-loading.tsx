import React from "react";

import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export function AnalysisSelectorLoading() {
  return (
    <div className='space-y-4'>
      <div className='flex items-center gap-2 mb-4'>
        <Skeleton className='h-5 w-32' />
        <Skeleton className='h-4 w-24' />
      </div>
      <div className='grid gap-4 md:grid-cols-2'>
        {Array.from({ length: 2 }).map((_, i) => (
          <Card key={i}>
            <CardHeader>
              <div className='flex items-start justify-between'>
                <div className='space-y-2 flex-1'>
                  <Skeleton className='h-5 w-32' />
                  <Skeleton className='h-4 w-full' />
                </div>
                <Skeleton className='h-4 w-16' />
              </div>
            </CardHeader>
            <CardContent>
              <div className='space-y-2'>
                <Skeleton className='h-4 w-24' />
                <div className='flex flex-wrap gap-1'>
                  {Array.from({ length: 3 }).map((_, j) => (
                    <Skeleton key={j} className='h-6 w-20' />
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

export default AnalysisSelectorLoading;
