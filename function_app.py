import azure.functions as func
import logging
from azure.storage.blob import BlobServiceClient
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from azure.core.credentials import AzureKeyCredential
import json
import os
from transformers import pipeline  



app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="input-transcripts/{name}",
                               connection="maqpocearningcalls_STORAGE") 
def AnalyzeEarningsCall(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
    try:
        # 1. Read the transcript from the uploaded blob
        transcript_text = myblob.read().decode('utf-8')
        logging.info(f"Blob content: {transcript_text[:50]}...")  # Log a snippet
        # 2. Initialize BERT keyword extraction pipeline
        keyword_extractor = pipeline("text2text-generation", model="facebook/bart-large-cnn")

        # 3. Extract keywords with BERT
        keywords_result = keyword_extractor(transcript_text, max_length=130, min_length=30)
        logging.info(f"Keywords extracted: {keywords_result}")
        keywords =  keywords_result[0].get("generated_text", []).split(",")  # Assuming the model returns a comma-separated string
        logging.info(f"Keywords: {keywords}")
        # 2. Initialize NLTK Sentiment Analyzer
        nltk.download('vader_lexicon')  # Download the VADER lexicon (only needs to be done once)
        sid = SentimentIntensityAnalyzer()

        # 3. Analyze sentiment with NLTK
        sentiment_scores = sid.polarity_scores(transcript_text)

        # Determine overall sentiment (simplified)
        if sentiment_scores['compound'] >= 0.05:
            overall_sentiment = 'Positive'
        elif sentiment_scores['compound'] <= -0.05:
            overall_sentiment = 'Negative'
        else:
            overall_sentiment = 'Neutral'

        # 4.  Process and format the results (create a JSON structure)
        analysis_results = {
            "sentiment": overall_sentiment,
            "confidence_scores": sentiment_scores,
            "key_phrases": keywords,  # NLTK doesn't provide key phrases directly
            "entities": [],     # NLTK doesn't provide entities directly
        }
        results_json = json.dumps(analysis_results, indent=2)
        logging.info(f"Analysis results: {results_json}")

        # 5. Store the JSON results in the output container
        output_container_name = "output-analysis"
        storage_account_connection_string = os.environ["AzureWebJobsStorage"]
        blob_service_client = BlobServiceClient.from_connection_string(storage_account_connection_string)
        output_blob_name = myblob.name.replace(".txt", "_analysis.json")
        output_blob_client = blob_service_client.get_blob_client(container=output_container_name, blob=output_blob_name)
        output_blob_client.upload_blob(results_json, overwrite=True)

        logging.info(f"Analysis results uploaded to {output_blob_name}")

    except Exception as e:
        logging.error(f"Error processing blob: {e}")
        raise
