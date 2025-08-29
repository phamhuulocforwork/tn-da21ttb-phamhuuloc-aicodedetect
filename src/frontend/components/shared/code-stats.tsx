import React from "react";

interface CodeStatsProps {
  code: string;
  className?: string;
}

export function CodeStats({ code, className = "" }: CodeStatsProps) {
  if (!code?.trim()) return null;

  const lineCount = code.split("\n").length;
  const sizeInKB = Math.round((code.length / 1024) * 10) / 10;

  return (
    <div className={`text-sm text-muted-foreground ${className}`}>
      {lineCount} dòng • Kích thước: {sizeInKB} KB
    </div>
  );
}

export default CodeStats;
