export type CsIconName = "accessibility" | "activity" | "analytics" | "aria" | "bell" | "book" | "calendar" | "chat" | "check" | "compass" | "contrast" | "copy" | "download" | "edit" | "external" | "eye" | "filter" | "folder" | "grid" | "heart" | "help" | "home" | "info" | "keyboard" | "leaf" | "list" | "lock" | "minus" | "moon" | "palette" | "people" | "plane" | "plus" | "route" | "search" | "settings" | "shield" | "spark" | "success" | "sun" | "target" | "trash" | "upload" | "user" | "warning";

export function CsIcon({
  name,
  label,
  className = "cs-asset-icon",
}: {
  name: CsIconName;
  label?: string;
  className?: string;
}) {
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      alt={label ?? ""}
      aria-hidden={label ? undefined : true}
      className={className}
      height={24}
      src={`/convergencia-serena/icons/${name}.svg`}
      width={24}
    />
  );
}
