import React from "react";

interface SectionHeaderProps {
  title: string;
  children?: React.ReactNode;
  className?: string;
}

export function SectionHeader({
  title,
  children,
  className = "",
}: SectionHeaderProps) {
  return (
    <div className={`flex items-center justify-between ${className}`}>
      <h3 className='text-lg font-semibold'>{title}</h3>
      {children}
    </div>
  );
}

export default SectionHeader;
