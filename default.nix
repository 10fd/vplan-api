{
	lib,
	python3Packages
}:
with python3Packages;
buildPythonApplication {
	pname = "vplan-api";
	version = "main";
	propagatedBuildInputs = [ flask ];
	src = ./.;
}
