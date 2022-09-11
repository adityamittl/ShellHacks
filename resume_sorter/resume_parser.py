def parseResume(filepath):
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.formrecognizer import DocumentAnalysisClient

    endpoint = "https://for-shellhacks.cognitiveservices.azure.com/"
    key = os.environ["KEY"]

    model_id = "resume-parser"

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    f =  open(filepath, "rb")

    poller = document_analysis_client.begin_analyze_document(model_id, f)
    result = poller.result()

    for idx, document in enumerate(result.documents):
        for name, field in document.fields.items():
            field_value = field.value if field.value else field.content
            return field_value

# print(parseResume("/home/kanak/Documents/Resumes/5_6332084895971542622.pdf"))