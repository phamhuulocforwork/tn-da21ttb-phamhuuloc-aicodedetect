import React from "react";

import ThemeToggle from "@/components/theme-toggle";

export default function header() {
  return (
    <div className='border-b h-[var(--header-height)] flex items-center justify-between px-4 container mx-auto'>
      <div className='flex flex-col'>
        <h1 className='text-xl md:text-2xl font-bold leading-none'>
          HỆ THỐNG PHÂN TÍCH MÃ NGUỒN
        </h1>
        <p className='text-sm text-muted-foreground mt-1'>
          Phát hiện AI-generated code trong bài tập lập trình của sinh viên
        </p>
      </div>
      <ThemeToggle />
    </div>
  );
}
