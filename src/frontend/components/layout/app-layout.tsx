import React from "react";

import { AppHeader } from "./app-header";

interface AppLayoutProps {
  children: React.ReactNode;
  title: string;
  subtitle?: string;
  headerClassName?: string;
  className?: string;
}

export function AppLayout({
  children,
  title,
  subtitle,
  headerClassName,
  className = "",
}: AppLayoutProps) {
  return (
    <div className={`min-h-screen bg-background ${className}`}>
      <AppHeader
        title={title}
        subtitle={subtitle}
        className={headerClassName}
      />
      <main className='flex-1'>{children}</main>
    </div>
  );
}

export default AppLayout;
