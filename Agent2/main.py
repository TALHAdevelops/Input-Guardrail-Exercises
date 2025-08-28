from agents import Agent, Runner, input_guardrail,InputGuardrailTripwireTriggered, GuardrailFunctionOutput
from pydantic import BaseModel
from connection import config
import rich
import asyncio


class Output(BaseModel):
    response: str
    guardrail_triggered: bool


Father_agent = Agent(
    name = "father ",
    instructions= "You are a father agent. Your task is to stop your child to run AC below 26°C strictly.",
    output_type=Output,
)

@input_guardrail
async def guardrail_function(ctx, agent, input):
    checking = await Runner.run(
        Father_agent,
        input,
        run_config=config
        
    )
    rich.print(checking.final_output)
    
    return GuardrailFunctionOutput(
        output_info= checking.final_output.response,
        tripwire_triggered= checking.final_output.guardrail_triggered
    )
    
    
#MAin Agent

Child_agent = Agent(
    name="child",
    instructions="You are a child agent.",
    input_guardrails=[guardrail_function],
)

user_input = "I'm changing the temperature to 25°C"

async def main():
    try:
        response = await Runner.run(
            Child_agent,
            user_input,
            run_config=config
        )
        rich.print(response.final_output)

    except InputGuardrailTripwireTriggered as e:
        rich.print("NOO Dont Do it")

if __name__ == "__main__":
   asyncio.run(main())
