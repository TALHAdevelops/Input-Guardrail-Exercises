from agents import Agent, Runner, input_guardrail,InputGuardrailTripwireTriggered, GuardrailFunctionOutput
from pydantic import BaseModel
from connection import config
import rich
import asyncio


class Output(BaseModel):
    response: str
    guardrail_triggered: bool


guardrail_agent = Agent(
    name = "guardrail_agent",
    instructions= "You are a guardrail agent. Your task is to check whether input of student is related to studies not management related.",
    output_type=Output,
)

@input_guardrail
async def guardrail_function(ctx, agent, input):
    checking = await Runner.run(
        guardrail_agent,
        input,
        run_config=config
        
    )
    rich.print(checking.final_output)
    
    return GuardrailFunctionOutput(
        output_info= checking.final_output.response,
        tripwire_triggered= checking.final_output.guardrail_triggered
    )
    
    
#MAin Agent

Student = Agent(
    name="student",
    instructions="You are a student agent.",
    input_guardrails=[guardrail_function],
)

user_input = "I want to change my class timings 😭😭"

async def main():
    try:
        response = await Runner.run(
            Student,
            user_input,
            run_config=config
        )
        rich.print(response.final_output)

    except InputGuardrailTripwireTriggered as e:
        rich.print("Only studies are allowed.")

if __name__ == "__main__":
   asyncio.run(main())
