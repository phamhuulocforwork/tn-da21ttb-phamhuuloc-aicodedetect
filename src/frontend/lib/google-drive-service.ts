declare global {
  interface Window {
    google: {
      accounts: {
        oauth2: {
          initTokenClient: (config: any) => any;
        };
      };
    };
    gapi: {
      load: (api: string, callback: () => void) => void;
      client: {
        init: (config: any) => Promise<void>;
        drive: {
          files: {
            list: (params: any) => Promise<any>;
            get: (params: any) => Promise<any>;
          };
        };
      };
      auth2: {
        getAuthInstance: () => any;
      };
    };
  }
}

export interface GoogleDriveFile {
  id: string;
  name: string;
  mimeType: string;
  size?: number;
  parents?: string[];
}

export interface ProcessedFile {
  filename: string;
  filepath: string;
  language: string;
  content: string;
  size: number;
}

export class GoogleDriveOAuthService {
  private tokenClient: any = null;
  private accessToken: string | null = null;
  private readonly CLIENT_ID: string;
  private readonly DISCOVERY_DOC =
    "https://www.googleapis.com/discovery/v1/apis/drive/v3/rest";
  private readonly SCOPES = "https://www.googleapis.com/auth/drive.readonly";

  constructor() {
    this.CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || "";

    if (!this.CLIENT_ID) {
      console.warn(
        "⚠️ NEXT_PUBLIC_GOOGLE_CLIENT_ID not set. Google Drive OAuth sẽ không hoạt động.",
      );
    }
  }

  /**
   * Initialize Google APIs and OAuth2
   */
  async initialize(): Promise<boolean> {
    try {
      // Load Google Identity Services
      await this.loadGoogleIdentityServices();

      // Load GAPI client
      await this.loadGAPIClient();

      // Initialize OAuth2 token client
      this.initializeTokenClient();

      console.log("✅ Google Drive OAuth service initialized");
      return true;
    } catch (error) {
      console.error("❌ Failed to initialize Google Drive OAuth:", error);
      return false;
    }
  }

  /**
   * Load Google Identity Services script
   */
  private loadGoogleIdentityServices(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (window.google?.accounts?.oauth2) {
        resolve();
        return;
      }

      const script = document.createElement("script");
      script.src = "https://accounts.google.com/gsi/client";
      script.onload = () => resolve();
      script.onerror = () =>
        reject(new Error("Failed to load Google Identity Services"));
      document.head.appendChild(script);
    });
  }

  /**
   * Load GAPI client
   */
  private loadGAPIClient(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (window.gapi?.client) {
        resolve();
        return;
      }

      const script = document.createElement("script");
      script.src = "https://apis.google.com/js/api.js";
      script.onload = () => {
        window.gapi.load("client", async () => {
          try {
            await window.gapi.client.init({
              discoveryDocs: [this.DISCOVERY_DOC],
            });
            resolve();
          } catch (error) {
            reject(error);
          }
        });
      };
      script.onerror = () => reject(new Error("Failed to load GAPI client"));
      document.head.appendChild(script);
    });
  }

  /**
   * Initialize OAuth2 token client
   */
  private initializeTokenClient(): void {
    if (!this.CLIENT_ID) {
      throw new Error("Google Client ID is required");
    }

    this.tokenClient = window.google.accounts.oauth2.initTokenClient({
      client_id: this.CLIENT_ID,
      scope: this.SCOPES,
      callback: (response: any) => {
        if (response.access_token) {
          this.accessToken = response.access_token;
          window.gapi.client.init({ access_token: response.access_token });
        }
      },
    });
  }

  /**
   * Request user authorization and get access token
   */
  async authorize(): Promise<boolean> {
    try {
      if (!this.tokenClient) {
        throw new Error("Token client not initialized");
      }

      return new Promise((resolve) => {
        this.tokenClient.callback = (response: any) => {
          if (response.access_token) {
            this.accessToken = response.access_token;
            window.gapi.client.init({
              access_token: response.access_token,
            });
            console.log("✅ Google Drive authorization successful");
            resolve(true);
          } else {
            console.error("❌ Authorization failed:", response);
            resolve(false);
          }
        };

        this.tokenClient.requestAccessToken({ prompt: "consent" });
      });
    } catch (error) {
      console.error("❌ Authorization error:", error);
      return false;
    }
  }

  /**
   * Check if user is currently authorized
   */
  isAuthorized(): boolean {
    return !!this.accessToken;
  }

  /**
   * Revoke authorization
   */
  async revokeAuthorization(): Promise<void> {
    if (this.accessToken) {
      await fetch(
        `https://oauth2.googleapis.com/revoke?token=${this.accessToken}`,
        {
          method: "POST",
        },
      );
      this.accessToken = null;
      console.log("✅ Authorization revoked");
    }
  }

  /**
   * Extract Google Drive ID from URL
   */
  extractDriveId(url: string): string | null {
    const patterns = [
      /\/file\/d\/([a-zA-Z0-9_-]+)/, // File URL
      /\/folders\/([a-zA-Z0-9_-]+)/, // Folder URL
      /id=([a-zA-Z0-9_-]+)/, // Query parameter
    ];

    for (const pattern of patterns) {
      const match = url.match(pattern);
      if (match) {
        return match[1];
      }
    }
    return null;
  }

  /**
   * List files in a Google Drive folder
   */
  async listFiles(folderId: string): Promise<GoogleDriveFile[]> {
    if (!this.isAuthorized()) {
      throw new Error("Not authorized. Call authorize() first.");
    }

    try {
      const response = await window.gapi.client.drive.files.list({
        q: `'${folderId}' in parents and trashed = false`,
        fields: "files(id, name, mimeType, size, parents)",
        pageSize: 1000,
      });

      return response.result.files || [];
    } catch (error) {
      console.error("❌ Error listing files:", error);
      throw new Error(`Failed to list files: ${error}`);
    }
  }

  /**
   * Get file content
   */
  async getFileContent(fileId: string): Promise<string> {
    if (!this.isAuthorized()) {
      throw new Error("Not authorized. Call authorize() first.");
    }

    try {
      const response = await fetch(
        `https://www.googleapis.com/drive/v3/files/${fileId}?alt=media`,
        {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        },
      );

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.text();
    } catch (error) {
      console.error("❌ Error getting file content:", error);
      throw new Error(`Failed to get file content: ${error}`);
    }
  }

  /**
   * Recursively process folder and get all code files
   */
  async processFolder(
    folderId: string,
    basePath: string = "",
  ): Promise<ProcessedFile[]> {
    const files = await this.listFiles(folderId);
    const processedFiles: ProcessedFile[] = [];
    const codeExtensions = [".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".txt"];

    for (const file of files) {
      if (file.mimeType === "application/vnd.google-apps.folder") {
        // Recursive process subfolder
        const subfolderFiles = await this.processFolder(
          file.id,
          `${basePath}${file.name}/`,
        );
        processedFiles.push(...subfolderFiles);
      } else {
        // Check if it's a code file
        const isCodeFile = codeExtensions.some((ext) =>
          file.name.toLowerCase().endsWith(ext),
        );

        if (isCodeFile) {
          try {
            const content = await this.getFileContent(file.id);
            const language = this.getFileLanguage(file.name);

            processedFiles.push({
              filename: file.name,
              filepath: `${basePath}${file.name}`,
              language,
              content,
              size: file.size ? parseInt(file.size.toString()) : content.length,
            });
          } catch (error) {
            console.warn(`⚠️ Failed to get content for ${file.name}:`, error);
          }
        }
      }
    }

    return processedFiles;
  }

  /**
   * Process Google Drive URL and get all code files
   */
  async processGoogleDriveUrl(url: string): Promise<ProcessedFile[]> {
    const driveId = this.extractDriveId(url);
    if (!driveId) {
      throw new Error("Invalid Google Drive URL");
    }

    return await this.processFolder(driveId);
  }

  /**
   * Determine file language from extension
   */
  private getFileLanguage(filename: string): string {
    const ext = filename.toLowerCase().split(".").pop();
    const languageMap: Record<string, string> = {
      c: "c",
      cpp: "cpp",
      cc: "cpp",
      cxx: "cpp",
      h: "c",
      hpp: "cpp",
      txt: "c",
    };
    return languageMap[ext || ""] || "c";
  }
}

// Global singleton instance
let googleDriveService: GoogleDriveOAuthService | null = null;

export function getGoogleDriveService(): GoogleDriveOAuthService {
  if (!googleDriveService) {
    googleDriveService = new GoogleDriveOAuthService();
  }
  return googleDriveService;
}

export default GoogleDriveOAuthService;
