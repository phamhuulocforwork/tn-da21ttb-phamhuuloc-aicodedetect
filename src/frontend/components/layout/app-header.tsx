import React from "react";

interface AppHeaderProps {
  title: string;
  subtitle?: string;
  className?: string;
}

export function AppHeader({ title, subtitle, className = "" }: AppHeaderProps) {
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
    </header>
  );
}

export default AppHeader;
