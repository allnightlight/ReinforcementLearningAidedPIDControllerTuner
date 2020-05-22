
# Section 1: Introduction

The interest of this project is to find the feasibility of tuning the PID controller via the reinforcement learning framework.

This text is aiming at finding the optimal proportional gain of the controller to regulate the environment 
modelled by the first-order time-delay system with periodically switching stepwise disturbance
by using the Actor Critic methods

This is a very basic study, though, it's possible to verify the validity of the parameter tuning RL(Reinforcement Learning)-aided procedures.

# Section 2: Problem Setting

## Agent

The agent of this study is implimented as the form of the P-controller, 
which means that 
- the agent output continuous actions,
- actions are proportional to observations from the environment with the constant proportional rate, so-called gain.
Other than those features, 
- the agent adds random values following the normal distribution with a fixed deviation on actions,
- actions are passed through the hypobolic tan function before being imposed on the environment in order to make the tuning process stable.

## Environment

The features of the environment are followed as below:
- it's discribed by the first-order time-delay system with the fixed time constant = 10,
- it's driven 
	- by manipulated values given by the agent 
	- and also by disturbance switching from -1 to 1 and vice versa with the fixed interval = 30,
- it outputs the state variable as the observation.

Note that the observation is regarded as the error from the regulated value = 0, which will be minimized by the controller.

## Reward

Reward consists of the twofold parts:
- the absolute value of the observation(namely the error),
- the absolute value of actions.

It's the parameter: "weightOnError" by which the two components are added.
For example, "weigtOnError" = 0.9 means prioritising the regulation rather than the cost of action,
while "weightOnError" = 0.1 means reducing the cost of action at the expense of high error.

## Return

Given the agent and the environment, Return is defined as the expected value of the average of rewards along with the fixed length horizon = 16.
The Actor Critic methods minimizes the value of Return 
so that the proportional parameter of the p-controller, gain, will be tuned according to the intention of designer.

# Section 3: Experiments

It's supposed that the agents, namely P-controllers converges to the optimal one along with the training 
and that the larger the weight on the error is, the greater the optimal proportional gain is.
These are confirmed, here.

## Subsection 3.1: 

Given that "weightOnError" = 0.9, 0.5, 0.1, 10 agents were trained, respectively, with the following hyper prameter.

Table 3.1.1 Training parameters
| name|value|
|:---:|:---:|
|learning rate for value optimization| 0.01 |
|learning rate for policy optimization| 0.001 |

The figure 3.1.1 shows the trace of gains along with the training for each value of weightOnError, respectively.
You can notice that
- in all the case of weighOnError, the proportional gain converges,
- the converged gain becomes larger with the higher weight on the error in the reward.

The figure 3.1.2 shows the closed loop simulation wtih the given environment and the trained agents
for the pair of the value of weightOnError and the training iteration, respecively.
(Note that one agent among the 10 agents with the same weightOnError and the iteration, randomly.)
And, each panel contain two lines: one is the observation and another is the action.
You can notice that
- the weight on the error of the reward is greater and the P-controller responses more quickly, 
- and the action becomes more larger, which means that the action is more costly.

## Subsection 3.2: