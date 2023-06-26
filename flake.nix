{
  description = "Git repositories for Python projects";

  inputs = rec {
    nixos.url = "github:NixOS/nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils/v1.0.0";
    pythoneda-base = {
      url = "github:pythoneda/base/0.0.1a15";
      inputs.nixos.follows = "nixos";
      inputs.flake-utils.follows = "flake-utils";
    };
    pythoneda-event-git-python = {
      url = "github:pythoneda-event/git-python/0.0.1a1";
      inputs.nixos.follows = "nixos";
      inputs.flake-utils.follows = "flake-utils";
      inputs.pythoneda-base.follows = "pythoneda-base";
    };
    pythoneda-shared-git = {
      url = "github:pythoneda-shared/git/0.0.1a1";
      inputs.nixos.follows = "nixos";
      inputs.flake-utils.follows = "flake-utils";
      inputs.pythoneda-base.follows = "pythoneda-base";
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
        pythoneda-git-python-for = { version, pythoneda-base
          , pythoneda-shared-git, pythoneda-event-git-python, python }:
          let
            pname = "pythoneda-git-python";
            pythonVersionParts = builtins.splitVersion python.version;
            pythonMajorVersion = builtins.head pythonVersionParts;
            pythonMajorMinorVersion =
              "${pythonMajorVersion}.${builtins.elemAt pythonVersionParts 1}";
            pnameWithUnderscores =
              builtins.replaceStrings [ "-" ] [ "_" ] pname;
            wheelName =
              "${pnameWithUnderscores}-${version}-py${pythonMajorVersion}-none-any.whl";
          in python.pkgs.buildPythonPackage rec {
            inherit pname version;
            projectDir = ./.;
            src = ./.;
            format = "pyproject";

            nativeBuildInputs = with python.pkgs; [ pip pkgs.jq poetry-core ];
            propagatedBuildInputs = with python.pkgs; [
              pythoneda-base
              pythoneda-event-git-python
              pythoneda-shared-git
            ];

            checkInputs = with python.pkgs; [ pytest ];

            pythonImportsCheck = [ "pythonedagitpython" ];

            preBuild = ''
              python -m venv .env
              source .env/bin/activate
              pip install ${pythoneda-base}/dist/pythoneda_base-${pythoneda-base.version}-py3-none-any.whl
              pip install ${pythoneda-shared-git}/dist/pythoneda_shared_git-${pythoneda-shared-git.version}-py3-none-any.whl
              pip install ${pythoneda-event-git-python}/dist/pythoneda_event_git_python-${pythoneda-event-git-python.version}-py3-none-any.whl
              rm -rf .env
            '';

            postInstall = ''
              mkdir $out/dist
              cp dist/${wheelName} $out/dist
              jq ".url = \"$out/dist/${wheelName}\"" $out/lib/python${pythonMajorMinorVersion}/site-packages/${pnameWithUnderscores}-${version}.dist-info/direct_url.json > temp.json && mv temp.json $out/lib/python${pythonMajorMinorVersion}/site-packages/${pnameWithUnderscores}-${version}.dist-info/direct_url.json
            '';

            meta = with pkgs.lib; {
              inherit description license homepage maintainers;
            };
          };
        pythoneda-git-python-0_0_1a8-for = { pythoneda-base
          , pythoneda-shared-git, pythoneda-event-git-python, python }:
          pythoneda-git-python-for {
            version = "0.0.1a8";
            inherit pythoneda-base pythoneda-shared-git
              pythoneda-event-git-python python;
          };
      in rec {
        packages = rec {
          pythoneda-git-python-0_0_1a8-python38 =
            pythoneda-git-python-0_0_1a8-for {
              pythoneda-base =
                pythoneda-base.packages.${system}.pythoneda-base-latest-python38;
              pythoneda-shared-git =
                pythoneda-shared-git.packages.${system}.pythoneda-shared-git-latest-python38;
              pythoneda-event-git-python =
                pythoneda-event-git-python.packages.${system}.pythoneda-event-git-python-latest-python38;
              python = pkgs.python38;
            };
          pythoneda-git-python-0_0_1a8-python39 =
            pythoneda-git-python-0_0_1a8-for {
              pythoneda-base =
                pythoneda-base.packages.${system}.pythoneda-base-latest-python39;
              pythoneda-shared-git =
                pythoneda-shared-git.packages.${system}.pythoneda-shared-git-latest-python39;
              pythoneda-event-git-python =
                pythoneda-event-git-python.packages.${system}.pythoneda-event-git-python-latest-python39;
              python = pkgs.python39;
            };
          pythoneda-git-python-0_0_1a8-python310 =
            pythoneda-git-python-0_0_1a8-for {
              pythoneda-base =
                pythoneda-base.packages.${system}.pythoneda-base-latest-python310;
              pythoneda-shared-git =
                pythoneda-shared-git.packages.${system}.pythoneda-shared-git-latest-python310;
              pythoneda-event-git-python =
                pythoneda-event-git-python.packages.${system}.pythoneda-event-git-python-latest-python310;
              python = pkgs.python310;
            };
          pythoneda-git-python-latest-python38 =
            pythoneda-git-python-0_0_1a8-python38;
          pythoneda-git-python-latest-python39 =
            pythoneda-git-python-0_0_1a8-python39;
          pythoneda-git-python-latest-python310 =
            pythoneda-git-python-0_0_1a8-python310;
          pythoneda-git-python-latest = pythoneda-git-python-latest-python310;
          default = packages.pythoneda-git-python-latest;
        };
        defaultPackage = packages.default;
        devShells = rec {
          pythoneda-git-python-0_0_1a8-python38 = shared.devShell-for {
            package = packages.pythoneda-git-python-0_0_1a8-python38;
            pythoneda-base =
              pythoneda-base.packages.${system}.pythoneda-base-latest-python38;
            python = pkgs.python38;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-git-python-0_0_1a8-python39 = shared.devShell-for {
            package = packages.pythoneda-git-python-0_0_1a8-python39;
            pythoneda-base =
              pythoneda-base.packages.${system}.pythoneda-base-latest-python39;
            python = pkgs.python39;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-git-python-0_0_1a8-python310 = shared.devShell-for {
            package = packages.pythoneda-git-python-0_0_1a8-python310;
            pythoneda-base =
              pythoneda-base.packages.${system}.pythoneda-base-latest-python310;
            python = pkgs.python310;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-git-python-latest-python38 =
            pythoneda-git-python-0_0_1a8-python38;
          pythoneda-git-python-latest-python39 =
            pythoneda-git-python-0_0_1a8-python39;
          pythoneda-git-python-latest-python310 =
            pythoneda-git-python-0_0_1a8-python310;
          pythoneda-git-python-latest = pythoneda-git-python-latest-python310;
          default = pythoneda-git-python-latest;
        };
      });
}
