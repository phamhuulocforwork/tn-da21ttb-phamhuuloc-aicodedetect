import { Providers } from "@/components/shared/providers";

import "@/styles/globals.css";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang='vi' suppressHydrationWarning>
      <body className='antialiased font-sans'>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
