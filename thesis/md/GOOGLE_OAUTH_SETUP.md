# Google OAuth2 Frontend Setup Guide

## Tổng quan

Frontend này hỗ trợ Google Drive OAuth2 để user có thể tự authenticate và truy cập files từ Google Drive mà không cần setup thủ công ở backend.

## Cấu hình Google Cloud Console

### Bước 1: Tạo OAuth2 Client ID

1. Truy cập [Google Cloud Console](https://console.cloud.google.com/)
2. Chọn hoặc tạo project mới
3. Bật Google Drive API:

   ```
   APIs & Services → Library → Search "Google Drive API" → Enable
   ```

4. Tạo OAuth2 credentials:

   ```
   APIs & Services → Credentials → Create Credentials → OAuth client ID
   ```

5. Chọn **"Web application"**

6. Cấu hình **Authorized JavaScript origins**:

   ```
   Development: http://localhost:3000
   Production: https://yourdomain.com
   ```

7. **Không cần** Authorized redirect URIs (sử dụng popup flow)

8. Click **Create** và copy **Client ID**

### Bước 2: Cấu hình Environment Variables

Tạo file `.env.local` trong thư mục frontend:

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your_google_oauth_client_id_here
```

**Lưu ý:** Client ID có format:

```
123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com
```

## Cách sử dụng

### 1. User Flow

1. User chọn tab **"Google Drive OAuth"**
2. Click **"Đăng nhập với Google"**
3. Popup Google authentication mở ra
4. User authorize app để truy cập Google Drive (read-only)
5. Nhập Google Drive URL
6. App tự động truy cập và download files
7. Phân tích files như bình thường

### 2. Technical Flow

```typescript
// 1. Initialize Google OAuth service
const driveService = getGoogleDriveService();
await driveService.initialize();

// 2. User authorize
const success = await driveService.authorize();

// 3. Process Google Drive URL
const files = await driveService.processGoogleDriveUrl(driveUrl);

// 4. Send files to backend for analysis
const results = await apiClient.analyzeBatchFromFiles(files);
```

## Ưu điểm so với Backend OAuth

### ✅ Frontend OAuth (Khuyến nghị)

- **User-friendly**: Không cần setup thủ công
- **Secure**: User tự control permissions
- **Scalable**: Không cần store credentials ở server
- **Real-time**: Truy cập trực tiếp mà không qua proxy
- **Flexible**: User có thể revoke access bất cỳ lúc nào

### ⚠️ Backend OAuth (Legacy)

- **Setup phức tạp**: Cần Service Account hoặc OAuth setup
- **Security risk**: Credentials stored on server
- **Rate limiting**: Shared quota cho all users
- **Maintenance**: Cần manage token refresh

## Testing

### 1. Test Environment Setup

```bash
cd src/frontend
npm install
npm run dev
```

### 2. Test Google OAuth

1. Mở http://localhost:3000
2. Navigate to Multiple Analysis page
3. Chọn tab "Google Drive OAuth"
4. Kiểm tra:
   - ✅ Hiển thị đúng setup guide nếu chưa config
   - ✅ Initialize Google APIs thành công
   - ✅ Popup authorization hoạt động
   - ✅ File picker hoạt động với URL

### 3. Test Integration

Tạo một Google Drive folder với vài files .c/.cpp và test:

```
1. Share folder publicly hoặc với account test
2. Copy folder URL: https://drive.google.com/drive/folders/abc123
3. Paste vào OAuth picker
4. Verify files được detect và download
5. Verify analysis results
```

## Troubleshooting

### Lỗi thường gặp:

#### "OAuth client not configured"

- ✅ Check NEXT_PUBLIC_GOOGLE_CLIENT_ID có đúng không
- ✅ Restart development server sau khi thay đổi env

#### "Popup blocked"

- ✅ Allow popups cho domain này
- ✅ Thử authorization trong tab mới

#### "Invalid origin"

- ✅ Add localhost:3000 vào Authorized JavaScript origins
- ✅ Add production domain nếu deploy

#### "Access denied"

- ✅ Folder/file có được share không?
- ✅ Account có quyền truy cập không?
- ✅ URL format đúng không?

### Debug Mode

Mở Developer Console để xem logs:

```javascript
// Check if OAuth service initialized
console.log("Google OAuth available:", window.google);

// Check authorization status
const driveService = getGoogleDriveService();
console.log("Authorized:", driveService.isAuthorized());
```

## Performance Tips

1. **File size limits**: Files > 1MB có thể chậm
2. **Concurrent requests**: Google Drive có rate limits
3. **Folder depth**: Deep nested folders mất thời gian
4. **Browser memory**: Quá nhiều files có thể làm chậm browser

## Security Notes

- **Read-only access**: App chỉ yêu cầu quyền đọc
- **No data storage**: Files không được lưu trên server
- **Client-side only**: OAuth credentials chỉ ở browser
- **User control**: User có thể revoke access bất cỳ lúc nào

## Migration từ Backend OAuth

Nếu bạn đang dùng backend OAuth:

1. Giữ nguyên backend endpoints (backward compatibility)
2. Thêm frontend OAuth như option mới
3. User có thể chọn method prefer
4. Sau khi stable, có thể deprecate backend OAuth

## Production Deployment

### Environment Variables

```bash
# Production .env.local
NEXT_PUBLIC_API_URL=https://your-api-domain.com
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your_production_client_id
```

### Google Cloud Console Production Setup

1. Tạo separate project cho production
2. Add production domain vào Authorized origins
3. Use separate Client ID cho production
4. Monitor quota usage trong Console

### Verification

- ✅ HTTPS required cho production domains
- ✅ Domain verification có thể cần thiết
- ✅ Test thoroughly trước khi deploy
- ✅ Monitor error logs sau deploy
