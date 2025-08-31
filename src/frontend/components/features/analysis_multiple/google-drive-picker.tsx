"use client";

import * as React from "react";

import {
  CheckCircle,
  ExternalLink,
  FileText,
  Folder,
  Link,
  Loader2,
  LogIn,
  RefreshCw,
} from "lucide-react";

import { Alert, AlertDescription } from "@/components/ui/alert";
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

import {
  type ProcessedFile,
  getGoogleDriveService,
} from "@/lib/google-drive-service";

interface GoogleDrivePickerProps {
  onFilesSelected: (files: ProcessedFile[]) => void;
  onError: (error: string) => void;
}

export function GoogleDrivePicker({
  onFilesSelected,
  onError,
}: GoogleDrivePickerProps) {
  const [url, setUrl] = React.useState("");
  const [isProcessing, setIsProcessing] = React.useState(false);
  const [processedFiles, setProcessedFiles] = React.useState<ProcessedFile[]>(
    [],
  );
  const [urlError, setUrlError] = React.useState<string | null>(null);

  const driveService = React.useMemo(() => getGoogleDriveService(), []);

  const validateUrl = (inputUrl: string): boolean => {
    if (!inputUrl) return true;

    const isValidDriveUrl =
      inputUrl.includes("drive.google.com") &&
      (inputUrl.includes("/folders/") || inputUrl.includes("/file/d/"));

    if (!isValidDriveUrl) {
      setUrlError("URL không hợp lệ. Vui lòng nhập URL Google Drive hợp lệ.");
      return false;
    }

    setUrlError(null);
    return true;
  };

  const handleUrlChange = (value: string) => {
    setUrl(value);
    validateUrl(value);
  };

  const handleProcessUrl = async () => {
    if (!url || !validateUrl(url)) {
      return;
    }

    if (!driveService.isAuthorized()) {
      onError("Chưa được authorize. Vui lòng đăng nhập Google Drive trước.");
      return;
    }

    setIsProcessing(true);

    try {
      const files = await driveService.processGoogleDriveUrl(url);

      if (files.length === 0) {
        onError(
          "Không tìm thấy files code hợp lệ trong Google Drive folder/file này.",
        );
        return;
      }

      setProcessedFiles(files);
      onFilesSelected(files);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Unknown error";
      onError(`Lỗi xử lý Google Drive: ${errorMessage}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const getFileIcon = (filename: string) => {
    const ext = filename.toLowerCase().split(".").pop();
    const codeExts = ["c", "cpp", "cc", "cxx", "h", "hpp"];

    if (codeExts.includes(ext || "")) {
      return <FileText className='h-4 w-4 text-blue-600' />;
    }
    return <FileText className='h-4 w-4 text-gray-600' />;
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return "0 B";
    const k = 1024;
    const sizes = ["B", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  return (
    <div className='space-y-4'>
      <Card>
        <CardHeader className='pb-4'>
          <div className='flex items-center gap-2'>
            <Link className='h-5 w-5 text-blue-600' />
            <CardTitle>Google Drive URL</CardTitle>
          </div>
          <CardDescription>
            Nhập URL của Google Drive folder hoặc file để tự động truy cập và
            phân tích.
          </CardDescription>
        </CardHeader>

        <CardContent className='space-y-4'>
          <div>
            <div className='space-y-3'>
              <Label htmlFor='drive-url'>URL Google Drive</Label>
              <div className='flex gap-2'>
                <Input
                  id='drive-url'
                  value={url}
                  onChange={(e) => handleUrlChange(e.target.value)}
                  placeholder='https://drive.google.com/drive/folders/... hoặc https://drive.google.com/file/d/...'
                  className={urlError ? "border-red-300" : ""}
                />
                <Button
                  onClick={handleProcessUrl}
                  disabled={!url || !!urlError || isProcessing}
                  className='shrink-0'
                >
                  {isProcessing ? (
                    <>
                      <Loader2 className='h-4 w-4 mr-1 animate-spin' />
                      Đang xử lý...
                    </>
                  ) : (
                    "Tiếp tục"
                  )}
                </Button>
              </div>
            </div>
            {urlError && (
              <p className='text-xs font-semibold text-red-600 mt-1'>
                {urlError}
              </p>
            )}
            <p className='text-xs text-muted-foreground mt-2'>
              Dán liên kết của Google Drive là thư mục/tệp mà bạn có quyền truy
              cập.
            </p>
          </div>
        </CardContent>
      </Card>

      {processedFiles.length > 0 && (
        <Card>
          <CardHeader className='pb-4'>
            <div className='flex items-center justify-between'>
              <div className='flex items-center gap-2'>
                <CheckCircle className='h-5 w-5 text-green-600' />
                <CardTitle>Files được tìm thấy</CardTitle>
              </div>
              <Button
                variant='outline'
                size='sm'
                onClick={handleProcessUrl}
                disabled={isProcessing}
              >
                <RefreshCw className='h-4 w-4 mr-1' />
                Làm mới
              </Button>
            </div>
            <CardDescription>
              Đã tìm thấy{" "}
              <span className='font-semibold text-primary'>
                {processedFiles.length}
              </span>{" "}
              file{processedFiles.length !== 1 ? "s" : ""} code hợp lệ.
            </CardDescription>
          </CardHeader>

          <CardContent>
            <Scroller className='h-60' hideScrollbar>
              <div className='space-y-2'>
                {processedFiles.map((file, index) => (
                  <div
                    key={index}
                    className='flex items-center justify-between p-2 rounded-lg border '
                  >
                    <div className='flex items-center gap-2 flex-1 min-w-0'>
                      {getFileIcon(file.filename)}
                      <div className='flex-1 min-w-0'>
                        <p className='text-sm font-medium truncate'>
                          {file.filename}
                        </p>
                        <p className='text-xs text-muted-foreground truncate'>
                          {file.filepath}
                        </p>
                      </div>
                    </div>
                    <div className='flex items-center gap-2 text-xs text-muted-foreground'>
                      <span className='bg-blue-100 text-blue-800 px-2 py-1 rounded'>
                        {file.language.toUpperCase()}
                      </span>
                      <span>{formatFileSize(file.size)}</span>
                    </div>
                  </div>
                ))}
              </div>
            </Scroller>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

export default GoogleDrivePicker;
