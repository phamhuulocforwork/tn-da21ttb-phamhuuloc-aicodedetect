"use client";

import * as React from "react";

import {
  CheckCircle,
  Loader2,
  Shield,
  User,
  X,
} from "lucide-react";

import GoogleIcon from "@/components/icons/google-icons";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { getGoogleDriveService } from "@/lib/google-drive-service";

interface GoogleDriveAuthProps {
  onAuthSuccess: () => void;
  onAuthError: (error: string) => void;
}

export function GoogleDriveAuth({
  onAuthSuccess,
  onAuthError,
}: GoogleDriveAuthProps) {
  const [isInitializing, setIsInitializing] = React.useState(false);
  const [isAuthorizing, setIsAuthorizing] = React.useState(false);
  const [isAuthorized, setIsAuthorized] = React.useState(false);
  const [initError, setInitError] = React.useState<string | null>(null);

  const driveService = React.useMemo(() => getGoogleDriveService(), []);

  const isConfigured = React.useMemo(() => {
    return !!process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;
  }, []);

  React.useEffect(() => {
    if (isConfigured) {
      initializeService();
    }
  }, [isConfigured]);

  React.useEffect(() => {
    if (isAuthorized) {
      onAuthSuccess();
    }
  }, [isAuthorized, onAuthSuccess]);

  const initializeService = async () => {
    setIsInitializing(true);
    setInitError(null);

    try {
      const success = await driveService.initialize();
      if (!success) {
        throw new Error("Failed to initialize Google Drive service");
      }

      setIsAuthorized(driveService.isAuthorized());
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Unknown error";
      setInitError(errorMessage);
      onAuthError(errorMessage);
    } finally {
      setIsInitializing(false);
    }
  };

  const handleAuthorize = async () => {
    setIsAuthorizing(true);

    try {
      const success = await driveService.authorize();
      if (success) {
        setIsAuthorized(true);
        onAuthSuccess();
      } else {
        throw new Error("Authorization failed or was cancelled");
      }
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Authorization failed";
      onAuthError(errorMessage);
    } finally {
      setIsAuthorizing(false);
    }
  };

  const handleRevoke = async () => {
    try {
      await driveService.revokeAuthorization();
      setIsAuthorized(false);
      onAuthError("Đã ngắt kết nối khỏi Google Drive");
    } catch (error) {
      console.error("Failed to revoke authorization:", error);
      onAuthError("Không thể ngắt kết nối khỏi Google Drive");
    }
  };

  if (!isConfigured) {
    return (
      <Alert className='border-yellow-200 bg-yellow-50'>
        <Shield className='h-4 w-4 text-yellow-600' />
        <AlertDescription className='text-yellow-800'>
          <div className='space-y-2'>
            <p className='font-medium'>Google OAuth2 chưa được cấu hình</p>
          </div>
        </AlertDescription>
      </Alert>
    );
  }

  if (initError) {
    return (
      <Alert className='border-red-200 bg-red-50'>
        <X className='h-4 w-4 text-red-600' />
        <AlertDescription className='text-red-800'>
          <div className='space-y-2'>
            <p className='font-medium'>Lỗi khởi tạo Google Drive service</p>
            <p className='text-sm'>{initError}</p>
            <Button
              variant='outline'
              size='sm'
              onClick={initializeService}
              className='text-red-700 border-red-300 hover:bg-red-100'
            >
              Thử lại
            </Button>
          </div>
        </AlertDescription>
      </Alert>
    );
  }

  if (isAuthorized) {
    return (
      <Alert className='border-green-200 bg-green-50'>
        <CheckCircle className='h-4 w-4 text-green-600' />
        <AlertDescription className='text-green-800'>
          <div className='flex items-center justify-between'>
            <div>
              <p className='font-medium'>Đã kết nối với Google Drive</p>
              <p className='text-sm'>
                Bạn có thể truy cập files từ Google Drive của mình.
              </p>
            </div>
            <Button
              variant='outline'
              size='sm'
              onClick={handleRevoke}
              className='text-green-700 border-green-300 hover:bg-green-100'
            >
              Ngắt kết nối
            </Button>
          </div>
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <Card className='border-primary-200'>
      <CardHeader className='pb-4 flex justify-between'>
        <div className='space-y-2'>
          <div className='flex items-center gap-2'>
            <Shield className='h-5 w-5 text-primary-600' />
            <CardTitle className='text-primary-900'>
              Kết nối với Google Drive
            </CardTitle>
          </div>
          <CardDescription>
            Đăng nhập để truy cập trực tiếp files từ Google Drive của bạn mà
            không cần paste URL.
          </CardDescription>
        </div>
        <Button
          onClick={handleAuthorize}
          disabled={isInitializing || isAuthorizing}
          variant='outline'
        >
          {isInitializing && (
            <>
              <Loader2 className='h-4 w-4 mr-1 animate-spin' />
              Đang khởi tạo...
            </>
          )}
          {isAuthorizing && (
            <>
              <Loader2 className='h-4 w-4 mr-1 animate-spin' />
              Đang đăng nhập...
            </>
          )}
          {!isInitializing && !isAuthorizing && (
            <>
              <GoogleIcon className='h-4 w-4 mr-1' />
              Đăng nhập với Google
            </>
          )}
        </Button>
      </CardHeader>

      <CardContent className='space-y-4'>
        <div className='space-y-3'>
          <div className='flex items-center gap-3 text-sm'>
            <User className='h-4 w-4 text-green-600' />
            <span>Đăng nhập với tài khoản Google của bạn</span>
          </div>
          <div className='flex items-center gap-3 text-sm'>
            <Shield className='h-4 w-4 text-blue-600' />
            <span>Chỉ yêu cầu quyền đọc files (read-only)</span>
          </div>
          <div className='flex items-center gap-3 text-sm'>
            <CheckCircle className='h-4 w-4 text-purple-600' />
            <span>Tự động phát hiện và download files code</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default GoogleDriveAuth;
