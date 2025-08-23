"use client";

import { type ButtonHTMLAttributes } from "react";
import { useEffect, useState } from "react";

import { MoonStar, Sun } from "lucide-react";
import { useTheme } from "next-themes";

import { Button } from "@/components/ui/button";

export interface ThemeToggleProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  showLabel?: boolean;
}

export function ThemeToggle({
  showLabel = false,
  ...props
}: ThemeToggleProps): React.ReactElement {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  if (!mounted) {
    return (
      <Button variant='outline' size='icon' {...props}>
        <span className='sr-only'>Đổi giao diện</span>
      </Button>
    );
  }

  return (
    <Button variant='outline' size='icon' onClick={toggleTheme} {...props}>
      {theme === "dark" ? (
        <Sun className='size-5' />
      ) : (
        <MoonStar className='size-5' />
      )}
      <span className='sr-only'>Đổi giao diện</span>
      {showLabel && (
        <span className='ml-2 hidden sm:inline'>
          {theme === "dark" ? "Sáng" : "Tối"}
        </span>
      )}
    </Button>
  );
}

export default ThemeToggle;
