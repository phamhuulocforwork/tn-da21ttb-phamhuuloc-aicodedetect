import React from "react";

import C from "../icons/c-icon";
import CPlusPlusIcon from "../icons/c-plusplus-icon";

interface LanguageIconProps {
  language: string;
  className?: string;
}

export function LanguageIcon({ language, className = "" }: LanguageIconProps) {
  if (!language) return null;

  return (
    <>
      {language.toLowerCase() === "cpp" && (
        <CPlusPlusIcon className={className} />
      )}
      {language.toLowerCase() === "c" && <C className={className} />}
    </>
  );
}

export default LanguageIcon;
