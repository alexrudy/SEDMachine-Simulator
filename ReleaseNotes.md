# Release Notes
* 0.3.9
	- Renamed ``lenslets`` to ``objects`` for support module
	- Calibration lamps no longer undergo integration
* 0.3.8
	- Dotted configuration names.
* 0.3.7
	- Uses AstroObject 0.5 vocabulary
* 0.3.6
	- RCPipeline module using IRAF tools as an example pipeline entirley in python.
* 0.3.5
	- Fixes and upgrades to setuptools, as well as decorator based simulator
* 0.3.4
	- Fixes for installation, data and exports
* 0.3.3
	- Documentation and README
* 0.3.2
	- Improvements to SEDTools
* 0.3.1
	- Rename SEDSpec2 to SEDTools
	- Remove and re-include data files
	- Make SEDMsetup command
* 0.3.0
	- Simulator works for a variety of sources. Runs on the latest edition of the AstroObject module.
	- Documentation available from Sphinx Autodoc
	- Dependencies updated and run properly.
	- Simulator includes Calibration Source, Sky-only, flat, and simple-source modes.
* 0.2.0a1
	- This alpha is simply a port to the new simulator framework. Only the main simulator has been ported at this point.
	- All modules will now use the framework-based logging system. This still produces slightly odd results.
* 0.1.3p1,p2
	- Patch setup.py for AstroObject 0.2.8 rather than 0.2.6
	- Patch setup.py for Matplotlib 1.0 rather than 1.1
* 0.1.3
	- Use of setup.py for deployment and setup managment.
* 0.1.2
	- Documentation of Command Line Interface
	- Update to SED.py script
	- Separation of Instrument functions into SEDInstrument.py
	- Creation of SEDSource module to handle source manipulation
	- Cleanup of Nick's spectrum simulations in SEDSpec
	- Basic Utlity additions
* 0.1.1
	- Initial Basic Release
