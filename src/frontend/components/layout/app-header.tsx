"use client";

import React from "react";

import { usePathname } from "next/navigation";

import { ModeSwitcher } from "@/components/shared/mode-switcher";

interface AppHeaderProps {
  title: string;
  subtitle?: string;
  className?: string;
}

export function AppHeader({ title, subtitle, className = "" }: AppHeaderProps) {
  const pathname = usePathname();
  const showModeSwitcher =
    pathname === "/analysis" || pathname === "/analysis_multiple";

  return (
    <header
      className={`border-b h-[var(--header-height)] flex items-center justify-between px-4 container mx-auto ${className}`}
    >
      <div className='flex flex-col'>
        <h1 className='text-xl md:text-2xl font-bold leading-none'>{title}</h1>
        {subtitle && (
          <p className='text-sm text-muted-foreground mt-1'>{subtitle}</p>
        )}
      </div>
      {showModeSwitcher && (
        <div className='flex items-center'>
          <ModeSwitcher />
        </div>
      )}
    </header>
  );
}

export default AppHeader;
