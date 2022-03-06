{
  description = "deps for modbot";

  inputs = {
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
    flake-utils = {
      url = "github:numtide/flake-utils";
    };
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
    };
  };

  outputs = { self, nixpkgs , flake-compat , flake-utils , poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ poetry2nix.overlay ];
        };
      in rec {
        packages.modbot = pkgs.poetry2nix.mkPoetryApplication {
          projectDir  = ./.;
          python = pkgs.python39;
        };
        defaultPackage = packages.modbot;
      }
    );
}
