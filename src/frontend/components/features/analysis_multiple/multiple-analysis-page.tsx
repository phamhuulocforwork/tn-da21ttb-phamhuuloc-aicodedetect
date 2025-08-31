"use client";

import * as React from "react";

import {
  CheckCircle,
  ExternalLink,
  FileText,
  Link,
  RefreshCw,
  Send,
  Upload,
  X,
} from "lucide-react";

import GoogleDrive from "@/components/icons/google-drive-icon";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  FileUpload,
  FileUploadDropzone,
  FileUploadItem,
  FileUploadItemDelete,
  FileUploadItemMetadata,
  FileUploadItemPreview,
  FileUploadList,
  FileUploadTrigger,
} from "@/components/ui/file-upload";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
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
    "file_upload" | "google_drive_oauth"
  >("file_upload");
  const [uploadType, setUploadType] = React.useState<
    "zip" | "google_drive_url"
  >("zip");
  const [file, setFile] = React.useState<File | null>(null);
  const [files, setFiles] = React.useState<File[]>([]);
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

  const handleFilesChange = (newFiles: File[]) => {
    if (newFiles.length > 0) {
      const selectedFile = newFiles[0];
      if (
        !selectedFile.name.endsWith(".zip") &&
        !selectedFile.name.endsWith(".rar")
      ) {
        setError("Chỉ hỗ trợ file ZIP hoặc RAR");
        setFile(null);
        setFiles([]);
        return;
      }

      const maxSize = 50 * 1024 * 1024; // 50MB
      if (selectedFile.size > maxSize) {
        setError("File không được vượt quá 50MB");
        setFile(null);
        setFiles([]);
        return;
      }

      setFile(selectedFile);
      setFiles(newFiles);
      setError(null);
    } else {
      setFile(null);
      setFiles([]);
    }
  };

  const handleFileReject = (rejectedFile: File, message: string) => {
    setError(`${rejectedFile.name}: ${message}`);
    setFile(null);
    setFiles([]);
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

      if (sourceType === "file_upload") {
        if (uploadType === "zip" && file) {
          data = await apiClient.uploadBatchZip(file);
        } else if (uploadType === "google_drive_url" && googleDriveUrl) {
          data = await apiClient.analyzeBatchGoogleDrive({
            source_type: "google_drive",
            google_drive_url: googleDriveUrl,
          });
        } else {
          throw new Error(
            "Vui lòng chọn file hoặc nhập URL Google Drive hợp lệ",
          );
        }
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
    <div className='container mx-auto py-6 h-[calc(100vh-var(--header-height))] flex flex-col'>
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
                setSourceType(value as "file_upload" | "google_drive_oauth")
              }
            >
              <TabsList className='grid w-full grid-cols-2'>
                <TabsTrigger value='file_upload'>
                  <Upload className='h-4 w-4 mr-1' />
                  Tải Lên File
                </TabsTrigger>
                <TabsTrigger value='google_drive_oauth'>
                  <GoogleDrive className='h-4 w-4 mr-1' />
                  Google Drive
                </TabsTrigger>
              </TabsList>

              <TabsContent value='file_upload' className='space-y-4'>
                <RadioGroup
                  value={uploadType}
                  onValueChange={(value) =>
                    setUploadType(value as "zip" | "google_drive_url")
                  }
                  className='space-y-4'
                >
                  <div className='flex items-center space-x-2'>
                    <RadioGroupItem value='zip' id='zip-upload' />
                    <Label htmlFor='zip-upload' className='cursor-pointer'>
                      Tải lên file ZIP/RAR
                    </Label>
                  </div>

                  {uploadType === "zip" && (
                    <div className='ml-6 space-y-4'>
                      <Label>Chọn tệp ZIP/RAR</Label>
                      <FileUpload
                        maxFiles={1}
                        maxSize={50 * 1024 * 1024} // 50MB
                        value={files}
                        onValueChange={handleFilesChange}
                        onFileReject={handleFileReject}
                        accept='.zip,.rar'
                      >
                        <FileUploadDropzone>
                          <div className='flex flex-col items-center gap-2 text-center p-4'>
                            <div className='flex items-center justify-center rounded-full border p-3'>
                              <Upload className='h-6 w-6 text-muted-foreground' />
                            </div>
                            <p className='font-medium text-sm'>
                              Kéo thả file ZIP/RAR vào đây hoặc click để chọn
                            </p>
                            <p className='text-xs text-muted-foreground'>
                              Hỗ trợ: .zip, .rar (tối đa 50MB)
                            </p>
                          </div>
                        </FileUploadDropzone>

                        <FileUploadList>
                          {files.map((file, index) => (
                            <FileUploadItem key={index} value={file}>
                              <FileUploadItemPreview />
                              <FileUploadItemMetadata />
                              <FileUploadItemDelete asChild>
                                <Button
                                  variant='ghost'
                                  size='icon'
                                  className='h-7 w-7'
                                >
                                  <X className='h-4 w-4' />
                                </Button>
                              </FileUploadItemDelete>
                            </FileUploadItem>
                          ))}
                        </FileUploadList>
                      </FileUpload>
                    </div>
                  )}

                  <div className='flex items-center space-x-2'>
                    <RadioGroupItem value='google_drive_url' id='drive-url' />
                    <Label htmlFor='drive-url' className='cursor-pointer'>
                      Nhập URL Google Drive
                    </Label>
                  </div>

                  {uploadType === "google_drive_url" && (
                    <div className='ml-6 space-y-2'>
                      <Label htmlFor='drive-url-input'>URL Google Drive</Label>
                      <Input
                        id='drive-url-input'
                        value={googleDriveUrl}
                        onChange={(e) =>
                          handleGoogleDriveUrlChange(e.target.value)
                        }
                        placeholder='https://drive.google.com/drive/folders/... hoặc https://drive.google.com/file/d/...'
                      />
                      <p className='text-xs text-muted-foreground'>
                        Dán một liên kết thư mục hoặc tệp Google Drive mà bạn có
                        quyền truy cập.
                      </p>
                    </div>
                  )}
                </RadioGroup>
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
                (sourceType === "file_upload" &&
                  ((uploadType === "zip" && !file) ||
                    (uploadType === "google_drive_url" && !googleDriveUrl))) ||
                (sourceType === "google_drive_oauth" && oauthFiles.length === 0)
              }
              className='w-full'
            >
              {isUploading ? (
                <>
                  <RefreshCw className='h-4 w-4 mr-1 animate-spin' />
                  Bắt Đầu Phân Tích...
                </>
              ) : (
                <>
                  <Send className='w-4 h-4 mr-1' />
                  Phân Tích
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
                <Scroller className='h-full' hideScrollbar>
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
