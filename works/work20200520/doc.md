
# Section 1: Introduction

The interest of this project is to find the feasibility of tuning the PID controller via the reinforcement learning framework.

This text is aimed at finding the optimal proportional gain of the controller to regulate the environment 
modelled by the first-order time-delay system with periodically switching stepwise disturbance
by using the Actor Critic methods.
This is a very basic study, though, it's possible to verify the validity of the parameter tuning RL (Reinforcement Learning)-aided procedures.

# Section 2: Problem Setting

## Agent

This study implemented the agent as the form of the P-controller, 
which means that 
- the agent output continuous actions,
- actions are proportional to observations of the environment with the constant proportional rate, so-called proportional gain.

Other than those features, 
- the agent adds random values following the normal distribution with a fixed standard deviation = 0.1 on actions,
- actions pass through the hyperbolic tan function before being acted on the environment in order to make the tuning process stable.

## Environment

The features of the environment are followed as below:
- it's described by the first-order time-delay system with the fixed time constant = 10,
- it's driven 
	- by manipulating values given by the agent 
	- and also by disturbance switching from -1 to 1 and vice versa with the fixed interval = 30,
- it outputs the state variable as the observation.

Note that the observation is regarded as the error from the regulated value = 0, which will be minimized by the controller.

## Reward

Reward consists of the twofold parts:
- the absolute value of the observation(namely the error),
- the absolute value of actions.

It's the weight parameter on the error against the action, 
called just the weight parameter,
by which the two components are added.
For example, the value = 0.9 means prioritising the regulation of the error rather than the cost of action,
while the value = 0.1 means reducing the cost of action at the expense of high error.

## Return

Given the agent and the environment, Return is defined as the expected value of the average of rewards along with the fixed length horizon = 8.
The Actor Critic methods minimize the value of the Return 
so that the proportional parameter of the p-controller will be tuned according to the intention of the designer.

# Section 3: Case studies

It's supposed that the agents, namely P-controllers converges to the optimal one along with the training 
and that the larger the weight parameter is, the greater the optimal proportional gain is.
Here, these arguments will be confirmed.

## Subsection 3.1: case study #1

Given that the weight parameter = 0.9, 0.5, 0.1, 10 agents were trained, respectively, with the following hyper parameter.

Table 3.1.1 Training parameters
| name|value|
|:---:|:---:|
|both the value and the policy optimizer|Adam|
|learning rate for value optimization| 0.01 |
|learning rate for policy optimization| 0.001 |
|the interval of policy update| 16 |

The figure 3.1.1 shows the trace of gains along with the training for each value of the weight parameter, respectively.
You can notice that
- in all the case of the weight parameter, some of proportional gains are converging, 
- in the others, the majority of which started from the positive gain, the gain increases rather than go below the zero-axis.

<img src="./img/p_gain_training_process.png" width="480px">

Fig.3.1.1 The proportional gains over the training process

The figure 3.1.2 shows the distributions of the proportional gains for each weight parameter at the training iterations.
It shows that the median of the converged gains becomes less with the higher weight on the error in the reward.
This means that the P-controller with the higher weight parameter responses against the stepwise disturbance more quickly.

<img src="./img/p_gain_distribution.png" width="480px">

Fig.3.1.2 The proportional gains over the training process

## Subsection 3.2: case study #2

This case study used the optimizer: RMSprop instead of the optimizer: Adam as the case study #1 used.
As the former optimizer was applied to the reinforcement learning in some papers, 
it's possible that the optimizer should have been effective for the convergence of the proportional gain.
More precisely, the training parameters were set as summarised in the table 3.2.1.

The results of the trained gains are shown in the figure 3.2.1 and 3.2.2.
They tell us that the optimizer: RMSporp cannot make sense for improving the convergence.

Table 3.2.1 Training parameters
| name|value|
|:---:|:---:|
|both the value and the policy optimizer|RMSprop|
|learning rate for value optimization| 0.01 |
|learning rate for policy optimization| 0.001 |
|the interval of policy update| 16 |

<img src="./img/p_gain_training_process_casestudy002.png" width="480px">

Fig.3.2.1 The proportional gains over the training process

<img src="./img/p_gain_distribution_casestudy002.png" width="480px">

Fig.3.2.2 The proportional gains over the training process

# Summary:

- Case study #1 tells us that the PID parameter tuning algorithm powered by the RL is helpful, however, it remains the question in the convergence.
