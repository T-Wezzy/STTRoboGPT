from llama_index import SimpleDirectoryReader,GPTListIndex,GPTVectorStoreIndex,LLMPredictor,PromptHelper,ServiceContext,StorageContext,load_index_from_storage
from langchain import OpenAI
import sys
import os
import speech_recognition as sr
import time
import re
import winsound

os.environ["OPENAI_API_KEY"] = "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"


#=============================
# GPT response prep
def create_index(path):
    max_input = 4096
    tokens = 200
    chunk_size = 600 #for LLM, we need to define chunk size
    max_chunk_overlap = 20
    promptHelper = PromptHelper(max_input,tokens,max_chunk_overlap,chunk_size_limit=chunk_size)
    llmPredictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-babbage-001",max_tokens=tokens))
    # Load Data
    docs = SimpleDirectoryReader(path).load_data()
    # Create Vector Index
    service_context = ServiceContext.from_defaults(llm_predictor=llmPredictor, prompt_helper=promptHelper)
    vectorIndex = GPTVectorStoreIndex.from_documents(documents=docs, service_context=service_context)
    vectorIndex.storage_context.persist(persist_dir= 'indexStorage')
def gptAnswer(question):
    storage_context = StorageContext.from_defaults(persist_dir= 'indexStorage')
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    return response

#=============================

r = sr.Recognizer()

# speech recognition mic setup
with sr.Microphone() as mic:

    print("AI Started")
 
    while True:
 
        audio_data = r.listen(mic)

        # convert speech to text
        try:
            text = r.recognize_google(audio_data)

            # could maybe make a list in the future and have a For loop?
            subString1 = "hey Google"
            subString2 = "Google"

            # searches text string for listed subStrings
            if re.search(subString1, text):
                
                # plays activation sound
                winsound.PlaySound("AIActivate", winsound.SND_FILENAME)
                
                # listens for question
                audio_data = r.listen(mic)
 
                # convert speech to text
                question = r.recognize_google(audio_data)
                print(question)

                # gen GPT response
                create_index('context')
                response = gptAnswer(question)
                print(response)
                pass

            elif re.search(subString2, text): # same as one up there but for subString 2

                # plays activation sound
                winsound.PlaySound("AIActivate", winsound.SND_FILENAME)

                # listens for question
                audio_data = r.listen(mic)

                # convert speech to text
                question = r.recognize_google(audio_data)
                print(question)
 
                # gen GPT response
                create_index('context')
                response = gptAnswer(text)
                print(response)
                pass
            else:
                # does nothing because subString was not found
                print("")

        except:
            # substring / no speech to detect: loop
            pass



# Potentially faster method of detecting voice

#while True:
#    
#    try:
#        
#        with sr.Microphone() as mic:
#
#            r.adjust_for_ambient_noise(mic, duration=0.2)
#            audio = r.listen(mic)
#
#            text = r.recognize_google(audio)
#            text = text.lower()
#
#            print(f"Recognized {text}")
#    
#    except sr.UnknownValueError():
#
#        r = sr.Recognizer()
#        continue