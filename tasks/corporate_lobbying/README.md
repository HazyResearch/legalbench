# corporate_lobbying 
 **Contributor**: John Nay
 
 **Source**: John Nay
 
 **License**: [CC By 4.0](https://creativecommons.org/licenses/by/4.0/)
 
 **Task summary**: Predict if a proposed bill is relevant to a company.
 
 **Size (samples)**: 500
 
 ## Task Description
 
 This task measures LLM ability to predict whether a proposed bill is relevant to a company.
 
 ## Column names
 
 - `bill_title`: title of bill
 - `bill_summary`: summary of bill
 - `company_name`: name of company
 - `company_description`: description of company
 - `label`: whether the bill is relevant ("Yes") or not ("No")
 
 ## Prompting
 
 You can prompt the model like this:
 
 ```text
 template = """You are a lobbyist analyzing Congressional bills for their impacts on companies. 
 Given the title and summary of the bill, plus information on the company from its 10K SEC filing, it is your job to determine if a bill is at least somewhat relevant to a company in terms of whether it could impact the company's bottom-line if it was enacted (by saying YES or NO; note the all-caps). 
 Official title of bill: {bill_title}
 Official summary of bill: {bill_summary}
 Company name: {company_name}
 Company business description: {company_description}
 Is this bill potentially relevant to the company? FINAL ANSWER:
 """
 ```
 
 Where
 
 ```
 Official title of bill: {bill_title}
 Official summary of bill: {bill_summary}
 Company name: {company_name}
 Company business description: {company_description}
 ```
 
 Are four of the five columns of this data.
