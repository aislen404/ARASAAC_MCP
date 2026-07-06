import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { ThemeToggle } from "../../src/components/theme-toggle";

describe("ThemeToggle", () => {
  beforeEach(() => {
    window.localStorage.clear();
    document.documentElement.removeAttribute("data-theme");
    vi.stubGlobal(
      "matchMedia",
      vi.fn().mockReturnValue({ matches: false }),
    );
  });

  it("exposes state and persists the selected theme", async () => {
    render(<ThemeToggle />);
    const button = screen.getByRole("button", { name: "Usar tema oscuro" });

    expect(button.getAttribute("aria-pressed")).toBe("false");
    fireEvent.click(button);

    await waitFor(() => {
      expect(
        screen
          .getByRole("button", { name: "Usar tema claro" })
          .getAttribute("aria-pressed"),
      ).toBe("true");
    });
    expect(document.documentElement.dataset.theme).toBe("dark");
    expect(window.localStorage.getItem("arasaac-theme")).toBe("dark");
  });
});
