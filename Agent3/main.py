from agents import Agent, Runner, input_guardrail,InputGuardrailTripwireTriggered, GuardrailFunctionOutput
from pydantic import BaseModel
from connection import config
import rich
import asyncio


class Output(BaseModel):
    response: str
    guardrail_triggered: bool


gateKeeper_agent = Agent(
    name = "guardrail_agent",
    instructions= "You are a school gatekeeper agent. Your task is to stop Students from other schools.",
    output_type=Output,
)

@input_guardrail
async def guardrail_function(ctx, agent, input):
    checking = await Runner.run(
        gateKeeper_agent,
        input,
        run_config=config
        
    )
    rich.print(checking.final_output)
    
    return GuardrailFunctionOutput(
        output_info= checking.final_output.response,
        tripwire_triggered= checking.final_output.guardrail_triggered
    )
    
    
#MAin Agent

student = Agent(
    name="student",
    instructions="You are a student agent.",
    input_guardrails=[guardrail_function],
)

user_input = "I'm studying in other school"

async def main():
    try:
        response = await Runner.run(
            student,
            user_input,
            run_config=config
        )
        rich.print(response.final_output)

    except InputGuardrailTripwireTriggered as e:
        rich.print("Only this school's students are allowed.")

if __name__ == "__main__":
   asyncio.run(main())
