{
  description = "Git repositories for Python projects";

  inputs = rec {
    nixos.url = "github:NixOS/nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils/v1.0.0";
    poetry2nix = {
      url = "github:nix-community/poetry2nix/v1.28.0";
      inputs.nixpkgs.follows = "nixos";
      inputs.flake-utils.follows = "flake-utils";
    };
    pythoneda-base = {
      url = "github:pythoneda/base/0.0.1a12";
      inputs.nixos.follows = "nixos";
      inputs.flake-utils.follows = "flake-utils";
      inputs.poetry2nix.follows = "poetry2nix";
    };
  };
  outputs = inputs:
    with inputs;
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixos { inherit system; };
        python = pkgs.python3;
        pythonPackages = python.pkgs;
        description = "Git repositories for Python projects";
        license = pkgs.lib.licenses.gpl3;
        homepage = "https://github.com/pythoneda/git-python";
        maintainers = with pkgs.lib.maintainers; [ ];
        nixpkgsRelease = "nixos-23.05";
        shared = import ./nix/devShells.nix;
        pythoneda-git-python-for = { version, pythoneda-base, python }:
          python.pkgs.buildPythonPackage rec {
            pname = "pythoneda-git-python";
            inherit version;
            src = ./.;
            format = "pyproject";

            nativeBuildInputs = with python.pkgs; [ pip poetry-core ];

            propagatedBuildInputs = with python.pkgs; [ pythoneda-base ];

            checkInputs = with python.pkgs; [ pytest pythoneda-base ];

            pythonImportsCheck = [ "pythonedagitpython" ];

            postInstall = ''
              mkdir $out/dist
              cp dist/*.whl $out/dist
            '';

            meta = with pkgs.lib; {
              inherit description license homepage maintainers;
            };
          };
        pythoneda-git-python-0_0_1a6-for = { pythoneda-base, python }:
          pythoneda-git-python-for {
            version = "0.0.1a6";
            inherit pythoneda-base python;
          };
      in rec {
        packages = rec {
          pythoneda-git-python-0_0_1a6-python38 =
            pythoneda-git-python-0_0_1a6-for {
              pythoneda-base =
                pythoneda-base.packages.${system}.pythoneda-base-latest-python38;
              python = pkgs.python38;
            };
          pythoneda-git-python-0_0_1a6-python39 =
            pythoneda-git-python-0_0_1a6-for {
              pythoneda-base =
                pythoneda-base.packages.${system}.pythoneda-base-latest-python39;
              python = pkgs.python39;
            };
          pythoneda-git-python-0_0_1a6-python310 =
            pythoneda-git-python-0_0_1a6-for {
              pythoneda-base =
                pythoneda-base.packages.${system}.pythoneda-base-latest-python310;
              python = pkgs.python310;
            };
          pythoneda-git-python-latest-python38 =
            pythoneda-git-python-0_0_1a6-python38;
          pythoneda-git-python-latest-python39 =
            pythoneda-git-python-0_0_1a6-python39;
          pythoneda-git-python-latest-python310 =
            pythoneda-git-python-0_0_1a6-python310;
          pythoneda-git-python-latest = pythoneda-git-python-latest-python310;
          default = packages.pythoneda-git-python-latest;
        };
        defaultPackage = packages.default;
        devShells = rec {
          pythoneda-git-python-0_0_1a6-python38 = shared.devShell-for {
            package = packages.pythoneda-git-python-0_0_1a6-python38;
            python = pkgs.python38;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-git-python-0_0_1a6-python39 = shared.devShell-for {
            package = packages.pythoneda-git-python-0_0_1a6-python39;
            python = pkgs.python39;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-git-python-0_0_1a6-python310 = shared.devShell-for {
            package = packages.pythoneda-git-python-0_0_1a6-python310;
            python = pkgs.python310;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-git-python-latest-python38 =
            pythoneda-git-python-0_0_1a6-python38;
          pythoneda-git-python-latest-python39 =
            pythoneda-git-python-0_0_1a6-python39;
          pythoneda-git-python-latest-python310 =
            pythoneda-git-python-0_0_1a6-python310;
          pythoneda-git-python-latest = pythoneda-git-python-latest-python310;
          default = pythoneda-git-python-latest;
        };
      });
}
