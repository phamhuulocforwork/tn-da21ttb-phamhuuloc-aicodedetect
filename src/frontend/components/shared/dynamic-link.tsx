import Link from "next/link";

import { ArrowRight, ExternalLink } from "lucide-react";

import { buttonVariants } from "@/components/ui/button";

import { cn, getIsExternalLink } from "@/lib/utils";

interface DynamicLinkProps extends React.ComponentPropsWithoutRef<typeof Link> {
  isExternal?: boolean;
}

export function DynamicLink({
  href,
  children,
  isExternal,
  ...props
}: DynamicLinkProps) {
  const isExternalLink = isExternal || getIsExternalLink(href.toString());

  return (
    <Link
      href={href}
      target={isExternalLink ? "_blank" : "_self"}
      className={cn(
        buttonVariants({
          variant: "ghost",
          size: "icon",
          className: "px-2 py-0.5 [&_svg]:size-3.5",
        }),
      )}
      {...props}
    >
      {children}
      {isExternalLink ? (
        <ExternalLink aria-hidden='true' />
      ) : (
        <ArrowRight aria-hidden='true' />
      )}
    </Link>
  );
}
