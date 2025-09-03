"use client";

import { usePathname, useRouter } from "next/navigation";

import { ArrowLeftRight } from "lucide-react";

import { Button } from "@/components/ui/button";

export function ModeSwitcher() {
  const pathname = usePathname();
  const router = useRouter();

  const isMultipleMode = pathname === "/analysis_multiple";
  const targetPath = isMultipleMode ? "/analysis" : "/analysis_multiple";
  const buttonText = isMultipleMode
    ? "Chuyển sang Phân tích đơn"
    : "Chuyển sang Phân tích nhiều";

  const handleSwitch = () => {
    router.push(targetPath);
  };

  return (
    <Button
      variant='outline'
      size='sm'
      onClick={handleSwitch}
      className='flex items-center gap-2'
    >
      <ArrowLeftRight className='h-4 w-4' />
      {buttonText}
    </Button>
  );
}

export default ModeSwitcher;
