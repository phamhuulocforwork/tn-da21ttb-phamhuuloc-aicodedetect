"use client";

import { motion } from "framer-motion";
import {
  AlertTriangle,
  BookOpen,
  CheckCircle,
  Code2,
  Cpu,
  FileText,
  Hash,
  Info,
  MessageSquare,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function UserGuide() {
  const languages = [
    { name: "C", description: "Phù hợp cho các bài tập cơ bản", icon: "🔧" },
    {
      name: "C++",
      description: "Hỗ trợ object-oriented programming",
      icon: "⚡",
    },
    { name: "Java", description: "Cho các bài tập nâng cao", icon: "☕" },
    { name: "Python", description: "Scripting và data processing", icon: "🐍" },
    { name: "JavaScript", description: "Web development", icon: "🌐" },
    { name: "TypeScript", description: "Type-safe JavaScript", icon: "🔷" },
  ];

  const analysisFeatures = [
    {
      icon: Cpu,
      label: "Complexity",
      description: "Đo độ phức tạp thuật toán và cấu trúc code",
      color: "text-blue-500",
    },
    {
      icon: Hash,
      label: "Redundancy",
      description: "Phần trăm code lặp lại và không cần thiết",
      color: "text-purple-500",
    },
    {
      icon: FileText,
      label: "Naming Score",
      description: "Điểm đánh giá cách đặt tên biến và hàm",
      color: "text-orange-500",
    },
    {
      icon: MessageSquare,
      label: "Comments",
      description: "Tỷ lệ và chất lượng comment trong code",
      color: "text-green-500",
    },
  ];

  const confidenceLevels = [
    {
      icon: CheckCircle,
      level: "Xanh lá (0-60%)",
      description: "Có thể là code viết bởi sinh viên",
      color: "text-green-500",
    },
    {
      icon: AlertTriangle,
      level: "Vàng (60-80%)",
      description: "Nghi ngờ có sự hỗ trợ của AI",
      color: "text-yellow-500",
    },
    {
      icon: AlertTriangle,
      level: "Đỏ (80-100%)",
      description: "Rất có thể được tạo bởi AI",
      color: "text-red-500",
    },
  ];

  return (
    <div className='space-y-6 h-full overflow-y-auto'>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className='sticky top-0 bg-background/80 backdrop-blur-sm pb-4 border-b'
      >
        <div className='flex items-center gap-2 mb-2'>
          <BookOpen className='w-6 h-6 text-primary' />
          <h2 className='text-xl font-bold'>Hướng dẫn sử dụng</h2>
        </div>
        <p className='text-sm text-muted-foreground'>
          Tìm hiểu cách sử dụng hệ thống phát hiện AI-generated code
        </p>
      </motion.div>

      {/* Supported Languages */}
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Card>
          <CardHeader className='pb-3'>
            <CardTitle className='text-lg flex items-center gap-2'>
              <Code2 className='w-5 h-5' />
              Ngôn ngữ được hỗ trợ
            </CardTitle>
          </CardHeader>
          <CardContent className='space-y-3'>
            {languages.map((lang, index) => (
              <motion.div
                key={lang.name}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 + index * 0.1 }}
                className='flex items-start gap-3 p-2 rounded-lg hover:bg-muted/50 transition-colors'
              >
                <span className='text-lg'>{lang.icon}</span>
                <div className='flex-1'>
                  <div className='flex items-center gap-2'>
                    <Badge variant='outline' className='text-xs'>
                      {lang.name}
                    </Badge>
                  </div>
                  <p className='text-xs text-muted-foreground mt-1'>
                    {lang.description}
                  </p>
                </div>
              </motion.div>
            ))}
          </CardContent>
        </Card>
      </motion.div>

      {/* Analysis Features */}
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <Card>
          <CardHeader className='pb-3'>
            <CardTitle className='text-lg flex items-center gap-2'>
              <Info className='w-5 h-5' />
              Cách thức phân tích
            </CardTitle>
          </CardHeader>
          <CardContent className='space-y-4'>
            {analysisFeatures.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={feature.label}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 + index * 0.1 }}
                  className='flex items-start gap-3 p-3 rounded-lg bg-muted/30'
                >
                  <Icon className={`w-5 h-5 mt-0.5 ${feature.color}`} />
                  <div className='flex-1'>
                    <h4 className='font-medium text-sm'>{feature.label}</h4>
                    <p className='text-xs text-muted-foreground leading-relaxed'>
                      {feature.description}
                    </p>
                  </div>
                </motion.div>
              );
            })}
          </CardContent>
        </Card>
      </motion.div>

      {/* Confidence Levels */}
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <Card>
          <CardHeader className='pb-3'>
            <CardTitle className='text-lg'>Kết quả phân tích</CardTitle>
          </CardHeader>
          <CardContent className='space-y-3'>
            {confidenceLevels.map((level, index) => {
              const Icon = level.icon;
              return (
                <motion.div
                  key={level.level}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.4 + index * 0.1 }}
                  className='flex items-start gap-3 p-3 rounded-lg border'
                >
                  <Icon className={`w-4 h-4 mt-0.5 ${level.color}`} />
                  <div className='flex-1'>
                    <h4 className='font-medium text-sm'>{level.level}</h4>
                    <p className='text-xs text-muted-foreground'>
                      {level.description}
                    </p>
                  </div>
                </motion.div>
              );
            })}
          </CardContent>
        </Card>
      </motion.div>

      {/* Usage Tips */}
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
      >
        <Card>
          <CardHeader className='pb-3'>
            <CardTitle className='text-lg'>Lời khuyên</CardTitle>
          </CardHeader>
          <CardContent className='space-y-3'>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className='space-y-2'
            >
              <div className='flex items-start gap-2'>
                <span className='text-primary text-sm mt-1'>💡</span>
                <p className='text-xs text-muted-foreground leading-relaxed'>
                  Paste toàn bộ code vào editor để có kết quả phân tích chính
                  xác nhất
                </p>
              </div>
              <div className='flex items-start gap-2'>
                <span className='text-primary text-sm mt-1'>⚡</span>
                <p className='text-xs text-muted-foreground leading-relaxed'>
                  Hệ thống tự động detect ngôn ngữ, nhưng bạn có thể chọn thủ
                  công
                </p>
              </div>
              <div className='flex items-start gap-2'>
                <span className='text-primary text-sm mt-1'>🎯</span>
                <p className='text-xs text-muted-foreground leading-relaxed'>
                  Kết quả chỉ mang tính chất tham khảo, cần kết hợp với đánh giá
                  của giảng viên
                </p>
              </div>
            </motion.div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
