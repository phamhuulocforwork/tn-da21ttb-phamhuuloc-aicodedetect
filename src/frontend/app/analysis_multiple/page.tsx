"use client";

import * as React from "react";

import {
  ArrowLeft,
  ArrowRight,
  File,
  MousePointerClick,
  Upload,
  X,
} from "lucide-react";

import { FloatingMenu } from "@/components/features/analysis_multiple/floating-menu";
import { AnalysisLayout } from "@/components/layout/analysis-layout";
import { Button } from "@/components/ui/button";
import { defineStepper } from "@/components/ui/stepper";

import { useIsMobile } from "@/hooks/use-mobile";

const { Stepper } = defineStepper(
  {
    id: "1",
    title: "Bộ câu hỏi",
    description: "Tải lên bộ câu hỏi",
    icon: <Upload />,
  },
  {
    id: "2",
    title: "Tùy chọn",
    description: "Tùy chọn thêm",
    icon: <MousePointerClick />,
  },
  {
    id: "3",
    title: "Tạo đề, đáp án",
    description: "Tạo đề, đáp án",
    icon: <File />,
    isLast: true,
  },
);

export default function AnalysisMultiplePage() {
  const isMobile = useIsMobile();

  return (
    <AnalysisLayout>
      <div id='analysis' className='container mx-auto p-4 space-y-6'>
        <Stepper.Provider
          className='space-y-4'
          variant={isMobile ? "vertical" : "horizontal"}
          labelOrientation={isMobile ? "horizontal" : "vertical"}
        >
          {({ methods }) => (
            <>
              <Stepper.Navigation>
                {methods.all.map((step) => (
                  <Stepper.Step
                    of={step.id}
                    key={step.id}
                    icon={step.icon}
                    onClick={() => methods.goTo(step.id)}
                  >
                    <Stepper.Title>{step.title}</Stepper.Title>
                    {isMobile &&
                      methods.when(step.id, () => (
                        <Stepper.Panel>
                          {step.id === "1" && <div>1</div>}
                          {step.id === "2" && <div>2</div>}
                          {step.id === "3" && <div>3</div>}
                        </Stepper.Panel>
                      ))}
                  </Stepper.Step>
                ))}
              </Stepper.Navigation>
              {!isMobile &&
                methods.switch({
                  "1": (step) => <div>1</div>,
                  "2": (step) => <div>2</div>,
                  "3": (step) => <div>3</div>,
                })}
              <Stepper.Controls>
                {!methods.isLast && (
                  <Button
                    variant='secondary'
                    onClick={methods.prev}
                    disabled={methods.isFirst}
                  >
                    <ArrowLeft />
                    Quay lại
                  </Button>
                )}
                <Button onClick={methods.isLast ? methods.reset : methods.next}>
                  {methods.isLast ? (
                    <>
                      <X />
                      Hủy bỏ
                    </>
                  ) : (
                    <>
                      Tiếp tục
                      <ArrowRight />
                    </>
                  )}
                </Button>
              </Stepper.Controls>
            </>
          )}
        </Stepper.Provider>

        <FloatingMenu />
      </div>
    </AnalysisLayout>
  );
}
