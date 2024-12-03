from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

class CodeReviewAgent:
    def __init__(self, model='gpt-4'):
        self.llm = ChatOpenAI(model=model, temperature=0.2)
        self.prompt_template = PromptTemplate(
            input_variables=['pr_details'],
            template="""
            Perform a comprehensive code review for the following Pull Request:

            PR Title: {pr_details[title]}
            PR Description: {pr_details[body]}
            
            Patch Details:
            {pr_details[patch]}

            Analyze and provide feedback on:
            1. Code Style and Formatting
            2. Potential Bugs or Errors
            3. Performance Improvements
            4. Best Practices and Design Recommendations

            Provide a structured JSON response with detailed comments.
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
        review_prompt = self.prompt_template.format(pr_details=pr_details)
        review_result = self.llm.predict(review_prompt)
        
        return {
            "pr_number": pr_details['number'],
            "review": json.loads(review_result),
            "analyzed_at": datetime.now().isoformat()
        }

