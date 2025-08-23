"use client";

import { useEffect, useRef, useState } from "react";

import { NeatConfig, NeatGradient } from "@firecms/neat";

const DEFAULT_CONFIG: NeatConfig = {
  colors: [
    {
      color: "#D2F4FB",
      enabled: true,
    },
    {
      color: "#AAE8F7",
      enabled: true,
    },
    {
      color: "#2FB9E1",
      enabled: true,
    },
    {
      color: "#97C8EC",
      enabled: true,
    },
    {
      color: "#a2d2ff",
      enabled: false,
    },
  ],
  speed: 2.5,
  horizontalPressure: 3,
  verticalPressure: 4,
  waveFrequencyX: 2,
  waveFrequencyY: 3,
  waveAmplitude: 5,
  shadows: 1,
  highlights: 5,
  colorBrightness: 1,
  colorSaturation: 7,
  wireframe: false,
  colorBlending: 8,
  backgroundColor: "#003FFF",
  backgroundAlpha: 1,
  grainScale: 3,
  grainIntensity: 0.3,
  grainSpeed: 1,
  resolution: 0.5,
};

interface GradientBackgroundProps {
  config?: Partial<NeatConfig>;
  speed?: number;
  className?: string;
  children?: React.ReactNode;
}

export function GradientBackground({
  config = {},
  speed = 4,
  className = "",
  children,
}: GradientBackgroundProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isCanvasSupported, setIsCanvasSupported] = useState<boolean>(false);

  useEffect(() => {
    const checkCanvasSupport = () => {
      const canvas = document.createElement("canvas");
      setIsCanvasSupported(!!(canvas.getContext && canvas.getContext("2d")));
    };

    checkCanvasSupport();
  }, []);

  useEffect(() => {
    if (!isCanvasSupported) return;

    let gradient: NeatGradient | null = null;

    if (canvasRef.current) {
      gradient = new NeatGradient({
        ref: canvasRef.current,
        ...DEFAULT_CONFIG,
        ...config,
      });
      gradient.speed = speed;
    }

    return () => {
      gradient?.destroy();
    };
  }, [isCanvasSupported, config, speed]);

  return (
    <div
      className={`relative flex h-full min-h-screen w-full items-center justify-center bg-transparent ${className}`}
    >
      {isCanvasSupported && (
        <canvas
          ref={canvasRef}
          className='absolute inset-0 -z-10 hidden h-full w-full lg:block'
        />
      )}
      {children}
    </div>
  );
}

export default GradientBackground;
