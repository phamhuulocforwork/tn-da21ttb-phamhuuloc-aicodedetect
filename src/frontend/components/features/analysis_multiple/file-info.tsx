import LanguageIcon from "@/components/shared/language-icons";

interface FileInfoProps {
  filename: string;
  language: string;
  file_size: number;
  loc: number;
}

export function FileInfo({
  filename,
  language,
  file_size,
  loc,
}: FileInfoProps) {
  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 B";
    const k = 1024;
    const sizes = ["B", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  return (
    <div className='flex items-start gap-3 w-full'>
      <LanguageIcon language={language} className='h-10 w-10 flex-shrink-0' />
      <div className='flex-1 min-w-0 space-y-2'>
        <div>
          <h3 className='font-medium text-sm truncate' title={filename}>
            {filename}
          </h3>
          <div className='text-sm text-muted-foreground'>
            {loc} dòng • Kích thước: {formatFileSize(file_size)}
          </div>
        </div>
      </div>
    </div>
  );
}
