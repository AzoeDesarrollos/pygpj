Name "PyGPJ"

outfile "PyGPJ.exe"
InstallDir $PROGRAMFILES\GPJ

PageEx license
	Caption "PyGPJ: Acuerdo de Licencia"
	LicenseData licdata.txt
	LicenseForceSelection radiobuttons "Acepto" "No acepto"
PageExEnd

PageEx components
	Caption "PyGPJ: Selección de componentes"
PageExEnd

PageEx directory
	Caption "PyGPJ: Directorio de instalación"
	DirText "PyGPJ se instalará en el siguiente directorio. Para seleccionar un directorio diferente, haga clic en Buscar y elija un directorio distinto." "Destino" "Buscar" "Seleccione el directorio donde se realizará la instalación de PyGPJ"
PageExEnd

PageEx instfiles
	Caption "PyGPJ: Instalando componentes"
PageExEnd

Section "PyGPJ"
	SetOutPath $INSTDIR
	WriteUninstaller Desisntalar.exe
	File main.py
	File LICENSE.txt

	SetOutPath $INSTDIR\doc
	File doc\aptitudes_doc.txt
	File doc\dotes_doc.txt
	File doc\armas_doc.txt
	File doc\armaduras_doc.txt

	SetOutPath $INSTDIR\func
	File func\__init__.py

	SetOutPath $INSTDIR\func\core
	File func\core\__init__.py
	File func\core\prsnj.py
	File func\core\config.py
	File func\core\chargen.py
	File func\core\export.py
	File func\core\intro.py
	File func\core\lang.py
	File func\core\viz.py

	SetOutPath $INSTDIR\func\gen
	File func\gen\__init__.py
	File func\gen\apts.py
	File func\gen\cars.py
	File func\gen\dotes.py
	File func\gen\habs.py
	File func\gen\iniciales.py
	File func\gen\objetos.py

	SetOutPath $INSTDIR\func\data
	File func\data\__init__.py
	File func\data\campaign.json
	File func\data\setup.py

SectionEnd

SectionGroup "Idiomas"

	Section "Idioma Español"

	SetOutPath $INSTDIR\func\data\es

		File func\data\es\apts.json
		File func\data\es\armas.json
		File func\data\es\armds.json
		File func\data\es\clases.json
		File func\data\es\conjuros.json
		File func\data\es\dominios.json
		File func\data\es\dotes.json
		File func\data\es\escuelas.json
		File func\data\es\habs.json
		File func\data\es\idiomas.json
		File func\data\es\objmag.json
		File func\data\es\razas.json
		File func\data\es\nombre.txt

	SectionEnd

	Section "Idioma Inglés"

		setOutPath $INSTDIR\func\data\en
		File func\data\en\apts.json
		File func\data\en\armas.json
		File func\data\en\armds.json
		File func\data\en\clases.json
		File func\data\en\conjuros.json
		File func\data\en\dominios.json
		File func\data\en\dotes.json
		File func\data\en\escuelas.json
		File func\data\en\habs.json
		File func\data\en\idiomas.json
		File func\data\en\objmag.json
		File func\data\en\razas.json
		File func\data\en\nombre.txt

	SectionEnd

SectionGroupEnd

Section "Uninstall"
	Delete $INSTDIR\Uninst.exe ; delete self
	RMDir /r $INSTDIR
SectionEnd