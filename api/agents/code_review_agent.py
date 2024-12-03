from langchain_mistralai import ChatMistralAI
from langchain.prompts import PromptTemplate
import json
from datetime import datetime
import os
import getpass
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

class CodeReviewAgent:
    def __init__(self, model='mistral-large-latest'):
        self.llm = ChatMistralAI(model=model, temperature=0.05, mistral_api_key=MISTRAL_API_KEY)
        self.prompt_template = PromptTemplate(
            input_variables=['title', 'body', 'patch'],
            template="""
            Perform a comprehensive code review for the following Pull Request:
            
            PR Title: {title}
            PR Description: {body}
            
            Patch Details:
            {patch}
            
            For each file in the patch, analyze and provide:
            1. Style issues (formatting, naming conventions)
            2. Potential bugs or logic errors
            3. Performance concerns
            4. Best practice violations
            
            Provide output in this exact JSON format:
            {{
                "files": [
                    {{
                        "name": "filename",
                        "issues": [
                            {{
                                "type": "style|bug|performance|best_practice",
                                "line": line_number,
                                "description": "detailed issue description",
                                "suggestion": "how to fix the issue"
                            }}
                        ]
                    }}
                ],
                "summary": {{
                    "total_files": number_of_files,
                    "total_issues": total_issue_count,
                    "critical_issues": critical_issue_count
                }}
            }}
            
            Respond ONLY with the JSON, without any additional text or explanation.
            """
        )

    def analyze_pull_request(self, pr_details):
        """
        Analyze a pull request using AI-powered code review
        
        Args:
            pr_details (dict): Pull Request details from GitHub
        
        Returns:
            dict: Structured code review analysis
        """
        # Prepare the prompt with specific details
        review_prompt = self.prompt_template.format(
            title=pr_details.get('title', ''),
            body=pr_details.get('body', ''),
            patch=pr_details.get('patch', '')
        )
        print("here2")
        # Get AI review
        review_result = self.llm.predict(review_prompt)
        review_result = review_result[7:-3] 

        try:
            parsed_result = json.loads(review_result)
        except json.JSONDecodeError:
            try:
                parsed_result = json.dumps(review_result)
            except Exception as e:
                parsed_result = str(review_result)
        return {
            "pr_number": pr_details.get('number'),
            "review": parsed_result,
            "analyzed_at": datetime.now().isoformat()
        }