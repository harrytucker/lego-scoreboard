:: ------------------------------------------------------------------------------------------------
:: Setup script for Lego Challenge site.
::
:: Experimental - may not work as advertised.
:: ------------------------------------------------------------------------------------------------

@ECHO Python and pip versions:
python --version
pip --version

@ECHO Installing dependencies via pip...
pip install pip --upgrade
pip install -r requirements

@ECHO Setting requirement environment variables...
set FLASK_APP=%cd%\lego\__init__.py
set FLASK_DEBUG=1

@ECHO Done
