{pkgs ? import <nixpkgs> {}, ...}:
pkgs.mkShellNoCC {
  name = "icdcs-2025";

  packages = with pkgs; [
    # LaTeX
    texliveFull
    tex-fmt

    # Python
    python312
    uv
  ];

  shellHook = ''
    unset PYTHONPATH

    test -d .venv && source .venv/bin/activate || echo "No virtualenv found."
  '';
}
