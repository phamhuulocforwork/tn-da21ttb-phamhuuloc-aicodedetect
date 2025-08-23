import React from "react";

import Link from "next/link";

import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <div className='flex items-center justify-center min-h-[60vh]'>
      <Button size='lg' asChild>
        <Link href='/analysis'>Bắt đầu phân tích</Link>
      </Button>
    </div>
  );
}
