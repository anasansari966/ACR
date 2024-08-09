# Inserting the Data

Steps Involved

- Prompt

- Check Clear Memory
- Rephrase Prompt
- Generate Query
- Extract info from query
- Validate the extracted Info
- Handle Validation Error If any
- from the non rephrased prompt check whether user suggests ‘ yes proceed’
- if not validation error and is proceed then run the query

Example :

Prompt

```
Add new Patient with name John Doe born on 12/12/2012 , 120CM , 65KG
```

Rephrased query

```
Add new Patient with name John Doe born on 12/12/2012 , 120CM , 65KG
```

Generated query

```sql
INSERT INTO PatientInfo( FirstName, LastName, DateOfBirth, Height, Weight)
VALUES('John','Doe','12-12-2012',120,65);
```

- Note that LLM is aware of SQL dateformat and forms query properly so there is no need of date format validation and also whenever in prompt we specify today,tomorrow than date the prompt generate will have SQL Date functions such as

```sql
CURRDATE() --gives current date i.e today
CURRDATE() + Interval 1 Day --gives tomorrow
```

- So that is why we keep the date columns type as string in python validation class

Extracted Data

```python
table_name = PatientInfo
provided_fields = [{'FirstName': 'John', 'LastName': 'Doe', 'DateOfBirth': '12-12-2012', 'Height': '120', 'Weight': '65'}]

validation_error = [
    {'Gender':'should be male , female or other'},

     {'InsuranceType', 'PolicyNumber', 'MedicalRecord', 'HospitalRecord' : 'required'}
]
```

So now as there are validation error we need to handle it
So the LLM will generate a message saying

```
Please can you provide me Gender, InsuranceType, PolicyNumber, MedicalRecord, HospitalRecord data?
```

This is the reply to the user's first prompt.

Now the user Replies by saying

```
Gender male , InsuranceType Private, PolicyNumber 1234, MedicalRecord 1234, HospitalRecord 1234
```

Rephrased Prompt

```
Add new Patient with name John Doe born on 12/12/2012 , 120CM , 65KG , Gender male , InsuranceType Private, PolicyNumber 1234, MedicalRecord 1234, HospitalRecord 1234
```

Generated SQL

```sql
INSERT INTO PatientInfo( FirstName, LastName, DateOfBirth, Height, Weight, Gender, InsuranceType, PolicyNumber, MedicalRecord, HospitalRecord)
VALUES('John','Doe','12-12-2012',120,65,'male','Private','1234','1234','1234');
```

Extracted Data

```python
table_name = PatientInfo
provided_fields = [{'FirstName': 'John', 'LastName': 'Doe', 'DateOfBirth': '12-12-2012', 'Height': '120', 'Weight': '65'},{'Gender': 'male', 'InsuranceType': 'Private', 'PolicyNumber': '1234', 'MedicalRecord': '1234', 'HospitalRecord': '1234'}]

validation_error = []
```

Now the validation errors are zero now we have to see whether user asked to proceed in the prompt

```
Prompt : Gender male , InsuranceType Private, PolicyNumber 1234, MedicalRecord 1234, HospitalRecord 1234

which is not similar to 'yes proceed'
```

So user not saying to proceed , so LLM generates

```
First Name : John

Last Name : Doe

Date of Birth : 12-12-2012

Height : 120

Weight : 65

Gender : male

Insurance Type : Private

Policy Number : 1234

Medical Record : 1234

Hospital Record : 1234

These are the data provided Is this all right and do you want to proceed ?

```

This is the reply for second prompt

Then the use may change any data if they want or the use may say

```
yes proceed
```

Rephrased Prompt

```
Add new Patient with name John Doe born on 12/12/2012 , 120CM , 65KG , Gender male , InsuranceType Private, PolicyNumber 1234, MedicalRecord 1234, HospitalRecord 1234
```

Generated SQL

```sql
INSERT INTO PatientInfo( FirstName, LastName, DateOfBirth, Height, Weight, Gender, InsuranceType, PolicyNumber, MedicalRecord, HospitalRecord)
VALUES('John','Doe','12-12-2012',120,65,'male','Private','1234','1234','1234');
```

Extracted Data

```python
table_name = PatientInfo
provided_fields = [{'FirstName': 'John', 'LastName': 'Doe', 'DateOfBirth': '12-12-2012', 'Height': '120', 'Weight': '65'},{'Gender': 'male', 'InsuranceType': 'Private', 'PolicyNumber': '1234', 'MedicalRecord': '1234', 'HospitalRecord': '1234'}]

validation_error = []
```

No validation hence check for proceed prompt

```
Prompt : yes proceed
```

So the user asking for proceed so run the generated query

- If any SQL Error Generate generate a message explaining the error
- Else Generate a message saying 'Data got inserted Successfully

And then clear the chat history i.e memory.

# Updating the Data

The flow remains the same

# Restrictions

- For some tables we cant have same validation class for insert and update

      For Example for PatientInfo while inserting all fields are required but for updation he may provide only Height or weight and need not provide all fields so we cant keep all fields required but we have to validate the provided fields like height,weight greater should be number patient id is required

  ```
      So if we are making the Validation class generation automated this might not work properly or we have to handle this carefully
  ```
