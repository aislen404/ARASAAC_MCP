export function CsIllustration({
  alt,
  className,
  height,
  src,
  width,
  ariaHidden,
}: Readonly<{
  alt: string;
  className?: string;
  height: number;
  src: string;
  width: number;
  ariaHidden?: boolean;
}>) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- local SVG assets from /convergencia-serena/
    <img
      alt={alt}
      aria-hidden={ariaHidden ? true : undefined}
      className={className}
      height={height}
      src={src}
      width={width}
    />
  );
}
