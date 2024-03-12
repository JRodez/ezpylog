{ pkgs ? import <nixos-unstable> { }
, lib ? pkgs.lib
, python3Packages ? pkgs.python3Packages
, fetchPypi ? pkgs.fetchPypi
, nixosTests ? pkgs.nixosTests
, fetchFromGitHub ? pkgs.fetchFromGitHub
}:
let
  # stuff
in
python3Packages.buildPythonPackage rec {
  pname = "ezpylog";
  version = "2.2.0";
  doCheck = false;
  # format = "pyproject";

  src = ./.;


  nativeBuildInputs = [
    python3Packages.build
    python3Packages.setuptools
  ];
  propagatedBuildInputs = with python3Packages; [

  ];

  meta = with lib; {
    homepage = "https://github.com/jrodez/ezpylog";
    license = licenses.gpl3;
    description = "ezpylog is a minimalistic and easy to use python logger";
    maintainers = with maintainers; [ jrodez ];
  };
}
