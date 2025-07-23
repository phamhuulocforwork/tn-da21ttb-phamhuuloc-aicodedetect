import React from "react";

import ThemeToggle from "@/components/theme-toggle";

export default function header() {
  return (
    <div className='border-b bg-background/80 backdrop-blur-sm flex-shrink-0 z-10 h-header-height'>
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
  );
}
