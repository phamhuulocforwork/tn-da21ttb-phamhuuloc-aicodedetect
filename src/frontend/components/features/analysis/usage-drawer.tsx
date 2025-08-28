"use client";

import * as React from "react";

import Image from "next/image";

import { Check, ChevronLeft, ChevronRight, FileSearch, X } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer";
import { Progress } from "@/components/ui/progress";

interface TutorialStep {
  title: string;
  description: React.ReactNode;
  image?: string;
}

const tutorialSteps: TutorialStep[] = [
  {
    title: "Bước 1. ",
    description: <div className='indent-4'></div>,
    image: "/placeholder.svg",
  },
  {
    title: "Bước 2. ",
    description: <div className='indent-4'></div>,
    image: "/placeholder.svg",
  },
];

export default function UsageDrawer() {
  const [open, setOpen] = React.useState(false);
  const [currentStep, setCurrentStep] = React.useState(0);

  const totalSteps = tutorialSteps.length;
  const progress = ((currentStep + 1) / totalSteps) * 100;

  const handleNext = () => {
    if (currentStep < totalSteps - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      setOpen(false);
      // Reset to first step when closing after completion
      setTimeout(() => setCurrentStep(0), 300);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleClose = () => {
    setOpen(false);
    // Reset to first step when manually closing
    setTimeout(() => setCurrentStep(0), 300);
  };
  return (
    <Drawer open={open} onOpenChange={setOpen}>
      <DrawerTrigger asChild>
        <Button variant='outline' className='cursor-pointer'>
          <FileSearch /> Xem hướng dẫn
        </Button>
      </DrawerTrigger>
      <DrawerContent className='max-h-[90vh]'>
        <div className='mx-auto w-full max-w-xl'>
          <DrawerHeader>
            <div className='flex items-center justify-between'>
              <DrawerTitle className='text-xl font-bold'>
                {tutorialSteps[currentStep].title}
              </DrawerTitle>
              <DrawerClose asChild>
                <Button
                  variant='ghost'
                  size='icon'
                  className='h-8 w-8 rounded-full'
                  onClick={handleClose}
                >
                  <X className='h-4 w-4' />
                  <span className='sr-only'>Đóng</span>
                </Button>
              </DrawerClose>
            </div>
            <div className='flex items-center justify-center gap-2'>
              <span className='text-xs text-muted-foreground text-nowrap'>
                Bước {currentStep + 1} / {totalSteps}
              </span>
              <Progress value={progress} />
            </div>
          </DrawerHeader>

          <div className='p-4 pb-0'>
            <div className='mb-4 text-sm text-foreground'>
              {tutorialSteps[currentStep].description}
            </div>
            {tutorialSteps[currentStep].image && (
              <div className='overflow-hidden rounded-lg border shadow-md mb-4'>
                <Image
                  src={tutorialSteps[currentStep].image}
                  alt={`Minh họa cho ${tutorialSteps[currentStep].title}`}
                  width={600}
                  height={400}
                  className='w-full object-cover max-h-[300px]'
                />
              </div>
            )}
          </div>

          <DrawerFooter className='flex-row justify-between space-x-2 pt-2'>
            <Button
              onClick={handlePrevious}
              disabled={currentStep === 0}
              className='flex-1'
            >
              <ChevronLeft className='mr-2 h-4 w-4' />
              Trước
            </Button>
            <Button onClick={handleNext} size='sm' className='flex-1'>
              {currentStep === totalSteps - 1 ? (
                <>
                  Hoàn thành
                  <Check className='ml-2 h-4 w-4' />
                </>
              ) : (
                <>
                  Tiếp
                  <ChevronRight className='ml-2 h-4 w-4' />
                </>
              )}
            </Button>
          </DrawerFooter>
        </div>
      </DrawerContent>
    </Drawer>
  );
}
