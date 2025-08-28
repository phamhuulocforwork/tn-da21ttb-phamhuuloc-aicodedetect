"use client";

import { useState } from "react";

import { FileText, Upload, X } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
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

interface FileUploadDialogProps {
  onFileContentLoaded: (content: string, filename: string) => void;
  disabled?: boolean;
}

export function FileUploadDialog({
  onFileContentLoaded,
  disabled = false,
}: FileUploadDialogProps) {
  const [files, setFiles] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  const handleFileUpload = async () => {
    if (files.length === 0) {
      toast.error("Vui lòng chọn file để tải lên");
      return;
    }

    const file = files[0];
    setIsLoading(true);

    try {
      const content = await file.text();

      onFileContentLoaded(content, file.name);
      setIsOpen(false);
      setFiles([]);

      toast.success("File đã được tải lên", {
        description: `Đã tải nội dung file ${file.name} vào editor`,
      });
    } catch (error) {
      console.error("File loading error:", error);
      toast.error("Không thể đọc file", {
        description:
          error instanceof Error
            ? error.message
            : "Đã xảy ra lỗi không xác định",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const onFileReject = (file: File, message: string) => {
    toast.error(`File bị từ chối: ${file.name}`, {
      description: message,
    });
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button
          variant='outline'
          disabled={disabled}
          className='flex items-center gap-2'
        >
          <Upload className='h-4 w-4' />
          Upload File
        </Button>
      </DialogTrigger>
      <DialogContent className=''>
        <DialogHeader>
          <DialogTitle>Tải lên file code</DialogTitle>
          <DialogDescription>
            Chọn file code (.c, .cpp, .cc, .cxx, .txt) để tải nội dung vào
            editor
          </DialogDescription>
        </DialogHeader>

        <FileUpload
          maxFiles={1}
          maxSize={1024 * 1024} // 1MB
          className='w-full'
          value={files}
          onValueChange={setFiles}
          onFileReject={onFileReject}
          accept='.c,.cpp,.cc,.cxx,.txt'
          disabled={isLoading}
        >
          <FileUploadDropzone>
            <div className='flex flex-col items-center gap-2 text-center p-4'>
              <div className='flex items-center justify-center rounded-full border p-3'>
                <FileText className='h-6 w-6 text-muted-foreground' />
              </div>
              <p className='font-medium text-sm'>
                Kéo thả file vào đây hoặc click để chọn
              </p>
              <p className='text-xs text-muted-foreground'>
                Hỗ trợ: .c, .cpp, .cc, .cxx, .txt (tối đa 1MB)
              </p>
            </div>
          </FileUploadDropzone>

          <FileUploadList>
            {files.map((file, index) => (
              <FileUploadItem key={index} value={file}>
                <FileUploadItemPreview />
                <FileUploadItemMetadata />
                <FileUploadItemDelete asChild>
                  <Button variant='ghost' size='icon' className='h-7 w-7'>
                    <X className='h-4 w-4' />
                  </Button>
                </FileUploadItemDelete>
              </FileUploadItem>
            ))}
          </FileUploadList>
        </FileUpload>

        <div className='flex justify-end gap-2 mt-4'>
          <Button
            variant='outline'
            onClick={() => setIsOpen(false)}
            disabled={isLoading}
          >
            Hủy
          </Button>
          <Button
            onClick={handleFileUpload}
            disabled={files.length === 0 || isLoading}
          >
            {isLoading ? "Đang tải..." : "Tải lên"}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
