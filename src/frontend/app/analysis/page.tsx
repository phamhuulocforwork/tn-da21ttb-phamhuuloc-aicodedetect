"use client";

import { useState } from "react";

import { AnalysisResult, CodeEditor } from "./_components/code-editor";
import Header from "./_components/header";
import oneDarkPro from "./_components/onedarkpro.json";

export default function TestPage() {
  const [code, setCode] = useState(`#include <iostream>
#include <cmath>    // dùng sqrt()
using namespace std;

int main() {
  double a, b, c;
  cout << "Nhap he so a, b, c: ";
  cin >> a >> b >> c;

  if (a == 0) {
    if (b == 0) {
      if (c == 0) {
        cout << "Phuong trinh vo so nghiem." << endl;
      } else {
        cout << "Phuong trinh vo nghiem." << endl;
      }
    } else {
      double x = -c / b;
      cout << "Phuong trinh co mot nghiem: x = " << x << endl;
    }
  } else {
    double delta = b * b - 4 * a * c;
    if (delta > 0) {
      double x1 = (-b + sqrt(delta)) / (2 * a);
      double x2 = (-b - sqrt(delta)) / (2 * a);
      cout << "Phuong trinh co hai nghiem phan biet:\n";
      cout << "x1 = " << x1 << ", x2 = " << x2 << endl;
    } else if (delta == 0) {
      double x = -b / (2 * a);
      cout << "Phuong trinh co nghiem kep: x = " << x << endl;
    } else {
      cout << "Phuong trinh vo nghiem thuc." << endl;
    }
  }

  return 0;
}
`);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleCodeChange = (value: string | undefined) => {
    if (value !== undefined) {
      setCode(value);
    }
  };

  const handleSubmitCode = async (): Promise<AnalysisResult> => {
    setIsSubmitting(true);

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

      return mockResult;
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <Header />
      <div className='h-[calc(100vh-var(--header-height))] flex flex-col'>
        <div className='flex-1 p-4'>
          <CodeEditor
            value={code}
            height='100%'
            onChange={handleCodeChange}
            onSubmit={handleSubmitCode}
            isSubmitting={isSubmitting}
            placeholder='Nhập code của bạn vào đây để phân tích...'
            customDarkTheme={{
              base: "vs-dark",
              inherit: true,
              ...oneDarkPro,
            }}
          />
        </div>
      </div>
    </>
  );
}
