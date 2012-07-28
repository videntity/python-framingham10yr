Framingham 10 Year Heart Attack Risk Calculator
===============================================
(c.) Alan Viars - Videntity Systems Inc. - 2012

Version 0.1.1 - Apache 2 License.


Installation
------------

Use pip to install the the library and command line tool.

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
and 422 if there is an error. If you get an error, look in the errors list
returned in the response to see what you got wrong.  If the command is
successful, the risk is stored in "percent_risk".

    # Import the library
    >>> from framingham10yr.framingham10yr import framingham_10year_risk
    
    # enter valid values and calculate the risk.
    >>> result = framingham_10year_risk(sex="male", age=26, total_cholesterol=152, hdl_cholesterol=70,  systolic_blood_pressure=130, smoker=True, blood_pressure_med_treatment=False)
    >>> print result["status"], result["message"]
    200 OK
    >>> print type(result), result
        <type 'dict'> {'status': 200, 'systolic_blood_pressure': 130, 'total_cholesterol': 152, 'hdl_cholesterol': 70, 'percent_risk': '<1%', 'blood_pressure_med_treatment': False, 'message': 'OK', 'points': -1, 'age': 26, 'smoker': True}

Detecting Errors

    >>> result = framingham_10year_risk(sex="male-to-female-transgender", age=16, total_cholesterol=500, hdl_cholesterol=300,  systolic_blood_pressure=20, smoker="foo", blood_pressure_med_treatment="bar")
    >>> print result["status"], result["message"]
    422 The request contained errors and was unable to process.
    >>> print result['errors']
    ['Blood pressure medication treatment must be set to True, False, 1 or 0.',
        'Smoker must be set to True, False, 1, or 0.',
        'Age must be within the range of 20 to 79.',
        'Total cholesterol must be within the range of 130 to 320.',
        'HDL cholesterol must be within the range of 20 to 100.',
        'Systolic blood pressure must be within the range of 90 to 200.',
        'Sex must be male or female.']
        ]
        