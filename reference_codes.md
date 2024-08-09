Old Retrieval Code

```Python
 Function to run the conversation with memory
 def run_chain_select(input_text):
     # Load the current conversation history
     history = memory_select.load_memory_variables({}).get(
         "history", "No prior conversation history."
     )

     def query_refiner(conversation, query):
         client = OpenAI()
         response = client.chat.completions.create(
             model="gpt-4o",
             messages=[
                 {
                     "role": "system",
                     "content": f"Given the following user query and conversation log,if the conversation log does not have a prior history keep the query as it is. Else formulate the most relevant question to provide the user with an answer from data base\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
                 }
             ],
             temperature=0,
             max_tokens=256,
             top_p=1,
             frequency_penalty=0,
             presence_penalty=0,
         )
         return response.choices[0].message.content

     refined_query = query_refiner(history, input_text)

     # logger.debug("refined query:",refined_query)
     # Create the chain with memory handling
     @chain
     def debug(res):
         logger.debug(res["question"])
         logger.debug(res["query"])
         logger.debug(res["result"])
         return res

     select_chain = (
         RunnablePassthrough.assign(query=generate_query).assign(
             result=itemgetter("query") | execute_query
         )
         | debug
         | rephrase_answer
     )
     sequence_input = {
         "history": history,
         "question": refined_query,
         "table_names_to_use": [
             "medical_history_Autonomic",
             "medical_history_CoMorbidities",
             "medical_history_Diagnosis",
             "medical_history_Implants",
             "medical_history_MotorFunction",
             "medical_history_Note",
             "medical_history_Seizures",
             "medical_history_Surgeries",
             "medical_history_Symptoms",
             "PatientInfo",
             "PatientInfo_extension",
         ],
     }
     # sql_query = generate_query.invoke({"question": refined_query})
     # logger.debug("sql - ",sql_query)

     # Run the chain
     result = select_chain.invoke(sequence_input)

     # Save the new context to memory
     memory_select.save_context({"input": input_text}, {"output": result})

     return result
```
