def classify_document(text):
    text = text.lower()

    if any(keyword in text for keyword in ["resume", "curriculum vitae", "education", "skills", "experience"]):
        return "Resume"
    elif any(keyword in text for keyword in ["invoice", "invoice no", "total", "amount due", "bill to"]):
        return "Invoice"
    elif any(keyword in text for keyword in ["prescription", "diagnosis", "patient", "doctor", "medical", "dr.", "rx", "tablet", "diagnosis", "morning/evening"]):
        return "Medical"
    else:
        return "Others"
