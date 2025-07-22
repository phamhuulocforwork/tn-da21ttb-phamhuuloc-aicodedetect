"use client";

import { useState } from "react";

import { ThemeToggle } from "@/components/theme-toggle";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import { AnalysisResults } from "./_components/analysis-results";
import { AnalysisResult, CodeEditor } from "./_components/code-editor";
import oneDarkPro from "./_components/onedarkpro.json";
import { UserGuide } from "./_components/user-guide";

export default function TestPage() {
  const [code, setCode] = useState(`#include <iostream>
#include <vector>
#include <queue>

using namespace std;

// Định nghĩa node của danh sách liên kết
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {}
};

// So sánh để tạo min-heap trong priority_queue
struct Compare {
    bool operator()(ListNode* a, ListNode* b) {
        return a->val > b->val; // min-heap
    }
};

ListNode* mergeKLists(vector<ListNode*>& lists) {
    priority_queue<ListNode*, vector<ListNode*>, Compare> pq;

    // Bước 1: Đưa node đầu tiên của mỗi danh sách vào heap
    for (ListNode* list : lists) {
        if (list != nullptr) {
            pq.push(list);
        }
    }

    // Dummy node để dễ quản lý danh sách kết quả
    ListNode* dummy = new ListNode(0);
    ListNode* tail = dummy;

    // Bước 2: Lặp cho đến khi heap rỗng
    while (!pq.empty()) {
        ListNode* node = pq.top(); pq.pop();
        tail->next = node;
        tail = tail->next;
        if (node->next != nullptr) {
            pq.push(node->next);
        }
    }

    return dummy->next;
}

// Hàm tiện ích để tạo danh sách liên kết từ vector
ListNode* createList(const vector<int>& nums) {
    ListNode* dummy = new ListNode(0);
    ListNode* tail = dummy;
    for (int num : nums) {
        tail->next = new ListNode(num);
        tail = tail->next;
    }
    return dummy->next;
}

// Hàm in danh sách liên kết
void printList(ListNode* head) {
    while (head != nullptr) {
        cout << head->val;
        if (head->next != nullptr) cout << "->";
        head = head->next;
    }
    cout << endl;
}

// Main để test
int main() {
    vector<vector<int>> input = {{1, 4, 5}, {1, 3, 4}, {2, 6}};
    vector<ListNode*> lists;

    for (const auto& vec : input) {
        lists.push_back(createList(vec));
    }

    ListNode* merged = mergeKLists(lists);
    printList(merged);

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

  // Mock API call for demo purposes
  const handleSubmitCode = async (): Promise<AnalysisResult> => {
    setIsSubmitting(true);
    setShowResults(false);

    try {
      // Simulate API delay
      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Mock analysis - in real implementation, this would call your backend API
      const mockResult: AnalysisResult = {
        isAiGenerated: Math.random() > 0.5,
        confidence: Math.random() * 0.4 + 0.6, // Random confidence between 0.6 and 1.0
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
      {/* Header */}
      <div className='border-b bg-background/80 backdrop-blur-sm flex-shrink-0 z-10'>
        <div className='container mx-auto p-4'>
          <div className='flex items-center justify-between'>
            <div>
              <h1 className='text-2xl font-bold'>AI Code Detection System</h1>
              <p className='text-sm text-muted-foreground mt-1'>
                Phát hiện mã nguồn được tạo bởi AI trong bài tập lập trình của
                sinh viên
              </p>
            </div>
            <ThemeToggle />
          </div>
        </div>
      </div>

      {/* Main Content - Responsive 3 Columns with Animation */}
      <div className='flex-1 overflow-hidden'>
        <div className='container mx-auto p-4 h-full'>
          <div
            className={`grid gap-4 md:gap-6 h-full transition-all duration-500 ease-in-out ${
              showResults
                ? "grid-cols-1 lg:grid-cols-12"
                : "grid-cols-1 lg:grid-cols-8"
            }`}
          >
            {/* Column 1: User Guide */}
            <div
              className={`order-2 lg:order-1 transition-all duration-500 ease-in-out ${
                showResults ? "lg:col-span-3" : "lg:col-span-3"
              }`}
            >
              <UserGuide />
            </div>

            {/* Column 2: Code Editor */}
            <div
              className={`order-1 lg:order-2 transition-all duration-500 ease-in-out ${
                showResults ? "lg:col-span-5" : "lg:col-span-5"
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

            {/* Column 3: Analysis Results - Only visible when showResults is true */}
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
