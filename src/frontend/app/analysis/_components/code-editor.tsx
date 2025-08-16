"use client";

import { useCallback, useMemo, useState } from "react";

import { Editor as MonacoEditor } from "@monaco-editor/react";
import { FileCode, Loader2, Send } from "lucide-react";
import { editor } from "monaco-editor";
import { useTheme } from "next-themes";

import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import {
  AnalysisResponse,
  GeminiCombinedResponse,
  IndividualAnalysisResponse,
} from "@/lib/api-types";

export interface CodeEditorTheme {
  base: string;
  inherit: boolean;
  colors: Record<string, string>;
  rules: Array<{
    token: string;
    foreground?: string;
    background?: string;
    fontStyle?: string;
  }>;
}

export interface CodeEditorProps {
  value?: string;
  onChange?: (value: string | undefined) => void;
  language?: string;
  height?: string | number;
  theme?: "light" | "dark" | "system";
  customLightTheme?: CodeEditorTheme;
  customDarkTheme?: CodeEditorTheme;
  options?: editor.IStandaloneEditorConstructionOptions;
  className?: string;
  onSubmit?: (
    code: string,
    language: string,
  ) => Promise<
    AnalysisResponse | IndividualAnalysisResponse | GeminiCombinedResponse
  >;
  placeholder?: string;
  isSubmitting?: boolean;
}

const SUPPORTED_LANGUAGES = [
  { id: "c", name: "C", extensions: [".c"] },
  { id: "cpp", name: "C++", extensions: [".cpp", ".cxx", ".cc"] },
];

export function CodeEditor({
  value,
  onChange,
  language,
  height,
  theme: propTheme,
  customLightTheme,
  customDarkTheme,
  options,
  className,
  onSubmit,
  placeholder = "Nhập code của bạn vào đây...",
  isSubmitting = false,
  ...props
}: CodeEditorProps) {
  const { theme: systemTheme } = useTheme();
  const [selectedLanguage, setSelectedLanguage] = useState(language || "c");

  const activeTheme = propTheme || systemTheme || "dark";

  const detectedLanguage = useMemo(() => {
    if (selectedLanguage) return selectedLanguage;

    const languagePatterns = {
      c: /#include\s*<.*\.h>|int\s+main\s*\(|printf\s*\(|scanf\s*\(/,
      cpp: /#include\s*<iostream>|std::|cout\s*<<|cin\s*>>|namespace\s+std/,
      java: /public\s+class\s+\w+|public\s+static\s+void\s+main|System\.out\./,
      python:
        /def\s+\w+\s*\(|import\s+\w+|from\s+\w+\s+import|print\s*\(|if\s+__name__\s*==\s*["']__main__["']/,
      javascript: /\b(const|let|var|function|=>\s*{|console\.log)\b/,
      typescript: /\b(interface|type|namespace|:string|:number|:boolean)\b/,
    };

    if (!value) return "c";

    for (const [lang, pattern] of Object.entries(languagePatterns)) {
      if (pattern.test(value)) {
        return lang;
      }
    }

    return "c";
  }, [selectedLanguage, value]);

  const defaultOptions: editor.IStandaloneEditorConstructionOptions = {
    fontSize: 14,
    fontWeight: "500",
    fontFamily: "'JetBrains Mono', 'Fira Code', 'Consolas', monospace",
    scrollBeyondLastLine: false,
    automaticLayout: true,
    minimap: { enabled: false },
    lineNumbers: "on",
    wordWrap: "on",
    tabSize: 2,
    insertSpaces: true,
    bracketPairColorization: { enabled: true },
    cursorBlinking: "blink",
    formatOnPaste: true,
    formatOnType: true,
    suggestOnTriggerCharacters: true,
    quickSuggestions: true,
    parameterHints: { enabled: true },
    hover: { enabled: true },
    folding: true,
    foldingStrategy: "auto",
    renderLineHighlight: "all",
    selectOnLineNumbers: true,
    smoothScrolling: true,
    ...options,
  };

  const beforeMount = useCallback(
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (monaco: any) => {
      if (customLightTheme) {
        monaco.editor.defineTheme("custom-light-theme", customLightTheme);
      }

      if (customDarkTheme) {
        monaco.editor.defineTheme("custom-dark-theme", customDarkTheme);
      }

      // Configure language features
      monaco.languages.registerCompletionItemProvider("c", {
        provideCompletionItems: () => ({
          suggestions: [
            {
              label: "printf",
              kind: monaco.languages.CompletionItemKind.Function,
              insertText: 'printf("${1:format}", ${2:args});',
              insertTextRules:
                monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            },
            {
              label: "scanf",
              kind: monaco.languages.CompletionItemKind.Function,
              insertText: 'scanf("${1:format}", ${2:args});',
              insertTextRules:
                monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            },
          ],
        }),
      });
    },
    [customLightTheme, customDarkTheme],
  );

  const editorTheme = useMemo(() => {
    if (activeTheme === "light" && customLightTheme) {
      return "custom-light-theme";
    }

    if (activeTheme === "dark" && customDarkTheme) {
      return "custom-dark-theme";
    }

    return activeTheme === "dark" ? "vs-dark" : "light";
  }, [activeTheme, customLightTheme, customDarkTheme]);

  const handleSubmit = async () => {
    if (!value?.trim() || !onSubmit || isSubmitting) return;

    try {
      await onSubmit(value, detectedLanguage);
    } catch (error) {
      console.error("Analysis failed:", error);
    }
  };

  return (
    <div className='space-y-4 h-full flex flex-col'>
      <div className='flex items-center justify-between gap-4 flex-shrink-0'>
        <div className='flex items-center gap-2'>
          <Select
            value={selectedLanguage}
            onValueChange={(value) => setSelectedLanguage(value)}
          >
            <SelectTrigger className='w-[180px]'>
              <SelectValue placeholder='Ngôn ngữ' />
            </SelectTrigger>
            <SelectContent>
              {SUPPORTED_LANGUAGES.map((lang) => (
                <SelectItem key={lang.id} value={lang.id}>
                  {lang.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className='flex items-center gap-2'>
          {onSubmit && (
            <Button
              onClick={handleSubmit}
              disabled={!value?.trim() || isSubmitting}
              className='min-w-[120px]'
            >
              {isSubmitting ? (
                <Loader2 className='w-4 h-4 mr-1 animate-spin' />
              ) : (
                <Send className='w-4 h-4 mr-1' />
              )}
              {isSubmitting ? "Đang phân tích..." : "Phân tích mã"}
            </Button>
          )}
        </div>
      </div>

      <div className='relative rounded-md border flex-1'>
        <MonacoEditor
          value={value || ""}
          onChange={onChange}
          height={height}
          options={defaultOptions}
          className={className}
          language={detectedLanguage}
          theme={editorTheme}
          beforeMount={beforeMount}
          loading={
            <div className='flex h-full items-center justify-center text-sm text-muted-foreground'>
              <Loader2 className='w-5 h-5 animate-spin mr-2' />
              Đang tải...
            </div>
          }
          {...props}
        />

        {!value && (
          <div className='absolute inset-0 flex items-center justify-center pointer-events-none'>
            <div className='text-muted-foreground text-sm flex items-center gap-2'>
              <FileCode className='w-4 h-4' />
              {placeholder}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
