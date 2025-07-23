"use client";

import { useState } from "react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import { AnalysisResults } from "./_components/analysis-results";
import { AnalysisResult, CodeEditor } from "./_components/code-editor";
import Header from "./_components/header";
// import Header from "./_components/header";
import oneDarkPro from "./_components/onedarkpro.json";
import { UserGuide } from "./_components/user-guide";

// import { UserGuide } from "./_components/user-guide";

export default function TestPage() {
  const [code, setCode] = useState(`#include <iostream>

int main() {
    cout << "Hello, World!" << endl;

    return 0;
}
`);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(
    null,
  );
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const handleCodeChange = (value: string | undefined) => {
    if (value !== undefined) {
      setCode(value);
    }
  };

  const handleSubmitCode = async (): Promise<AnalysisResult> => {
    setIsSubmitting(true);
    setShowResults(false);

    try {
      await new Promise((resolve) => setTimeout(resolve, 2000));

      const mockResult: AnalysisResult = {
        isAiGenerated: Math.random() > 0.5,
        confidence: Math.random() * 0.4 + 0.6,
        features: {
          complexity: Math.random() * 10 + 1,
          redundancy: Math.random() * 0.3,
          namingPatterns: Math.random() * 5 + 3,
          comments: Math.random() * 0.4,
        },
        reasons: [
          "Unusual variable naming patterns detected",
          "Code structure suggests algorithmic generation",
          "Comments are too systematic for typical student code",
          "Low complexity variations indicate AI assistance",
        ].slice(0, Math.floor(Math.random() * 4) + 1),
      };

      setAnalysisResult(mockResult);
      setShowResults(true);
      return mockResult;
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className='flex flex-col h-screen'>
      <Header />
      <div className='h-[calc(100vh-var(--header-height))] '>
        <div className='container mx-auto p-4 h-full'>
          <div
            className={`grid gap-4 md:gap-6 h-full transition-all duration-500 ease-in-out ${
              showResults
                ? "grid-cols-1 lg:grid-cols-12"
                : "grid-cols-1 lg:grid-cols-8"
            }`}
          >
            {!showResults && (
              <div className='order-2 lg:order-1 transition-all duration-500 ease-in-out lg:col-span-2'>
                <UserGuide />
              </div>
            )}

            <div
              className={`order-1 lg:order-2 transition-all duration-500 ease-in-out ${
                showResults ? "lg:col-span-8" : "lg:col-span-6"
              }`}
            >
              <Card className='h-full flex flex-col'>
                <CardHeader className='pb-3 flex-shrink-0'>
                  <CardTitle className='text-lg'>Code Editor</CardTitle>
                </CardHeader>
                <CardContent className='flex-1 flex flex-col'>
                  <CodeEditor
                    value={code}
                    onChange={handleCodeChange}
                    height='100%'
                    onSubmit={handleSubmitCode}
                    isSubmitting={isSubmitting}
                    placeholder='Nhập code của bạn vào đây để phân tích...'
                    customDarkTheme={{
                      base: "vs-dark",
                      inherit: true,
                      ...oneDarkPro,
                    }}
                  />
                </CardContent>
              </Card>
            </div>

            {showResults && (
              <div className='lg:col-span-4 order-3 animate-in slide-in-from-right-10 duration-700 ease-out'>
                <AnalysisResults
                  result={analysisResult}
                  isVisible={showResults}
                />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
