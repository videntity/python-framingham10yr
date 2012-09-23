#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=

# Copyright Videnty Systems Inc, 2012 videntity.com
# Apache 2 License


import sys, json


GENDER_CHOICES = (('MALE', 'MALE'), 
                 ('FEMALE', 'FEMALE'),)

SMOKER_CHOICES = ((True, 'Yes'), 
                 (False, 'No'),)

def framingham_10year_risk(sex, age, total_cholesterol, hdl_cholesterol,
                           systolic_blood_pressure, smoker,
                           blood_pressure_med_treatment):
    """Requires:
        sex                             - "male" or "female" string
        age                             - string or int
        total_cholesterol               - sting or int 
        hdl_cholesterol                 - int
        systolic_blood_pressure         - int
        smoker                          - True or False. Also accepts 1 or 0 as
                                          a string or an int
        blood_pressure_med_treatment    - True or False. Also accepts 1 or 0
                                          as a string or an int
    """
    
    #be liberal in what we accept...massage the input
    if sex in ("MALE", "m", "M", "boy", "xy", "male", "Male"):
        sex = "male"
    if sex in ("FEMALE", "f", "F", "girl", "xx", "female", "Female"):
        sex = "female"    
    
    if smoker in ("true", "t", "True", True, 1, "1"):
        smoker=True
    if smoker in ("false", "f", "False", False, 0, "0"):
        smoker=False
    if  blood_pressure_med_treatment in ("true", "t", "True", True, 1, "1"):
        blood_pressure_med_treatment = True
    if  blood_pressure_med_treatment  in ("false", "f", "False", False, 0, "0"):
        blood_pressure_med_treatment = False

    #intialize some things -----------------------------------------------------
    errors = [] #a list of errors
    points = 0 
    age = int(age)
    total_cholesterol = int(total_cholesterol)
    hdl_cholesterol = int(hdl_cholesterol)
    systolic_blood_pressure = int(systolic_blood_pressure)
    
    try:
        blood_pressure_med_treatment = bool(int(blood_pressure_med_treatment))
    except(ValueError):
        errors.append("Blood pressure medication treatment must be set to True, False, 1 or 0.")
    
    try:
        smoker = bool(int(smoker))
    except(ValueError):
        errors.append("Smoker must be set to True, False, 1, or 0.")
        
    
    # Intitalize our response dictionary
    response = {"status": 200,
                "sex":sex,
                "message": "OK",
                "age": age,
                "total_cholesterol": total_cholesterol,  
                "hdl_cholesterol" : hdl_cholesterol,
                "systolic_blood_pressure": systolic_blood_pressure,
                "smoker": smoker,
                "blood_pressure_med_treatment": blood_pressure_med_treatment,
                }
    
    
    #run some sanity checks ----------------------------------------------------
    if not 20 <= age <=79:
        errors.append("Age must be within the range of 20 to 79.")
    
    if not 130 <= total_cholesterol <= 320:
        errors.append("Total cholesterol must be within the range of 130 to 320.")
    
    if not 20 <= hdl_cholesterol <= 100:
        errors.append("HDL cholesterol must be within the range of 20 to 100.")
    
    if not 90 <= systolic_blood_pressure<= 200:
        errors.append("Systolic blood pressure must be within the range of 90 to 200.")
    
    if sex.lower() not in ('male', 'female'):
        errors.append("Sex must be male or female.")

    #Process males -----------------------------------------------------------
    if sex.lower()=="male":

        # Age - male        
        if  20 <= age <= 34:
            points-=9
        if  35 <= age <= 39:
            points-=4
        if  40 <= age <= 44:
            points-=0
        if  45 <= age <= 49:
            points+=3
        if  50 <= age <= 54:
            points+=6
        if  55 <= age <= 59:
            points+=8
        if  60 <= age <= 64:
            points+=10
        if  65 <= age <= 69:
            points+=12
        if  70 <= age <= 74:
            points+=14
        if  75 <= age <= 79:
            points+=16

        #Total cholesterol, mg/dL - Male ------------------------
        if  20 <= age <= 39:
            if total_cholesterol < 160:
                points +=0
            if 160 <= total_cholesterol <= 199:
                points+=4
            if 200 <= total_cholesterol <= 239:
                points+=7
            if 240 <= total_cholesterol <= 279:
                points+=9
            if total_cholesterol > 289:
                points+=11
        if  40 <= age <= 49:
            if total_cholesterol < 160:
                points +=0
            if 160 <= total_cholesterol <= 199:
                points+=3
            if 200 <= total_cholesterol <= 239:
                points+=5
            if 240 <= total_cholesterol <= 279:
                points+=6
            if total_cholesterol > 289:
                points+=8
        if  50 <= age <= 59:
            if total_cholesterol < 160:
                points +=0
            if 160 <= total_cholesterol <= 199:
                points+=2
            if 200 <= total_cholesterol <= 239:
                points+=3
            if 240 <= total_cholesterol <= 279:
                points+=4
            if total_cholesterol > 289:
                points+=5
        if  60 <= age <= 69:
            if total_cholesterol < 160:
                points +=0
            if 160 <= total_cholesterol <= 199:
                points+=1
            if 200 <= total_cholesterol <= 239:
                points+=1
            if 240 <= total_cholesterol <= 279:
                points+=2
            if total_cholesterol > 289:
                points+=3
        if  70 <= age <= 79:
            if total_cholesterol < 160:
                points +=0
            if 160 <= total_cholesterol <= 199:
                points+=0
            if 200 <= total_cholesterol <= 239:
                points+=0
            if 240 <= total_cholesterol <= 279:
                points+=1
            if total_cholesterol > 289:
                points+=1
        #smoking - male
        if smoker:
            if 20 <= age <= 39:
               points+=8 
            if 40 <= age <= 49:
               points+=5
            if 50 <= age <= 59:
               points+=3
            if 60 <= age <= 69:
               points+=1
            if 70 <= age <= 79:
               points+=1 
        else: # nonsmoker
            points += 0
         
        #hdl cholesterol
        if hdl_cholesterol > 60:
            points-=1
        if 50 <= hdl_cholesterol <= 59:
            points+=0
        if 40 <= hdl_cholesterol <= 49:
            points+=1
        if hdl_cholesterol < 40:
            points+=2
            
        #systolic blood pressure
        if not blood_pressure_med_treatment:
            if systolic_blood_pressure < 120:
                points+=0
            if 120 <= systolic_blood_pressure <= 129:
                points+=0
            if 130 <= systolic_blood_pressure <= 139:
                points+=1           
            if 140 <= systolic_blood_pressure <= 159:
                points+=1
            if systolic_blood_pressure >= 160:
                points +=2
        else: #if the patient is on blood pressure meds
            if systolic_blood_pressure < 120:
                points+=0
            if 120 <= systolic_blood_pressure <= 129:
                points+=1
            if 130 <= systolic_blood_pressure <= 139:
                points+=1           
            if 140 <= systolic_blood_pressure <= 159:
                points+=2
            if systolic_blood_pressure >= 160:
                points +=3
        
        #calulate % risk for males
        if points <= 0:
            percent_risk ="<1%"
        elif points == 1:
            percent_risk ="1%"
        
        elif points == 2:
            percent_risk ="1%"
            
        elif points == 3:
            percent_risk ="1%"
            
        elif points == 4:
            percent_risk ="1%"
            
        elif points == 5:
            percent_risk ="2%"
            
        elif points == 6:
            percent_risk ="2%"
            
        elif points == 7:
            percent_risk ="2%"
            
        elif points == 8:
            percent_risk ="2%"
            
        elif points == 9:
            percent_risk ="5%"
            
        elif points == 10:
            percent_risk ="6%"
            
        elif points == 11:
            percent_risk ="8%"
            
        elif points == 12:
            percent_risk ="10%"
            
        elif points == 13:
            percent_risk ="12%"

        elif points == 14:
            percent_risk ="16%"
            
        elif points == 15:
            percent_risk ="20%"
            
        elif points == 16:
            percent_risk ="25%"
            
        elif points >= 17:
            percent_risk =">30%"
            
    #process females ----------------------------------------------------------
    elif sex.lower()=="female":
        # Age - female        
        if  20 <= age <= 34:
            points-=7
        if  35 <= age <= 39:
            points-=3
        if  40 <= age <= 44:
            points-=0
        if  45 <= age <= 49:
            points+=3
        if  50 <= age <= 54:
            points+=6
        if  55 <= age <= 59:
            points+=8
        if  60 <= age <= 64:
            points+=10
        if  65 <= age <= 69:
            points+=12
        if  70 <= age <= 74:
            points+=14
        if  75 <= age <= 79:
            points+=16

        #Total cholesterol, mg/dL - Female ------------------------
        if  20 <= age <= 39:
            if total_cholesterol < 160:
                points +=0
            if 160 <= total_cholesterol <= 199:
                points+=4
            if 200 <= total_cholesterol <= 239:
                points+=8
            if 240 <= total_cholesterol <= 279:
                points+=11
            if total_cholesterol > 289:
                points+=13
        if  40 <= age <= 49:
            if total_cholesterol < 160:
                points +=0
            if 160 <= total_cholesterol <= 199:
                points+=3
            if 200 <= total_cholesterol <= 239:
                points+=6
            if 240 <= total_cholesterol <= 279:
                points+=8
            if total_cholesterol > 289:
                points+=10
        if  50 <= age <= 59:
            if total_cholesterol < 160:
                points +=0
            if 160 <= total_cholesterol <= 199:
                points+=2
            if 200 <= total_cholesterol <= 239:
                points+=4
            if 240 <= total_cholesterol <= 279:
                points+=5
            if total_cholesterol > 289:
                points+=7
        if  60 <= age <= 69:
            if total_cholesterol < 160:
                points +=0
            if 160 <= total_cholesterol <= 199:
                points+=1
            if 200 <= total_cholesterol <= 239:
                points+=2
            if 240 <= total_cholesterol <= 279:
                points+=3
            if total_cholesterol > 289:
                points+=4
        if  70 <= age <= 79:
            if total_cholesterol < 160:
                points +=0
            if 160 <= total_cholesterol <= 199:
                points+=1
            if 200 <= total_cholesterol <= 239:
                points+=1
            if 240 <= total_cholesterol <= 279:
                points+=2
            if total_cholesterol > 289:
                points+=2
        #smoking - female
        if smoker:
            if 20 <= age <= 39:
               points+=9 
            if 40 <= age <= 49:
               points+=7
            if 50 <= age <= 59:
               points+=4
            if 60 <= age <= 69:
               points+=2
            if 70 <= age <= 79:
               points+=1 
        else: #nonsmoker
            points += 0
         
        #hdl cholesterol - female
        if hdl_cholesterol > 60:
            points-=1
        if 50 <= hdl_cholesterol <= 59:
            points+=0
        if 40 <= hdl_cholesterol <= 49:
            points+=1
        if hdl_cholesterol < 40:
            points+=2
            
        #systolic blood pressure
        if not blood_pressure_med_treatment: #untreated
            if systolic_blood_pressure < 120:
                points+=0
            if 120 <= systolic_blood_pressure <= 129:
                points+=1
            if 130 <= systolic_blood_pressure <= 139:
                points+=2           
            if 140 <= systolic_blood_pressure <= 159:
                points+=3
            if systolic_blood_pressure >= 160:
                points +=4
        else: #if the patient is on blood pressure meds
            if systolic_blood_pressure < 120:
                points+=0
            if 120 <= systolic_blood_pressure <= 129:
                points+=3
            if 130 <= systolic_blood_pressure <= 139:
                points+=4           
            if 140 <= systolic_blood_pressure <= 159:
                points+=5
            if systolic_blood_pressure >= 160:
                points +=6
        
        #calulate % risk for females
        if points <= 9:
            percent_risk ="<1%"
        elif 9 <= points <= 12:
            percent_risk ="1%"
        
        elif 13 <= points <= 14:
            percent_risk ="2%"
            
        elif points == 15:
            percent_risk ="3%"
            

        elif points == 16:
            percent_risk ="4%"
            
        elif points == 17:
            percent_risk ="5%"
            
        elif points == 18:
            percent_risk ="6%"

        elif points == 19:
            percent_risk ="8%"
            
        elif points == 20:
            percent_risk ="11%"
            
        elif points == 21:
            percent_risk ="14%"
            
        elif points == 22:
            percent_risk ="17%"

        elif points == 23:
            percent_risk ="22%"
            
        elif points == 24:
            percent_risk ="27%"
            
        elif points >= 25:
            percent_risk ="30%"

    if errors:
        response['status']=422
        response['message'] = "The request contained errors and was unable to process."
        response['errors']=errors
    else:
        response['points']=points
        
        
        
        
        
        
        
        
        response['percent_risk']= percent_risk
    
    return response


if __name__ == "__main__":    
    """
    Accept values to calucluate the 10 years heart attack risk based on
    Framingham.
    """
    try: 
        sex=sys.argv[1].lower()
        age=sys.argv[2]
        total_cholesterol=sys.argv[3]
        hdl_cholesterol=sys.argv[4]
        systolic_blood_pressure=sys.argv[5]
        smoker=sys.argv[6].lower()
        blood_pressure_med_treatment=sys.argv[7].lower()
        
    except(IndexError):
        print "All values are required."
        print "Usage: framingham.py <sex> <age> <total_cholesterol> <hdl_cholesterol systolic_blood_pressure> <smoker> <blood_pressure_med_treatment>"
        print "Example: framingham.py male 25 152 56 130 0 0"
        exit(1)
        
    try:
        
        #execute the function
        result = framingham_10year_risk(sex, age, total_cholesterol,
                                       hdl_cholesterol, systolic_blood_pressure,
                                       smoker, blood_pressure_med_treatment)
        
        #return pretty-print json to standard out
        print json.dumps(result, indent=4)
          
    except():
        print "An unexpected error occured. Here is the post-mortem:"
        print sys.exc_info()
        