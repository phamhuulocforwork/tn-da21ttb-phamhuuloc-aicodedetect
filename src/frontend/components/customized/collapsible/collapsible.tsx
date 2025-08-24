"use client";

import { ReactNode } from "react";

import { ChevronDown, LucideIcon } from "lucide-react";

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";

export const CollapsibleFilter = ({
  title,
  icon: Icon,
  children,
  defaultOpen = false,
}: {
  title: string;
  icon?: LucideIcon;
  children: ReactNode;
  defaultOpen?: boolean;
}) => (
  <Collapsible defaultOpen={defaultOpen}>
    <CollapsibleTrigger className='group flex w-full items-center justify-between py-3 cursor-pointer'>
      <h3 className='flex items-center gap-2 text-sm font-semibold'>
        {!!Icon && <Icon className='h-5 w-5' />} {title}
      </h3>
      <ChevronDown className='h-4 w-4 group-data-[state=open]:rotate-180 transition-transform text-muted-foreground' />
    </CollapsibleTrigger>
    <CollapsibleContent className='pt-1 pb-3'>{children}</CollapsibleContent>
  </Collapsible>
);
