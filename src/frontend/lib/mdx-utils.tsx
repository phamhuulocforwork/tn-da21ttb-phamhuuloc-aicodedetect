import { useState, useEffect } from "react";
import { MDXRemote } from "next-mdx-remote";
import { serialize } from "next-mdx-remote/serialize";
import remarkGfm from "remark-gfm";
import rehypeSlug from "rehype-slug";
import rehypeAutolinkHeadings from "rehype-autolink-headings";
import { Loader2, AlertCircle } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

// Default MDX components with Tailwind styling
export const defaultMdxComponents = {
  h1: ({ children }: { children: React.ReactNode }) => (
    <h1 className="text-3xl font-bold tracking-tight mb-6 text-foreground scroll-m-20">
      {children}
    </h1>
  ),
  h2: ({ children }: { children: React.ReactNode }) => (
    <h2 className="text-2xl font-semibold tracking-tight mb-4 text-foreground border-b pb-2 scroll-m-20">
      {children}
    </h2>
  ),
  h3: ({ children }: { children: React.ReactNode }) => (
    <h3 className="text-xl font-semibold tracking-tight mb-3 text-foreground scroll-m-20">
      {children}
    </h3>
  ),
  h4: ({ children }: { children: React.ReactNode }) => (
    <h4 className="text-lg font-semibold tracking-tight mb-2 text-foreground scroll-m-20">
      {children}
    </h4>
  ),
  p: ({ children }: { children: React.ReactNode }) => (
    <p className="mb-4 leading-7 text-muted-foreground [&:not(:first-child)]:mt-6">
      {children}
    </p>
  ),
  ul: ({ children }: { children: React.ReactNode }) => (
    <ul className="ml-6 list-disc mb-4 space-y-2 [&>li]:mt-2">{children}</ul>
  ),
  ol: ({ children }: { children: React.ReactNode }) => (
    <ol className="ml-6 list-decimal mb-4 space-y-2 [&>li]:mt-2">{children}</ol>
  ),
  li: ({ children }: { children: React.ReactNode }) => (
    <li className="leading-7">{children}</li>
  ),
  blockquote: ({ children }: { children: React.ReactNode }) => (
    <blockquote className="mt-6 border-l-2 border-primary/30 pl-6 italic text-muted-foreground bg-muted/30 py-4 rounded-r">
      {children}
    </blockquote>
  ),
  code: ({ children }: { children: React.ReactNode }) => (
    <code className="relative rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm font-semibold">
      {children}
    </code>
  ),
  pre: ({ children }: { children: React.ReactNode }) => (
    <pre className="mb-4 mt-6 overflow-x-auto rounded-lg border bg-muted p-4">
      <code className="relative rounded bg-muted font-mono text-sm">
        {children}
      </code>
    </pre>
  ),
  strong: ({ children }: { children: React.ReactNode }) => (
    <strong className="font-semibold text-foreground">{children}</strong>
  ),
  em: ({ children }: { children: React.ReactNode }) => (
    <em className="italic">{children}</em>
  ),
  table: ({ children }: { children: React.ReactNode }) => (
    <div className="my-6 w-full overflow-y-auto">
      <table className="w-full">{children}</table>
    </div>
  ),
  thead: ({ children }: { children: React.ReactNode }) => (
    <thead className="bg-muted/50">{children}</thead>
  ),
  tbody: ({ children }: { children: React.ReactNode }) => (
    <tbody className="[&_tr:last-child]:border-0">{children}</tbody>
  ),
  tr: ({ children }: { children: React.ReactNode }) => (
    <tr className="border-b transition-colors hover:bg-muted/50">
      {children}
    </tr>
  ),
  th: ({ children }: { children: React.ReactNode }) => (
    <th className="border px-4 py-2 text-left font-bold [&[align=center]]:text-center [&[align=right]]:text-right">
      {children}
    </th>
  ),
  td: ({ children }: { children: React.ReactNode }) => (
    <td className="border px-4 py-2 text-left [&[align=center]]:text-center [&[align=right]]:text-right">
      {children}
    </td>
  ),
  hr: () => <hr className="my-4 border-border" />,
  a: ({ children, href }: { children: React.ReactNode; href?: string }) => (
    <a
      href={href}
      className="font-medium text-primary underline underline-offset-4 hover:text-primary/80"
      target="_blank"
      rel="noopener noreferrer"
    >
      {children}
    </a>
  ),
};

interface MDXRendererProps {
  content: string;
  components?: Record<string, React.ComponentType<any>>;
  className?: string;
  loadingText?: string;
  errorTitle?: string;
  errorDescription?: string;
  onError?: (error: Error) => void;
}

export function MDXRenderer({
  content,
  components = defaultMdxComponents,
  className = "prose dark:prose-invert max-w-none",
  loadingText = "Đang xử lý nội dung...",
  errorTitle = "Lỗi xử lý nội dung",
  errorDescription = "Không thể hiển thị nội dung. Vui lòng thử lại.",
  onError,
}: MDXRendererProps) {
  const [mdxSource, setMdxSource] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const processMDX = async () => {
      if (!content?.trim()) {
        setLoading(false);
        setError("Không có nội dung để hiển thị");
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const serializedMdx = await serialize(content, {
          mdxOptions: {
            remarkPlugins: [remarkGfm],
            rehypePlugins: [rehypeSlug, rehypeAutolinkHeadings],
          },
        });
        setMdxSource(serializedMdx);
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : "Unknown error";
        console.error("Error serializing MDX:", err);
        setError(errorMsg);
        onError?.(err instanceof Error ? err : new Error(errorMsg));
      } finally {
        setLoading(false);
      }
    };

    processMDX();
  }, [content, onError]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <Loader2 className="h-6 w-6 animate-spin mr-2" />
        <span className="text-muted-foreground">{loadingText}</span>
      </div>
    );
  }

  if (error) {
    return (
      <Alert>
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>{errorTitle}</AlertTitle>
        <AlertDescription>
          {errorDescription}
          {process.env.NODE_ENV === "development" && (
            <details className="mt-2">
              <summary className="cursor-pointer text-sm opacity-70">
                Chi tiết lỗi
              </summary>
              <pre className="mt-1 text-xs opacity-70 whitespace-pre-wrap">
                {error}
              </pre>
            </details>
          )}
        </AlertDescription>
      </Alert>
    );
  }

  if (!mdxSource) {
    return (
      <div className="text-muted-foreground text-center py-4">
        Không có nội dung để hiển thị
      </div>
    );
  }

  return (
    <div className={className}>
      <MDXRemote {...mdxSource} components={components} />
    </div>
  );
}

// Hook for MDX processing
export function useMDXContent(content: string) {
  const [mdxSource, setMdxSource] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const processMDX = async (mdxContent: string) => {
    if (!mdxContent?.trim()) {
      setError("Không có nội dung để xử lý");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const serializedMdx = await serialize(mdxContent, {
        mdxOptions: {
          remarkPlugins: [remarkGfm],
          rehypePlugins: [rehypeSlug, rehypeAutolinkHeadings],
        },
      });
      setMdxSource(serializedMdx);
      return serializedMdx;
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : "Unknown error";
      console.error("Error serializing MDX:", err);
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (content) {
      processMDX(content);
    }
  }, [content]);

  return {
    mdxSource,
    loading,
    error,
    processMDX,
  };
}
