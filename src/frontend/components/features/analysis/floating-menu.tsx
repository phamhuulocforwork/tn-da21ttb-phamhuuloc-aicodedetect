"use client";

import dynamic from "next/dynamic";
import Link from "next/link";

import { Github } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

import { ThemeToggle } from "../../shared";
import UsageDrawer from "./usage-drawer";

const Menu = () => {
  return (
    <div className='pointer-events-none fixed inset-x-0 bottom-0 z-30 flex overflow-hidden px-2 pb-1 duration-300 animate-in slide-in-from-bottom-12 lg:justify-center lg:p-4 lg:pb-4'>
      <div className='flex w-full flex-col items-center gap-2'>
        <div className='pointer-events-auto relative mx-auto flex flex-shrink-1 items-center gap-2 rounded-md border justify-center p-2 shadow-md backdrop-blur-sm scrollbar-thin max-lg:overflow-x-auto max-sm:w-full'>
          <ThemeToggle className='cursor-pointer' />

          <Separator orientation='vertical' />

          <UsageDrawer />

          <Separator orientation='vertical' />

          <Button variant='outline' size='icon' className='cursor-pointer'>
            <Link
              target='_blank'
              href='https://github.com/phamhuulocforwork/tn-da21ttb-phamhuuloc-aicodedetect'
            >
              <Github />
            </Link>
          </Button>
        </div>
      </div>
    </div>
  );
};

export const FloatingMenu = dynamic(() => Promise.resolve(Menu), {
  ssr: false,
});
