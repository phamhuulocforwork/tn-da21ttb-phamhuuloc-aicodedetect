"use client";

import * as React from "react";

import {
  CheckCircle,
  ExternalLink,
  FileText,
  Link,
  RefreshCw,
  Upload,
  X,
} from "lucide-react";

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
import type { BatchAnalysisResponse } from "@/lib/api-types";
import type { ProcessedFile } from "@/lib/google-drive-service";

import {
  AnalysisResultCard,
  AnalysisResultCardSkeleton,
} from "./analysis-result-card";
import GoogleDriveAuth from "./google-drive-auth";
import GoogleDrivePicker from "./google-drive-picker";

export function MultipleAnalysisPage() {
  const [sourceType, setSourceType] = React.useState<
    "zip" | "google_drive_url" | "google_drive_oauth"
  >("zip");
  const [file, setFile] = React.useState<File | null>(null);
  const [googleDriveUrl, setGoogleDriveUrl] = React.useState("");
  const [oauthFiles, setOauthFiles] = React.useState<ProcessedFile[]>([]);
  const [isOauthAuthorized, setIsOauthAuthorized] = React.useState(false);

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

  const handleOauthAuthSuccess = () => {
    setIsOauthAuthorized(true);
    setError(null);
  };

  const handleOauthAuthError = (error: string) => {
    setError(error);
    setIsOauthAuthorized(false);
  };

  const handleOauthFilesSelected = (files: ProcessedFile[]) => {
    setOauthFiles(files);
    setError(null);
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
      } else if (sourceType === "google_drive_url" && googleDriveUrl) {
        data = await apiClient.analyzeBatchGoogleDrive({
          source_type: "google_drive",
          google_drive_url: googleDriveUrl,
        });
      } else if (sourceType === "google_drive_oauth" && oauthFiles.length > 0) {
        // Đọc file bằng OAuth - gửi BE phân tích
        data = await apiClient.analyzeBatchFromFiles(oauthFiles);
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

  const allResults = batchData?.results || [];
  const successfulResults = allResults.filter((r) => r.status === "success");

  return (
    <div className='container mx-auto py-6 max-h-[calc(100vh-var(--header-height))] flex flex-col'>
      {/* TODO: Thông báo lỗi */}
      {/* {error && (
        <Alert variant='destructive'>
          <AlertCircle className='h-4 w-4' />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )} */}

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
                setSourceType(
                  value as "zip" | "google_drive_url" | "google_drive_oauth",
                )
              }
            >
              <TabsList className='grid w-full grid-cols-3'>
                <TabsTrigger value='zip'>
                  <Upload className='h-4 w-4 mr-2' />
                  Tải Lên ZIP/RAR
                </TabsTrigger>
                <TabsTrigger value='google_drive_url'>
                  <Link className='h-4 w-4 mr-2' />
                  Google Drive URL
                </TabsTrigger>
                <TabsTrigger value='google_drive_oauth'>
                  <ExternalLink className='h-4 w-4 mr-2' />
                  Google Drive OAuth
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

              <TabsContent value='google_drive_url' className='space-y-4'>
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

              <TabsContent value='google_drive_oauth' className='space-y-4'>
                {!isOauthAuthorized ? (
                  <GoogleDriveAuth
                    onAuthSuccess={handleOauthAuthSuccess}
                    onAuthError={handleOauthAuthError}
                  />
                ) : (
                  <GoogleDrivePicker
                    onFilesSelected={handleOauthFilesSelected}
                    onError={handleOauthAuthError}
                  />
                )}
              </TabsContent>
            </Tabs>

            <Button
              onClick={handleStartAnalysis}
              disabled={
                isUploading ||
                (sourceType === "zip" && !file) ||
                (sourceType === "google_drive_url" && !googleDriveUrl) ||
                (sourceType === "google_drive_oauth" && oauthFiles.length === 0)
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
        <>
          <Card className='p-0'>
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
            <Card className='flex-1 flex flex-col min-h-0 mt-6'>
              <CardHeader className='flex-shrink-0'>
                <CardTitle className='flex items-center gap-2'>
                  <FileText className='h-5 w-5' />
                  Kết Quả Phân Tích ({successfulResults.length} files)
                </CardTitle>
                <CardDescription className='flex items-center gap-2'>
                  Nhấp vào nút <ExternalLink className='h-3.5 w-3.5' /> xem phân
                  tích chi tiết
                </CardDescription>
              </CardHeader>
              <CardContent className='flex-1 min-h-0 p-6'>
                <Scroller className='w-full'>
                  <div className='space-y-2'>
                    {allResults.map((result) => (
                      <AnalysisResultCard
                        key={result.analysis_id || result.filename}
                        result={result}
                      />
                    ))}
                  </div>
                </Scroller>
              </CardContent>
            </Card>
          )}

          {batchData.status === "processing" && allResults.length === 0 && (
            <Card className='mt-6'>
              <CardHeader className='flex-shrink-0'>
                <CardTitle className='flex items-center gap-2'>
                  <FileText className='h-5 w-5' />
                  Kết Quả Phân Tích
                </CardTitle>
                <CardDescription className='flex items-center gap-2'>
                  Đang phân tích {batchData.total_files} tệp...
                </CardDescription>
              </CardHeader>
              <CardContent className='p-8 text-center space-y-4'>
                {Array.from({ length: 4 }).map((_, i) => (
                  <AnalysisResultCardSkeleton key={i} />
                ))}
              </CardContent>
            </Card>
          )}
        </>
      )}
    </div>
  );
}
