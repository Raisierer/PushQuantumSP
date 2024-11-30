{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    systems.url = "github:nix-systems/default";
    devenv.url = "github:cachix/devenv";
    devenv.inputs.nixpkgs.follows = "nixpkgs";
  };

  nixConfig = {
    extra-trusted-public-keys = "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  outputs = { self, nixpkgs, devenv, systems, ... } @ inputs:
    let
      forEachSystem = nixpkgs.lib.genAttrs (import systems);
    in
    {
      packages = forEachSystem (system: {
        devenv-up = self.devShells.${system}.default.config.procfileScript;
        devenv-test = self.devShells.${system}.default.config.test;
      });

      devShells = forEachSystem
        (system:
          let
            pkgs = nixpkgs.legacyPackages.${system};
          in
          {
            default = devenv.lib.mkShell {
              inherit inputs pkgs;
              modules = [
                {
                  # https://devenv.sh/reference/options/
                  packages = [
                    pkgs.hello
                    pkgs.python311Packages.numpy
                    pkgs.python311Packages.matplotlib
                    pkgs.python311Packages.simanneal
                  ];

                  enterShell = ''
                    hello
                  '';

                  languages = {
                    python = {
                      enable = true;
                      package = pkgs.python311;
                      libraries = [
                      ];
                      uv = {
                        enable = true;
                        sync.enable = true;
                      };
                    };
                  };

                  processes.hello.exec = "hello";

                  env.UV_PYTHON_PREFERENCE = "only-system";
                  env.UV_PYTHON = "${pkgs.python311}";

                  env.LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
                }
              ];
            };
          });
    };
}
