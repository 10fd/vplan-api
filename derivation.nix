{
	lib,
	python3Packages
}:

with python3Packages;
buildPythonApplication rec {
	pname = "vplan-api";
	version = "main";
	src = ./.;
	
	propagatedBuildInputs = [ flask ];

	meta = with lib; {
		description = "Die API des Vertretungsplans am Taunusgymnasium";
		homepage = "https://github.com/10fd/vplan-api";
		license = licenses.mit;
	};
}
