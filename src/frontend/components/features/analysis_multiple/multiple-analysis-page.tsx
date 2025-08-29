"use client";

import * as React from "react";

import { useRouter } from "next/navigation";

import {
  Activity,
  AlertCircle,
  CheckCircle,
  ExternalLink,
  FileText,
  Link,
  RefreshCw,
  Upload,
  X,
} from "lucide-react";

import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Scroller } from "@/components/ui/scroller";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

import { apiClient } from "@/lib/api-client";
import type {
  BatchAnalysisResponse,
  FileAnalysisResult,
} from "@/lib/api-types";

export function MultipleAnalysisPage() {
  const router = useRouter();

  const [sourceType, setSourceType] = React.useState<"zip" | "google_drive">(
    "zip",
  );
  const [file, setFile] = React.useState<File | null>(null);
  const [googleDriveUrl, setGoogleDriveUrl] = React.useState("");

  const [batchData, setBatchData] =
    React.useState<BatchAnalysisResponse | null>(null);
  const [isUploading, setIsUploading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [pollingInterval, setPollingInterval] =
    React.useState<NodeJS.Timeout | null>(null);

  React.useEffect(() => {
    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval);
      }
    };
  }, [pollingInterval]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      if (
        !selectedFile.name.endsWith(".zip") &&
        !selectedFile.name.endsWith(".rar")
      ) {
        setError("Chỉ hỗ trợ file ZIP hoặc RAR");
        setFile(null);
        return;
      }

      const maxSize = 50 * 1024 * 1024; // 50MB
      if (selectedFile.size > maxSize) {
        setError("File không được vượt quá 50MB");
        setFile(null);
        return;
      }

      setFile(selectedFile);
      setError(null);
    }
  };

  const handleGoogleDriveUrlChange = (value: string) => {
    setGoogleDriveUrl(value);
    setError(null);

    if (value && !value.includes("drive.google.com")) {
      setError("URL không hợp lệ. Vui lòng nhập URL Google Drive hợp lệ.");
    }
  };

  const startPolling = (batchId: string) => {
    const interval = setInterval(async () => {
      try {
        const data = await apiClient.getBatchStatus(batchId);
        setBatchData(data);

        if (data.status !== "processing") {
          clearInterval(interval);
          setPollingInterval(null);
        }
      } catch (err) {
        console.error("Lỗi khi thăm dò:", err);
        clearInterval(interval);
        setPollingInterval(null);
      }
    }, 3000);

    setPollingInterval(interval);
  };

  const handleStartAnalysis = async () => {
    setError(null);
    setIsUploading(true);

    try {
      let data: BatchAnalysisResponse;

      if (sourceType === "zip" && file) {
        data = await apiClient.uploadBatchZip(file);
      } else if (sourceType === "google_drive" && googleDriveUrl) {
        data = await apiClient.analyzeBatchGoogleDrive({
          source_type: "google_drive",
          google_drive_url: googleDriveUrl,
        });
      } else {
        throw new Error("Tùy chọn tải lên không hợp lệ");
      }

      setBatchData(data);

      if (data.status === "processing") {
        startPolling(data.batch_id);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Đã xảy ra lỗi");
    } finally {
      setIsUploading(false);
    }
  };

  const handleRefreshStatus = async () => {
    if (!batchData) return;

    try {
      const data = await apiClient.getBatchStatus(batchData.batch_id);
      setBatchData(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Không thể làm mới trạng thái",
      );
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 B";
    const k = 1024;
    const sizes = ["B", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  const getSimilarityBadge = (
    aiSimilarity: number,
    humanSimilarity: number,
  ) => {
    if (aiSimilarity > humanSimilarity + 10)
      return <Badge variant='destructive'>Giống AI</Badge>;
    if (humanSimilarity > aiSimilarity + 10)
      return <Badge className='bg-green-500'>Giống Con Người</Badge>;
    return <Badge variant='secondary'>Hỗn Hợp</Badge>;
  };

  const handleViewDetails = (result: FileAnalysisResult) => {
    if (result.code_content) {
      const encodedCode = encodeURIComponent(result.code_content);
      router.push(`http://localhost:3000/analysis?code=${encodedCode}`);
    } else if (result.analysis_id) {
      router.push(
        `http://localhost:3000/analysis?code=${encodeURIComponent(result.analysis_id)}`,
      );
    }
  };

  const successfulResults =
    batchData?.results.filter((r) => r.status === "success") || [];

  return (
    <div className='container mx-auto p-6 space-y-6'>
      <div className='text-center'>
        <h1 className='text-3xl font-bold mb-2'>Phân Tích Nhiều Tệp</h1>
        <p className='text-muted-foreground'>
          Phân tích nhiều tệp mã cùng lúc để phát hiện AI
        </p>
      </div>

      {error && (
        <Alert variant='destructive'>
          <AlertCircle className='h-4 w-4' />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {!batchData && (
        <Card>
          <CardHeader>
            <CardTitle>Tải Lên Tệp</CardTitle>
            <CardDescription>
              Chọn nguồn của bạn và bắt đầu phân tích Lỗi
            </CardDescription>
          </CardHeader>
          <CardContent className='space-y-4'>
            <Tabs
              value={sourceType}
              onValueChange={(value) =>
                setSourceType(value as "zip" | "google_drive")
              }
            >
              <TabsList className='grid w-full grid-cols-2'>
                <TabsTrigger value='zip'>
                  <Upload className='h-4 w-4 mr-2' />
                  Tải Lên ZIP/RAR
                </TabsTrigger>
                <TabsTrigger value='google_drive'>
                  <Link className='h-4 w-4 mr-2' />
                  Liên Kết Google Drive
                </TabsTrigger>
              </TabsList>

              <TabsContent value='zip' className='space-y-4'>
                <div>
                  <Label htmlFor='file-upload'>Chọn Tệp ZIP/RAR</Label>
                  <Input
                    id='file-upload'
                    type='file'
                    accept='.zip,.rar'
                    onChange={handleFileChange}
                    className='cursor-pointer'
                  />
                  {file && (
                    <div className='mt-2 flex items-center gap-2'>
                      <Badge variant='secondary'>{file.name}</Badge>
                      <Badge variant='outline'>
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </Badge>
                    </div>
                  )}
                </div>
              </TabsContent>

              <TabsContent value='google_drive' className='space-y-4'>
                <div>
                  <Label htmlFor='drive-url'>URL Google Drive</Label>
                  <Input
                    id='drive-url'
                    value={googleDriveUrl}
                    onChange={(e) => handleGoogleDriveUrlChange(e.target.value)}
                    placeholder='https://drive.google.com/drive/folders/... hoặc https://drive.google.com/file/d/...'
                  />
                  <p className='text-sm text-muted-foreground mt-1'>
                    Dán một liên kết thư mục hoặc tệp Google Drive có thể chia
                    sẻ
                  </p>
                </div>
              </TabsContent>
            </Tabs>

            <Button
              onClick={handleStartAnalysis}
              disabled={
                isUploading ||
                (sourceType === "zip" && !file) ||
                (sourceType === "google_drive" && !googleDriveUrl)
              }
              className='w-full'
            >
              {isUploading ? (
                <>
                  <RefreshCw className='h-4 w-4 mr-2 animate-spin' />
                  Bắt Đầu Phân Tích...
                </>
              ) : (
                <>
                  Phân Tích
                  <Upload className='h-4 w-4 ml-2' />
                </>
              )}
            </Button>
          </CardContent>
        </Card>
      )}

      {batchData && (
        <div className='space-y-6'>
          <Card>
            <CardContent className='p-4'>
              <div className='flex justify-between items-center'>
                <div className='flex items-center gap-3'>
                  <Badge
                    variant={
                      batchData.status === "completed" ? "default" : "secondary"
                    }
                    className='flex items-center gap-1'
                  >
                    {batchData.status === "processing" && (
                      <RefreshCw className='h-3 w-3 animate-spin' />
                    )}
                    {batchData.status === "completed" && (
                      <CheckCircle className='h-3 w-3' />
                    )}
                    {batchData.status === "error" && <X className='h-3 w-3' />}
                    {batchData.status.charAt(0).toUpperCase() +
                      batchData.status.slice(1)}
                  </Badge>
                  <span className='text-sm text-muted-foreground'>
                    {batchData.processed_files}/{batchData.total_files} tệp
                  </span>
                </div>
                <div className='flex gap-2'>
                  <Button
                    variant='outline'
                    size='sm'
                    onClick={handleRefreshStatus}
                    disabled={batchData.status === "processing"}
                  >
                    <RefreshCw className='h-4 w-4 mr-1' />
                    Làm Mới
                  </Button>
                  <Button
                    variant='outline'
                    size='sm'
                    onClick={() => setBatchData(null)}
                  >
                    <X className='h-4 w-4 mr-1' />
                    Phân Tích Mới
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {successfulResults.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className='flex items-center gap-2'>
                  <FileText className='h-5 w-5' />
                  Kết Quả Phân Tích ({successfulResults.length} tệp)
                </CardTitle>
                <CardDescription>
                  Nhấp vào &quot;Xem Chi Tiết&quot; để phân tích từng tệp riêng
                  lẻ
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Scroller orientation='horizontal' className='w-full'>
                  <div className='flex gap-4 pb-4'>
                    {successfulResults.map((result) => (
                      <Card
                        key={result.analysis_id || result.filename}
                        className='flex-shrink-0 w-80 hover:shadow-md transition-shadow'
                      >
                        <CardContent className='p-4'>
                          <div className='space-y-3'>
                            <div className='flex items-start gap-2'>
                              <FileText className='h-4 w-4 text-muted-foreground flex-shrink-0 mt-0.5' />
                              <div className='flex-1 min-w-0'>
                                <div
                                  className='font-medium text-sm truncate'
                                  title={result.filename}
                                >
                                  {result.filename}
                                </div>
                                <div className='text-xs text-muted-foreground truncate'>
                                  {result.filepath}
                                </div>
                              </div>
                              <CheckCircle className='h-4 w-4 text-green-500 flex-shrink-0' />
                            </div>

                            <div className='space-y-2'>
                              <div className='flex justify-between text-xs'>
                                <span className='text-red-500'>
                                  Tương Đồng AI
                                </span>
                                <span className='font-medium'>
                                  {result.ai_similarity.toFixed(1)}%
                                </span>
                              </div>
                              <div className='w-full bg-muted rounded-full h-2'>
                                <div
                                  className='bg-red-500 h-2 rounded-full transition-all duration-300'
                                  style={{ width: `${result.ai_similarity}%` }}
                                />
                              </div>

                              <div className='flex justify-between text-xs'>
                                <span className='text-green-500'>
                                  Tương Đồng Con Người
                                </span>
                                <span className='font-medium'>
                                  {result.human_similarity.toFixed(1)}%
                                </span>
                              </div>
                              <div className='w-full bg-muted rounded-full h-2'>
                                <div
                                  className='bg-green-500 h-2 rounded-full transition-all duration-300'
                                  style={{
                                    width: `${result.human_similarity}%`,
                                  }}
                                />
                              </div>
                            </div>

                            <div className='flex justify-between items-center'>
                              {getSimilarityBadge(
                                result.ai_similarity,
                                result.human_similarity,
                              )}
                              <div className='text-xs text-muted-foreground text-right'>
                                <div>{result.loc} dòng</div>
                                <div>{formatFileSize(result.file_size)}</div>
                              </div>
                            </div>

                            <Button
                              size='sm'
                              variant='outline'
                              className='w-full'
                              onClick={() => handleViewDetails(result)}
                            >
                              <ExternalLink className='h-3 w-3 mr-1' />
                              Xem Chi Tiết
                            </Button>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </Scroller>
              </CardContent>
            </Card>
          )}

          {batchData.status === "processing" &&
            successfulResults.length === 0 && (
              <Card>
                <CardContent className='p-8 text-center'>
                  <Activity className='h-12 w-12 mx-auto text-muted-foreground/50 animate-pulse mb-4' />
                  <p className='text-muted-foreground'>Đang xử lý tệp...</p>
                  <p className='text-sm text-muted-foreground mt-1'>
                    Kết quả sẽ xuất hiện ở đây khi phân tích hoàn tất
                  </p>
                </CardContent>
              </Card>
            )}
        </div>
      )}
    </div>
  );
}
