# Earnings Call Analysis

## Project Overview
This project implements an automated ETL (Extract, Transform, Load) pipeline for analyzing earnings call transcripts using Azure Cloud Services. The system uses Azure Functions with Blob trigger to automatically process earnings call transcripts when they are uploaded to Azure Blob Storage, extracting sentiment analysis and key insights using natural language processing.



The solution leverages several Azure services:
- **Azure Blob Storage**: Stores raw transcripts and processed analysis results
- **Azure Functions**: 
  - Blob-triggered function that automatically processes new transcript uploads
  - Serverless compute architecture for cost-effective scaling
- **Azure Language Service**: Natural Language Processing capabilities
- **Azure Monitor**: Monitoring and logging

## Features
- **Automated Processing**: 
  - Blob trigger automatically initiates transcript analysis when new files are uploaded
  - No manual intervention needed for processing
- Sentiment analysis using NLTK VADER
- JSON-formatted analysis output
- Scalable serverless architecture

## Prerequisites
- Python 3.8+
- Azure Subscription
- Azure Functions Core Tools
- Azure Storage Account
- Azure Language Service instance

## Local Development Setup
1. Clone the repository
```bash
git clone <repository-url>
cd Earnings-Call-Analysis
```

2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure local settings
- Copy `local.settings.json.example` to `local.settings.json`
- Update with your Azure Storage connection strings and other settings

## Configuration
The following environment variables need to be configured:
- `AzureWebJobsStorage`: Azure Storage connection string
- `LANGUAGE_ENDPOINT`: Azure Language Service endpoint
- `LANGUAGE_KEY`: Azure Language Service key

## Deployment
1. Deploy to Azure Functions:
```bash
func azure functionapp publish <your-function-app-name>
```

2. Configure the following in Azure:
- Create input and output blob containers
- Set up application settings
- Configure monitoring

## Usage
1. Upload transcript files to the `input-transcripts` container
2. Azure Function automatically processes new uploads
3. Analysis results are stored in the `output-analysis` container

## Project Structure
```
├── function_app.py        # Main Azure Function implementation
├── generate_samples.py    # Script to generate sample transcripts
├── requirements.txt       # Python dependencies
├── sample_transcripts/    # Sample transcript files
└── README.md             # Project documentation
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
