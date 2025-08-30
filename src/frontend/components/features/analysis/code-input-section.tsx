import React from "react";

import { CodeEditor } from "@/components/blocks/code-editor/code-editor";
import oneDarkPro from "@/components/blocks/code-editor/onedarkpro.json";
import { CodeStats } from "@/components/shared/code-stats";
import { SectionHeader } from "@/components/shared/section-header";

import { AnalysisMode } from "./types";

interface CodeInputSectionProps {
  code: string;
  onCodeChange: (value: string | undefined) => void;
  onSubmit: (code: string, language: string) => Promise<unknown>;
  isSubmitting: boolean;
  analysisMode: AnalysisMode;
  onFileContentLoaded?: (content: string, filename: string) => void;
}

export function CodeInputSection({
  code,
  onCodeChange,
  isSubmitting,
  analysisMode,
  onFileContentLoaded,
}: CodeInputSectionProps) {
  return (
    <div className='space-y-4'>
      <SectionHeader title='Mã nguồn'>
        <CodeStats code={code} />
      </SectionHeader>

      <CodeEditor
        value={code}
        height='400px'
        onChange={onCodeChange}
        isSubmitting={isSubmitting}
        analysisMode={analysisMode}
        onFileContentLoaded={onFileContentLoaded}
        placeholder='Dán mã C/C++ vào đây để phân tích...'
        customDarkTheme={{
          base: "vs-dark",
          inherit: true,
          ...oneDarkPro,
        }}
      />
    </div>
  );
}

export default CodeInputSection;
