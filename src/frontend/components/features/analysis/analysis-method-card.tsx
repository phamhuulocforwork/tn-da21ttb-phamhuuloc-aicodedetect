import React from "react";

import { Clock } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { RadioGroupItem } from "@/components/ui/radio-group";

import { AnalysisMethodConfig, AnalysisMode } from "./types";

interface AnalysisMethodCardProps {
  mode: AnalysisMode;
  config: AnalysisMethodConfig;
  isSelected: boolean;
  disabled?: boolean;
}

export function AnalysisMethodCard({
  mode,
  config,
  isSelected,
  disabled = false,
}: AnalysisMethodCardProps) {
  const Icon = config.icon;

  return (
    <div className='relative'>
      <RadioGroupItem value={mode} id={mode} className='peer sr-only' />
      <Label
        htmlFor={mode}
        className={`
          block cursor-pointer
          ${disabled ? "cursor-not-allowed opacity-50" : ""}
        `}
      >
        <Card
          className={`
            transition-all duration-200 hover:shadow-md border-2
            ${
              isSelected
                ? "border-primary ring-2 ring-primary/20"
                : "border-border hover:border-primary/50"
            }
            ${disabled ? "hover:shadow-none hover:border-border" : ""}
          `}
        >
          <CardHeader className='pb-3'>
            <div className='flex items-start justify-between'>
              <div className='flex items-center gap-3'>
                <div
                  className={`
                    p-2 rounded-md 
                    ${
                      isSelected
                        ? "bg-primary text-primary-foreground"
                        : "bg-muted"
                    }
                  `}
                >
                  <Icon className='h-4 w-4' />
                </div>
                <div>
                  <CardTitle className='text-base'>{config.title}</CardTitle>
                  {config.badge && (
                    <Badge variant='secondary' className='mt-1 text-xs'>
                      {config.badge}
                    </Badge>
                  )}
                </div>
              </div>

              <div className='flex items-center gap-1 text-muted-foreground'>
                <Clock className='h-3 w-3' />
                <span className='text-xs'>{config.timeEstimate}</span>
              </div>
            </div>

            <CardDescription className='text-sm'>
              {config.description}
            </CardDescription>
          </CardHeader>

          <CardContent className='pt-0'>
            <div className='space-y-3'>
              <div>
                <p className='text-xs font-medium text-muted-foreground mb-2'>
                  Gồm các phương pháp:
                </p>
                <div className='flex flex-wrap gap-1'>
                  {config.features.map((feature, index) => (
                    <Badge
                      key={index}
                      variant='outline'
                      className='text-xs py-0.5 px-2'
                    >
                      {feature}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </Label>
    </div>
  );
}

export default AnalysisMethodCard;
