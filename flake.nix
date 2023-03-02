{
  description = "deps for modbot";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
    flake-utils = { url = "github:numtide/flake-utils"; };
    poetry2nix = {
      url = "github:Lunarequest/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-compat, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ poetry2nix.overlay ];
        };
        lib = pkgs.lib;
        stdenv = pkgs.stdenv;
        ModBotEnv =  pkgs.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
          python = pkgs.python311;
          overrides = pkgs.poetry2nix.overrides.withDefaults (final: prev: {
            # Notice that using .overridePythonAttrs or .overrideAttrs wont work!
            mypy = prev.mypy.override { preferWheel = true; };
          });
        }; 
        in {
          packages = {
            modbot =  pkgs.poetry2nix.mkPoetryApplication {
            projectDir = ./.;
            python = pkgs.python311;
            overrides = pkgs.poetry2nix.overrides.withDefaults (final: prev: {
              # Notice that using .overridePythonAttrs or .overrideAttrs wont work!
              mypy = prev.mypy.override { preferWheel = true; };
            });
            };
            default = self.packages.${system}.myapp;
          };

          devShells.default = pkgs.mkShell {
            buildInputs = with pkgs; [
              ModBotEnv
            ];
            packages = with pkgs;[
              poetry2nix.packages.${system}.poetry
              zsh
            ];
            shellHook = ''
              test ~/.zshrc && exec zsh
            '';
          };

        });
      }
