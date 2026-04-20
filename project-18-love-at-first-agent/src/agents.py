from dotenv import load_dotenv
import os
load_dotenv(r"C:\\Users\\Gurveer\\ds-portfolio\\.env")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

import json
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

@tool
def profile_data(info: str) -> str:
    """Profile the speed dating dataset."""
    return json.dumps({"total_rows": 8378, "match_rate": "16.5%",
                       "recommendation": "Use ROC AUC due to class imbalance"})

@tool
def check_leakage(features: str) -> str:
    """Check features for data leakage."""
    leakage = ["decision", "decision_o", "match", "dec", "dec_o"]
    flagged = [f.strip() for f in features.split(",") if f.strip() in leakage]
    safe = [f.strip() for f in features.split(",") if f.strip() not in leakage]
    return json.dumps({"flagged_leakage": flagged, "safe_features": safe})

def build_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return create_react_agent(llm, tools=[profile_data, check_leakage])

if __name__ == "__main__":
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": "Profile the dataset."}]})
    print(result["messages"][-1].content)
