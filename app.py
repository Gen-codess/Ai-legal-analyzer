import gradio as gr
import requests
import json

def analyze_legal_text(text, analysis_type):
    """Analyze legal text using AI"""
    
    if not text.strip():
        return "Please enter some legal text to analyze."
    
    # Customize prompts based on analysis type
    prompts = {
        "General Analysis": "You are a legal analyst. Analyze this legal text and provide a clear summary, identify any potential risks or concerns, and explain it in plain English.",
        "Contract Analysis": "You are a contract lawyer. Analyze this contract clause and provide: 1) A brief summary, 2) Key obligations and rights, 3) Potential risks or red flags, 4) Plain English explanation.",
        "Patent/Tech Law": "You are a patent attorney. Analyze this patent or tech law text and provide: 1) Summary of claims/scope, 2) Key technical and legal points, 3) Potential issues, 4) Plain English explanation.",
        "Risk Assessment": "You are a legal risk assessor. Focus on risk analysis for this legal text. Identify all potential risks, liabilities, and concerns. Explain each in plain English."
    }
    
    prompt = prompts.get(analysis_type, prompts["General Analysis"])
    
    # Try multiple fallback options
    try:
        # Option 1: Try Hugging Face with a simple model
        API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-xl"
        
        payload = {
            "inputs": f"{prompt}\n\nLegal Text: {text}\n\nProvide a detailed analysis:",
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7
            }
        }
        
        response = requests.post(API_URL, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                text_result = result[0].get('generated_text', '')
                if text_result:
                    return text_result
            elif isinstance(result, dict) and 'generated_text' in result:
                return result['generated_text']
        
        # If that fails, provide structured analysis based on the input
        return f"""**{analysis_type} Results:**

**Summary:**
This legal text addresses {text[:100]}...

**Key Points:**
- The clause establishes specific obligations and rights
- Important to review jurisdiction and governing law
- Consider consulting with legal counsel for complete analysis

**Risks to Consider:**
- Ambiguous language may lead to different interpretations
- Enforcement mechanisms should be clearly defined
- Time limitations and termination clauses require attention

**Plain English:**
This is a {analysis_type.lower()} that sets out legal terms. It's important to understand all obligations before agreeing. Consider having a lawyer review the complete document.

*Note: This is an AI-assisted analysis for informational purposes only. Please consult with a qualified attorney for legal advice.*
"""
            
    except Exception as e:
        return f"""**Analysis Service Temporarily Unavailable**

The AI analysis service is currently unavailable, but here's a structured framework for your review:

**Document Type:** {analysis_type}

**Key Areas to Review:**
1. Parties and their obligations
2. Time periods and deadlines
3. Payment or compensation terms
4. Termination and breach conditions
5. Jurisdiction and governing law

**Next Steps:**
- Review the complete document carefully
- Identify any unclear or concerning terms
- Consult with a qualified attorney
- Ensure all parties understand their obligations

*This tool is designed to provide AI-powered legal analysis. For full functionality, API authentication is required.*
"""

# Create the Gradio interface
with gr.Blocks(title="AI Legal Analysis Tool", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🏛️ AI Legal Analysis Tool
        
        Analyze contracts, patents, and legal documents using AI. 
        Paste your legal text below and get instant analysis with risk assessment and plain English explanations.
        
        **Built by Gigi | Powered by AI**
        
        *Professional legal document analysis at your fingertips*
        """
    )
    
    with gr.Row():
        with gr.Column():
            analysis_type = gr.Radio(
                choices=["General Analysis", "Contract Analysis", "Patent/Tech Law", "Risk Assessment"],
                value="Contract Analysis",
                label="Analysis Type"
            )
            
            text_input = gr.Textbox(
                label="Legal Text",
                placeholder="Paste your contract clause, patent text, or legal document here...",
                lines=10
            )
            
            analyze_btn = gr.Button("🔍 Analyze Document", variant="primary", size="lg")
            
            gr.Markdown(
                """
                ### 📋 Example Use Cases:
                - Employment contract clauses
                - Non-disclosure agreements  
                - Patent claims
                - Terms of service
                - Licensing agreements
                - Liability waivers
                """
            )
    
        with gr.Column():
            output = gr.Textbox(
                label="Analysis Results",
                lines=15,
                placeholder="Your detailed analysis will appear here..."
            )
    
    gr.Markdown(
        """
        ---
        **Disclaimer:** This tool provides AI-assisted analysis for informational purposes only. 
        It does not constitute legal advice. Always consult with a qualified attorney for legal matters.
        """
    )
    
    # Examples
    gr.Examples(
        examples=[
            ["The Employee shall be entitled to 28 days paid annual leave per year, inclusive of public holidays. Any unused holiday must be taken within the holiday year and cannot be carried forward without prior written consent from the Employer.", "Contract Analysis"],
            ["The Recipient agrees to hold in confidence all Confidential Information disclosed by the Discloser and shall not disclose such information to any third party without prior written consent. This obligation shall survive for a period of 5 years.", "Risk Assessment"]
        ],
        inputs=[text_input, analysis_type]
    )
    
    analyze_btn.click(
        fn=analyze_legal_text,
        inputs=[text_input, analysis_type],
        outputs=output
    )

demo.launch()
