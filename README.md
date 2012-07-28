Framingham 10 Year Heart Attack Risk Calculator
===============================================
(c.) Alan Viars - Videntity Systems Inc. - 2012

Version 0.1.1 - Apache 2 License.


Installation
------------

Use pip to install the parser.

    pip install python-framingham10yr


Using the Command Line Tool
---------------------------

This assumes you have a Python installed.  If you are on a Mac or Linux you
should be good to go.

Usage:

    > framingham.py <sex> <age> <total_cholesterol> <hdl_cholesterol systolic_blood_pressure> <smoker> <blood_pressure_med_treatment>

Example:

    > framingham.py male 25 152 56 130 0 0


Using the Library
-----------------

The library accepts the necessay input and returns a dictionary with the results
or errors. If the command is successful it will return with a status code of 200
and 422 if not. If you get an error, look in the errors list to see what you
got wrong.  If the command is successful, the risk is stored in "percent_risk".

    # Import the library
    >>> from framingham10yr.framingham10yr import framingham_10year_risk
    
    # enter valid values and calculate the risk.
    >>> result = framingham_10year_risk(sex="male", age=26, total_cholesterol=152, hdl_cholesterol=70,  systolic_blood_pressure=130, smoker=True, blood_pressure_med_treatment=False)
    >>> print type(result), result
        <type 'dict'> {'status': 200, 'systolic_blood_pressure': 130, 'total_cholesterol': 152, 'hdl_cholesterol': 70, 'percent_risk': '<1%', 'blood_pressure_med_treatment': False, 'message': 'OK', 'points': -1, 'age': 26, 'smoker': True}
