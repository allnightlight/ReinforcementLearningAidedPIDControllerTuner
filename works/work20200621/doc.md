

# 1. Introduction
In the following case studies,
the effect of PD-controller is investigated 
by comparing the behaviours between the system controlled by P-controller
and the ones contorlled by PD-controller.

It's supposed that 
the response against stepwise disturbance 
is improved by the derivative factor
since any abrubt change of error amplifies the action
via the derivative factor and the stepwise error can be diminished more quickly  than in the case of controlling by P-controller.

In this short text,
the responsiveness of the PD-controller is compared with the one of the P-controller
and also we see how the responsiveness depends on the hyperparameter of the Reinforcement Learning
and finally we look through the counter effect of higher responsiveness.

# 2. Specifications

## 2-1. Agent, namely Controller
The specification of agent is here.
Action consists of the following twofold,
the proportional term obtained by multiplying a value of error by a proportional gain
and the derivative term obtained by multiplying a derivative gain and a value of slope over the specific length time series of error, 
where the length of the series of errors is specified by a parameter: $nSeq$.

# 3. Highlights of case studies
The case studies shown in this text are hilighted as follow:
- The case study #1 compares the behaviours of P- and PD-controller with a set of hyper parameter by observing trends of response to the stepwise disturbance.
- The case study #2 shows the diffrence depending on the discount factor, one of the reinforcement learning hyperparameter, which controls the weight on the reward over the time horizon, more precisely say that the closer the discount factor is to 1 and the longer the time horizon is and then, less quickly the agent responses against the error.
- The case study #3 looks through the effect of the regularation parameter in order to investigate the expense of the responsiveness of controller.