:: ------------------------------------------------------------------------------------------------
:: Setup script for Lego Challenge site.
:: ------------------------------------------------------------------------------------------------

@ECHO Installing dependencies via pip...
pip install pip --upgrade
pip install -r requirements

@ECHO Setting requirement environment variables...
set FLASK_APP=%cd%\lego\__init__.py
set FLASK_DEBUG=1

@ECHO Done
