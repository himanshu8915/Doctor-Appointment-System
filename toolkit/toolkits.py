from typing import Literal
from langchain_core.tools import tool
from data_models.models import *
import pandas as pd
from pathlib import Path

@tool
def check_availability_by_doctor(desired_date:DateModel,doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Checking the database if we have availability for the specific doctor.
    The parameters should be mentioned by the user in the query
    """
    df=pd.read_csv(r"../data/doctor_availability.csv")

    df['date_slot_time']=df['date_slot'].apply(lambda input: input.split(' ')[-1])
    rows= list(df[(df['date_slot'].apply(lambda input:input.split(" ")[0])==desired_date.date)&(df['doctor_name']==doctor_name)&(df['is_available']==True)]['date_slot_time'])

    if len(rows)==0:
        output="No availability in the entire day"

    else:
        output=f'This availability for {desired_date.date}\n'
        output+="Availability Slots: "+ ','.join(rows)

    return output


@tool
def check_availability_by_specialization(desired_date:DateModel,specialization:Literal["general_dentist", "cosmetic_dentist", "prosthodontist", "pediatric_dentist","emergency_dentist","oral_surgeon","orthodontist"]):
    """
    checking the database if we have the availability for the specific specialization.
    The parameters should be mentioned by the user in the query
    """

    csv_path = r"../data/doctor_availability.csv"
    df=pd.read_csv(csv_path)

    df['date_slot_time']=df['date_slot'].apply(lambda input: input.split(" ")[-1])
    rows=df[(df['date_slot'].apply(lambda x:x.split(' ')[0])==desired_date.date)&(df['specialization']==specialization)&(df['is_available']==True)].groupby(['specialization','doctor_name'])['date_slot_time'].apply(list).reset_index(name='available_slots')

    if len(rows)==0:
        output="No availability in the entire day"

    else:
        def convert_to_am_pm(time_str):
           #split the time string into hourd and minutes
            time_Str=str(time_str)
            hours,minutes=map(int,time_Str.split(":"))

            #determine AM or PM
            period="AM" if hours <12 else "PM"

            #convert hours to 12-hour format
            hours=hours%12 or 12

            #format the output
            return f"{hours}:{minutes:02d} {period}"

        output=f"This availability for {desired_date.date}\n"
        for row in rows.values:
            output +=row[1] +".Available slots:\n" + ',\n'.join([convert_to_am_pm(value) for value in row[2]])+'\n'
    
    return output



@tool
def set_appointment(desired_date:DateTimeModel, id_number:IdentificationNumberModel,doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Set appointment or slot with the doctor
    The parameters MUST be mentioned by the user in the query
    """

    csv_path = r"../data/doctor_availability.csv"
    df=pd.read_csv(csv_path)

    case=df[(df['date_slot']==desired_date.date)&(df['doctor_name']==doctor_name)&(df['is_available']==True)]
    if len(case)==0:
        output="No availability for that particular case"
        return output
    else:
        df.loc[(df['date_slot'] == desired_date.date)&(df['doctor_name'] == doctor_name) & (df['is_available'] == True), ['is_available','patient_to_attend']] = [False, id_number.id]
        csv_path = r"../data/doctor_availability.csv"
        df.to_csv(csv_path, index=False)

        return "appointment scheduled successfully"


@tool
def cancel_appointment(date:DateTimeModel, id_number:IdentificationNumberModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Canceling an appointment.
    The parameters MUST be mentioned by the user in the query.
    """
    df = pd.read_csv(r"../data/doctor_availability.csv")
    case_to_remove = df[(df['date_slot'] == date.date)&(df['patient_to_attend'] == id_number.id)&(df['doctor_name'] == doctor_name)]
    if len(case_to_remove) == 0:
        return "You don´t have any appointment with that specifications"
    else:
        df.loc[(df['date_slot'] == date.date) & (df['patient_to_attend'] == id_number.id) & (df['doctor_name'] == doctor_name), ['is_available', 'patient_to_attend']] = [True, None]
        df.to_csv(f"../data/doctor_availability.csv", index = False)

        return "Successfully cancelled"
        
@tool
def reschedule_appointment(old_date:DateTimeModel,new_date:DateTimeModel,id_number:IdentificationNumberModel,doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Reschedule  an appointment.
    The parameters MUST be Mentioned by the user in the query.
    """     

    csv_path = r"../doctor_availability.csv"
    df=pd.read_csv(csv_path)
    available_for_desired_date=df[(df['date_slot']==new_date.date)&(df['is_available']==True)&(df['doctor_name']==doctor_name)] 

    if len(available_for_desired_date)==0:
     return "Not available slots in the desired period"
    else:
        cancel_appointment.invoke({"date":old_date,"id_number":id_number,"doctor_name":doctor_name})
        set_appointment.invoke({"desired_date":new_date,"id_number":id_number,"doctor_name":doctor_name})

        return "Successfully rescheduled for the desired date." 



# class AppointmentToolkit:
#     @staticmethod
#     def get_tools():
#         return [check_availability_by_doctor,check_availability_by_specialization,set_appointment,cancel_appointment,reschedule_appointment]
