from pydantic import BaseModel
from enum import Enum
class III_IREnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class IV_SUP_OBLIQUEEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class V_MASSETEREnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class VI_LATEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class VII_FRONTALSEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class VII_ZYGOMATICEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class VII_ORBEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class VII_BUCCALEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class VII_MANDIBULAREnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class VII_MENTALISEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class VII_CERVICALEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class VII_PLATYSMAEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class CIX_STYLOEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class X_VCOCALISEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class XI_SCMEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class XII_TONGUEEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class OTHEREnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'

class Case_setup_CranialMuscles_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	III_IR:III_IREnum 
	IV_SUP_OBLIQUE:IV_SUP_OBLIQUEEnum 
	V_MASSETER:V_MASSETEREnum 
	VI_LAT:VI_LATEnum 
	VII_FRONTALS:VII_FRONTALSEnum 
	VII_ZYGOMATIC:VII_ZYGOMATICEnum 
	VII_ORB:VII_ORBEnum 
	VII_BUCCAL:VII_BUCCALEnum 
	VII_MANDIBULAR:VII_MANDIBULAREnum 
	VII_MENTALIS:VII_MENTALISEnum 
	VII_CERVICAL:VII_CERVICALEnum 
	VII_PLATYSMA:VII_PLATYSMAEnum 
	CIX_STYLO:CIX_STYLOEnum 
	X_VCOCALIS:X_VCOCALISEnum 
	XI_SCM:XI_SCMEnum 
	XII_TONGUE:XII_TONGUEEnum 
	OTHER:OTHEREnum 


class Case_setup_CranialMuscles_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	III_IR:III_IREnum  = ''
	IV_SUP_OBLIQUE:IV_SUP_OBLIQUEEnum  = ''
	V_MASSETER:V_MASSETEREnum  = ''
	VI_LAT:VI_LATEnum  = ''
	VII_FRONTALS:VII_FRONTALSEnum  = ''
	VII_ZYGOMATIC:VII_ZYGOMATICEnum  = ''
	VII_ORB:VII_ORBEnum  = ''
	VII_BUCCAL:VII_BUCCALEnum  = ''
	VII_MANDIBULAR:VII_MANDIBULAREnum  = ''
	VII_MENTALIS:VII_MENTALISEnum  = ''
	VII_CERVICAL:VII_CERVICALEnum  = ''
	VII_PLATYSMA:VII_PLATYSMAEnum  = ''
	CIX_STYLO:CIX_STYLOEnum  = ''
	X_VCOCALIS:X_VCOCALISEnum  = ''
	XI_SCM:XI_SCMEnum  = ''
	XII_TONGUE:XII_TONGUEEnum  = ''
	OTHER:OTHEREnum  = ''


class Case_setup_EEG_channels_INSERT(BaseModel):
	patient_id:int 
	id:int  = 0
	pre_set_EEG:str 
	Input_positive:str 
	Input_negative:str 


class Case_setup_EEG_channels_UPDATE(BaseModel):
	patient_id:int  = 0
	id:int  = 0
	pre_set_EEG:str  = ''
	Input_positive:str  = ''
	Input_negative:str  = ''


class TrapEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class DELTOIDEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class BICEPEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class BREnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class TRICEPSEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class FCR_FCUEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class HANDEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class PSOASEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class ADDUCTOREnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class QUADSEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class EHLEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class TAEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class HAMSTRINGEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class GASTROCEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class FOOTEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class INTERCOSTALEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class ABSEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class U_ABSEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class L_ABSEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class RLNEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class AN_SPHEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class OTHER1Enum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class OTHER2Enum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'

class Case_setup_EMG_Muscles_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	Trap:TrapEnum 
	DELTOID:DELTOIDEnum 
	BICEP:BICEPEnum 
	BR:BREnum 
	TRICEPS:TRICEPSEnum 
	FCR_FCU:FCR_FCUEnum 
	HAND:HANDEnum 
	PSOAS:PSOASEnum 
	ADDUCTOR:ADDUCTOREnum 
	QUADS:QUADSEnum 
	EHL:EHLEnum 
	TA:TAEnum 
	HAMSTRING:HAMSTRINGEnum 
	GASTROC:GASTROCEnum 
	FOOT:FOOTEnum 
	INTERCOSTAL:INTERCOSTALEnum 
	ABS:ABSEnum 
	U_ABS:U_ABSEnum 
	L_ABS:L_ABSEnum 
	RLN:RLNEnum 
	AN_SPH:AN_SPHEnum 
	OTHER1:OTHER1Enum 
	OTHER2:OTHER2Enum 


class Case_setup_EMG_Muscles_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	Trap:TrapEnum  = ''
	DELTOID:DELTOIDEnum  = ''
	BICEP:BICEPEnum  = ''
	BR:BREnum  = ''
	TRICEPS:TRICEPSEnum  = ''
	FCR_FCU:FCR_FCUEnum  = ''
	HAND:HANDEnum  = ''
	PSOAS:PSOASEnum  = ''
	ADDUCTOR:ADDUCTOREnum  = ''
	QUADS:QUADSEnum  = ''
	EHL:EHLEnum  = ''
	TA:TAEnum  = ''
	HAMSTRING:HAMSTRINGEnum  = ''
	GASTROC:GASTROCEnum  = ''
	FOOT:FOOTEnum  = ''
	INTERCOSTAL:INTERCOSTALEnum  = ''
	ABS:ABSEnum  = ''
	U_ABS:U_ABSEnum  = ''
	L_ABS:L_ABSEnum  = ''
	RLN:RLNEnum  = ''
	AN_SPH:AN_SPHEnum  = ''
	OTHER1:OTHER1Enum  = ''
	OTHER2:OTHER2Enum  = ''


class TrapEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class DELTOIDEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class BICEPEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class BREnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class TRICEPSEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class FCR_FCUEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class HANDEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class PSOASEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class ADDUCTOREnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class QUADSEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class EHLEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class TAEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class HAMSTRINGEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class GASTROCEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class FOOTEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class INTERCOSTALEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class ABSEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class U_ABSEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class L_ABSEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class RLNEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class AN_SPHEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class OTHER1Enum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class OTHER2Enum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'

class Case_setup_MEP_Muscles_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	Trap:TrapEnum 
	DELTOID:DELTOIDEnum 
	BICEP:BICEPEnum 
	BR:BREnum 
	TRICEPS:TRICEPSEnum 
	FCR_FCU:FCR_FCUEnum 
	HAND:HANDEnum 
	PSOAS:PSOASEnum 
	ADDUCTOR:ADDUCTOREnum 
	QUADS:QUADSEnum 
	EHL:EHLEnum 
	TA:TAEnum 
	HAMSTRING:HAMSTRINGEnum 
	GASTROC:GASTROCEnum 
	FOOT:FOOTEnum 
	INTERCOSTAL:INTERCOSTALEnum 
	ABS:ABSEnum 
	U_ABS:U_ABSEnum 
	L_ABS:L_ABSEnum 
	RLN:RLNEnum 
	AN_SPH:AN_SPHEnum 
	OTHER1:OTHER1Enum 
	OTHER2:OTHER2Enum 


class Case_setup_MEP_Muscles_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	Trap:TrapEnum  = ''
	DELTOID:DELTOIDEnum  = ''
	BICEP:BICEPEnum  = ''
	BR:BREnum  = ''
	TRICEPS:TRICEPSEnum  = ''
	FCR_FCU:FCR_FCUEnum  = ''
	HAND:HANDEnum  = ''
	PSOAS:PSOASEnum  = ''
	ADDUCTOR:ADDUCTOREnum  = ''
	QUADS:QUADSEnum  = ''
	EHL:EHLEnum  = ''
	TA:TAEnum  = ''
	HAMSTRING:HAMSTRINGEnum  = ''
	GASTROC:GASTROCEnum  = ''
	FOOT:FOOTEnum  = ''
	INTERCOSTAL:INTERCOSTALEnum  = ''
	ABS:ABSEnum  = ''
	U_ABS:U_ABSEnum  = ''
	L_ABS:L_ABSEnum  = ''
	RLN:RLNEnum  = ''
	AN_SPH:AN_SPHEnum  = ''
	OTHER1:OTHER1Enum  = ''
	OTHER2:OTHER2Enum  = ''


class Case_setup_Modalties_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	EEG:int 
	ECOG:int 
	EMG:int 
	MEP:int 
	SSEP:int 
	T04:int 
	Trig_EMG:int 
	CN_EMG:int 
	Others:int 


class Case_setup_Modalties_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	EEG:int  = 0
	ECOG:int  = 0
	EMG:int  = 0
	MEP:int  = 0
	SSEP:int  = 0
	T04:int  = 0
	Trig_EMG:int  = 0
	CN_EMG:int  = 0
	Others:int  = 0


class UlnarEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class MedianEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class ErbsEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class PTNEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class FibularEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class SaphaneousEnum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class Other1Enum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'


class Other2Enum(str,Enum):
	left = 'left'
	right = 'right'
	bilateral = 'bilateral'

class Case_setup_SSEP_Nerves_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	Ulnar:UlnarEnum 
	Median:MedianEnum 
	Erbs:ErbsEnum 
	PTN:PTNEnum 
	Fibular:FibularEnum 
	Saphaneous:SaphaneousEnum 
	Other1:Other1Enum 
	Other2:Other2Enum 


class Case_setup_SSEP_Nerves_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	Ulnar:UlnarEnum  = ''
	Median:MedianEnum  = ''
	Erbs:ErbsEnum  = ''
	PTN:PTNEnum  = ''
	Fibular:FibularEnum  = ''
	Saphaneous:SaphaneousEnum  = ''
	Other1:Other1Enum  = ''
	Other2:Other2Enum  = ''


class Case_setup_SSEP_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	Neck_Electrode:str 
	Upper_Cortical:int 
	Upper_Subcortical:int 
	ERBS:int 
	Lower_Cortical:int 
	Lower_Subcortical:int 
	Pops:int 


class Case_setup_SSEP_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	Neck_Electrode:str  = ''
	Upper_Cortical:int  = 0
	Upper_Subcortical:int  = 0
	ERBS:int  = 0
	Lower_Cortical:int  = 0
	Lower_Subcortical:int  = 0
	Pops:int  = 0


class Case_setup_mep_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	bi_pole:int  = 0
	quad:int  = 0
	MEP_montage:int  = 0
	Active:str 
	Ref:str 


class Case_setup_mep_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	bi_pole:int  = 0
	quad:int  = 0
	MEP_montage:int  = 0
	Active:str  = ''
	Ref:str  = ''


class Case_setup_trig_emg_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	pedicle_screw:int 
	direct_nerve_stim:int 
	guidance:int 
	other:int 
	place_ground:str 
	proble_type:str 


class Case_setup_trig_emg_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	pedicle_screw:int  = 0
	direct_nerve_stim:int  = 0
	guidance:int  = 0
	other:int  = 0
	place_ground:str  = ''
	proble_type:str  = ''


class PatientInfo_extension_INSERT(BaseModel):
	EMR_ID:int  = 0
	patient_id:int 
	Procedure_Name:str 
	Hospital:str 
	Date_of_Service:str 
	Start_Time:str 
	Duration:str 
	Anesthesiologist:str 
	Reader:str 
	SNP1:str 
	SNP2:str 
	Surgeon:str 


class PatientInfo_extension_UPDATE(BaseModel):
	EMR_ID:int  = 0
	patient_id:int  = 0
	Procedure_Name:str  = ''
	Hospital:str  = ''
	Date_of_Service:str  = ''
	Start_Time:str  = ''
	Duration:str  = ''
	Anesthesiologist:str  = ''
	Reader:str  = ''
	SNP1:str  = ''
	SNP2:str  = ''
	Surgeon:str  = ''


class GenderEnum(str,Enum):
	Male = 'Male'
	Female = 'Female'
	Other = 'Other'


class InsuranceTypeEnum(str,Enum):
	Private = 'Private'
	Medicare = 'Medicare'
	Medicaid = 'Medicaid'
	VA = 'VA'

class PatientInfo_INSERT(BaseModel):
	patient_id:int  = 0
	FirstName:str 
	LastName:str 
	Gender:GenderEnum 
	DateOfBirth:str 
	Height:int 
	Weight:int 
	InsuranceType:InsuranceTypeEnum 
	PolicyNumber:str 
	MedicalRecord:str 
	HospitalRecord:str 


class PatientInfo_UPDATE(BaseModel):
	patient_id:int  = 0
	FirstName:str  = ''
	LastName:str  = ''
	Gender:GenderEnum  = ''
	DateOfBirth:str  = ''
	Height:int  = 0
	Weight:int  = 0
	InsuranceType:InsuranceTypeEnum  = ''
	PolicyNumber:str  = ''
	MedicalRecord:str  = ''
	HospitalRecord:str  = ''


class medical_history_Autonomic_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	bowel_bladder_changes:int  = 0
	discoloration:int  = 0
	burning_pain:int  = 0
	swollen_skin:int  = 0


class medical_history_Autonomic_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	bowel_bladder_changes:int  = 0
	discoloration:int  = 0
	burning_pain:int  = 0
	swollen_skin:int  = 0


class medical_history_CoMorbidities_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	diabetes:int  = 0
	hypertension:int  = 0
	stroke:int  = 0
	seizure:int  = 0
	vascular_disease:int  = 0
	other:str 


class medical_history_CoMorbidities_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	diabetes:int  = 0
	hypertension:int  = 0
	stroke:int  = 0
	seizure:int  = 0
	vascular_disease:int  = 0
	other:str  = ''


class medical_history_Diagnosis_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	code:str 
	diagnosis:str 
	notes:str 


class medical_history_Diagnosis_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	code:str  = ''
	diagnosis:str  = ''
	notes:str  = ''


class medical_history_Implants_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	implant_name:str 
	date_placed:str 
	dos:str 
	notes:str 


class medical_history_Implants_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	implant_name:str  = ''
	date_placed:str  = ''
	dos:str  = ''
	notes:str  = ''


class medical_history_MotorFunction_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	frequent_falls:int  = 0
	difficulty_getting_out_of_bed:int  = 0
	trouble_walking:int  = 0
	poor_balance:int  = 0
	other:str 


class medical_history_MotorFunction_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	frequent_falls:int  = 0
	difficulty_getting_out_of_bed:int  = 0
	trouble_walking:int  = 0
	poor_balance:int  = 0
	other:str  = ''


class medical_history_Note_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	note:str 


class medical_history_Note_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	note:str  = ''


class medical_history_Seizures_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	seizures_status:int  = 0
	note:str 


class medical_history_Seizures_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	seizures_status:int  = 0
	note:str  = ''


class medical_history_Surgeries_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	procedure_name:str 
	type:str 
	dos:str 
	notes:str 


class medical_history_Surgeries_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	procedure_name:str  = ''
	type:str  = ''
	dos:str  = ''
	notes:str  = ''


class medical_history_Symptoms_INSERT(BaseModel):
	id:int  = 0
	patient_id:int 
	symptom:str 
	side:str 
	area:str 
	source:str 
	action:str 


class medical_history_Symptoms_UPDATE(BaseModel):
	id:int  = 0
	patient_id:int  = 0
	symptom:str  = ''
	side:str  = ''
	area:str  = ''
	source:str  = ''
	action:str  = ''

