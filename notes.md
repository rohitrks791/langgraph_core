# Langraph:
In real scenario, our workflow hardly will be a linear chain, very commonly will be a cycle. For that langraph is very ease to handle complex workflow. 


Ex:1 ->we have a query from a user. -> then we categorize (technical, billing, general) -> analyze sentiment of the query( happy, sad, neutral, positive, negative) ->and depending on sentiment either we will Escalate (require human involvement), handling technical, billing, general team support.

We need a way to store/save the snapshots after every task that we are performing, basically we need to store the state after every single execution/function.
A state datastructure represents the current snapshot of your application

whenever we deal with state we basically hav a TypedDict (extra check) or Pydantic BaseModel

StateGraph is nothing but a workflow and state is expected
Every node takes state as a input and state as a output

we can use different llm call for different node, like we can use the free model for the easier task. for a particular kind of diffuclty or purpose, we can use different llm.

Ex:2 ->We will get a applications for particular job role of the person, ex the job role is python, we will be getting a application for python. What next step to be done for the particular candidate.
In every node we can use differents llms for our work
we will give candidate details to our llm -> then it categorize based on candidates exp. :Entry, Intermediate, Advanced. Then access_skills based on JD and the application of candidate recieved.
so our llm will do assesment.
Our llm will say whether it is a match or mismatch the JD:
we have categorize into
1. for match => schedule_hr (if candidates has exactly the skills reqd. as per job skills in JD)
2. for mismatch => check the experience of candidate, if its a senior level people the mismatch can be okay , then that case we can esclate to recruiter. but for entry level and mid level people for job apply, we will reject the application there itself.
Every node has a name and function associated with it.