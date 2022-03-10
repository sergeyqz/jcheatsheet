with import <nixpkgs> {};

let
  python = python39;
  pythonEnv = python.withPackages (ps: [
    ps.ipython ps.ipdb
    ps.markdown
  ]);
in mkShell {
  buildInputs = [
    pythonEnv
  ];
}
