"use client";

import { AnimatePresence, motion } from "framer-motion";
import {
  AlertTriangle,
  CheckCircle,
  Code,
  Hash,
  MessageSquare,
  TrendingUp,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export interface AnalysisResult {
  isAiGenerated: boolean;
  confidence: number;
  features: {
    complexity: number;
    redundancy: number;
    namingPatterns: number;
    comments: number;
  };
  reasons: string[];
}

interface AnalysisResultsProps {
  result: AnalysisResult | null;
  isVisible: boolean;
}

export function AnalysisResults({ result, isVisible }: AnalysisResultsProps) {
  const getConfidenceBadgeVariant = (confidence: number) => {
    if (confidence >= 0.8) return "destructive";
    if (confidence >= 0.6) return "secondary";
    return "default";
  };

  return (
    <div className='h-full'>
      <AnimatePresence mode='wait'>
        {isVisible && result ? (
          <motion.div
            initial={{ opacity: 0, x: 50, scale: 0.95 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, x: 50, scale: 0.95 }}
            transition={{
              duration: 0.4,
              ease: [0.4, 0.0, 0.2, 1],
              staggerChildren: 0.1,
            }}
            className='space-y-4'
          >
            {/* Main Result Card */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
            >
              <Card className='border-2'>
                <CardHeader className='pb-3'>
                  <CardTitle className='text-lg flex items-center gap-2'>
                    <motion.div
                      initial={{ scale: 0, rotate: -180 }}
                      animate={{ scale: 1, rotate: 0 }}
                      transition={{
                        delay: 0.2,
                        type: "spring",
                        stiffness: 200,
                      }}
                    >
                      {result.isAiGenerated ? (
                        <AlertTriangle className='w-5 h-5 text-red-500' />
                      ) : (
                        <CheckCircle className='w-5 h-5 text-green-500' />
                      )}
                    </motion.div>
                    Kết quả phân tích
                  </CardTitle>
                </CardHeader>
                <CardContent className='space-y-4'>
                  <motion.div
                    className='flex flex-col gap-3'
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.3 }}
                  >
                    <div className='flex items-center gap-2'>
                      <span className='font-medium text-sm'>Phát hiện AI:</span>
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.4, type: "spring" }}
                      >
                        <Badge
                          variant={
                            result.isAiGenerated ? "destructive" : "default"
                          }
                        >
                          {result.isAiGenerated
                            ? "AI Generated"
                            : "Human Written"}
                        </Badge>
                      </motion.div>
                    </div>

                    <div className='flex items-center gap-2'>
                      <span className='font-medium text-sm'>Độ tin cậy:</span>
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.5, type: "spring" }}
                      >
                        <Badge
                          variant={getConfidenceBadgeVariant(result.confidence)}
                        >
                          {(result.confidence * 100).toFixed(1)}%
                        </Badge>
                      </motion.div>
                    </div>
                  </motion.div>
                </CardContent>
              </Card>
            </motion.div>

            {/* Features Analysis */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <Card>
                <CardHeader className='pb-3'>
                  <CardTitle className='text-base flex items-center gap-2'>
                    <TrendingUp className='w-4 h-4' />
                    Phân tích đặc trưng
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className='grid grid-cols-2 gap-4'>
                    <motion.div
                      className='text-center p-3 rounded-lg bg-muted/50'
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.4 }}
                    >
                      <div className='flex items-center justify-center gap-1 mb-1'>
                        <Code className='w-3 h-3 text-muted-foreground' />
                      </div>
                      <div className='text-lg font-bold'>
                        {result.features.complexity.toFixed(1)}
                      </div>
                      <div className='text-xs text-muted-foreground'>
                        Complexity
                      </div>
                    </motion.div>

                    <motion.div
                      className='text-center p-3 rounded-lg bg-muted/50'
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.5 }}
                    >
                      <div className='flex items-center justify-center gap-1 mb-1'>
                        <Hash className='w-3 h-3 text-muted-foreground' />
                      </div>
                      <div className='text-lg font-bold'>
                        {(result.features.redundancy * 100).toFixed(1)}%
                      </div>
                      <div className='text-xs text-muted-foreground'>
                        Redundancy
                      </div>
                    </motion.div>

                    <motion.div
                      className='text-center p-3 rounded-lg bg-muted/50'
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.6 }}
                    >
                      <div className='text-lg font-bold'>
                        {result.features.namingPatterns.toFixed(1)}
                      </div>
                      <div className='text-xs text-muted-foreground'>
                        Naming Score
                      </div>
                    </motion.div>

                    <motion.div
                      className='text-center p-3 rounded-lg bg-muted/50'
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.7 }}
                    >
                      <div className='flex items-center justify-center gap-1 mb-1'>
                        <MessageSquare className='w-3 h-3 text-muted-foreground' />
                      </div>
                      <div className='text-lg font-bold'>
                        {(result.features.comments * 100).toFixed(1)}%
                      </div>
                      <div className='text-xs text-muted-foreground'>
                        Comments
                      </div>
                    </motion.div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            {/* Detailed Reasons */}
            {result.reasons.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
              >
                <Card>
                  <CardHeader className='pb-3'>
                    <CardTitle className='text-base'>
                      Chi tiết phân tích
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className='space-y-2'>
                      {result.reasons.map((reason, index) => (
                        <motion.li
                          key={index}
                          className='text-sm text-muted-foreground flex items-start gap-2'
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: 0.4 + index * 0.1 }}
                        >
                          <motion.span
                            className='text-primary mt-1 flex-shrink-0'
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            transition={{
                              delay: 0.5 + index * 0.1,
                              type: "spring",
                            }}
                          >
                            •
                          </motion.span>
                          <span className='leading-relaxed'>{reason}</span>
                        </motion.li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className='h-full flex items-center justify-center'
          >
            <div className='text-center text-muted-foreground'>
              <motion.div
                animate={{
                  scale: [1, 1.1, 1],
                  opacity: [0.5, 1, 0.5],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
              >
                <TrendingUp className='w-12 h-12 mx-auto mb-4' />
              </motion.div>
              <p className='text-sm'>
                Nhập code và nhấn &quot;Analyze Code&quot; để xem kết quả phân
                tích
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
