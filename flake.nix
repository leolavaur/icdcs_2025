{

  description = "ICDCS 2024 Tutorial materials.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix, ... }: flake-utils.lib.eachDefaultSystem (system: 
    let
      pkgs = import nixpkgs { inherit system; config.allowUnfree = true; };
    in {
      devShells.default = with pkgs; mkShellNoCC {
        buildInputs = [ 
          python311
          poetry
        ];
      };
    });
}