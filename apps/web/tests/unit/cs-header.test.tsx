import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { CsHeader } from "../../src/components/convergencia-serena/CsHeader";

describe("CsHeader", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "matchMedia",
      vi.fn().mockReturnValue({ matches: false }),
    );
  });

  it("does not render a search input", () => {
    render(<CsHeader />);
    expect(screen.queryByPlaceholderText(/Buscar materiales/i)).toBeNull();
    expect(screen.queryByRole("searchbox")).toBeNull();
    expect(screen.getByRole("button", { name: /Usar tema/i })).toBeTruthy();
  });
});
