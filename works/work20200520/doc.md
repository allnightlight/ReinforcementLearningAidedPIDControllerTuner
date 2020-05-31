
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
- the agent adds random values following the normal distribution 
	- with a fixed standard deviation = 0.1 on actions
	- or with a variable one on actions, 
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

Given the agent and the environment, Return is defined as either the expected value of the average of rewards along with the fixed length horizon = 8
or the expected one of the summation of the infinite reward series with the fixed discounting factor = 0.9.
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
| finite or infinite reward series | finite |
|reward horizon length | 8 |
| fix standard deviation of policy's probability | True|

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
the optimizer might have been effective for the convergence of the proportional gain.
That's why the difference of the optimizers was verified, here.
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
| finite or infinite reward series | finite |
|reward horizon length | 8 |
| fix standard deviation of policy's probability | True|


<img src="./img/p_gain_training_process_casestudy002.png" width="480px">

Fig.3.2.1 The proportional gains over the training process

<img src="./img/p_gain_distribution_casestudy002.png" width="480px">

Fig.3.2.2 The proportional gains over the training process

## Subsection 3.3: case study #3

In the contrast to the case studies #1 and #2,
the return was given by the summation of the infinite reward series with the discounting factor: gamma = 0.9
, which is equivalent to the moving average with the fixed window length = 10.
The length of the reward horizon = 8 of both the case studies #1 and #2 is enough long to cover the effect of the actions
and the result of the training does not differ from the case studies #1 and #2,
though, it's beneficial to train agents since the interval of policy update can be shrunk from 16 to 2.

The training parameters in the table 3.3.1 shown below were used.
The figure 3.3.1 and the figure 3.3.2 are the traces of the trained proportional gains.
Beyond the expectation, the summation of the infinite reward series with the discounting factor can lead to better convergence.
Especially, in the case with the weigh parameter = 0.1, the gain has already converged
and in the rest of the cases, it's possible to see that the gains are approaching to the converged one.
I'm struggling with the reason.

Table 3.3.1 Training parameters
| name|value|
|:---:|:---:|
|both the value and the policy optimizer|Adam|
|learning rate for value optimization| 0.01 |
|learning rate for policy optimization| 0.001 |
|the interval of policy update| 2 |
| finite or infinite reward series | infinite |
| gamma | 0.9 |
| fix standard deviation of policy's probability | True|

<img src="./img/p_gain_training_process_casestudy003.png" width="480px">

Fig.3.3.1 The proportional gains over the training process

<img src="./img/p_gain_distribution_casestudy003.png" width="480px">

Fig.3.3.2 The proportional gains over the training process

## Subsection 3.4: case study #4

This case study investigates the impact of the variable standard deviation of agents' policy.
The standard deviation is tuned to the logarithm scale.
This means that a parameter which represents the logarithm of the standard deviation is tuned through the RL-training.

The training parameters and the training results are shown in the table 3.4.1
, the figure 3.4.1 and the figure 3.4.2, respectively.
They reveal that the variable standard deviation did not contribute to the improvement of the convergence.

Table 3.4.1 Training parameters
| name|value|
|:---:|:---:|
|both the value and the policy optimizer|Adam|
|learning rate for value optimization| 0.01 |
|learning rate for policy optimization| 0.001 |
|the interval of policy update| 2 |
| finite or infinite reward series | infinite |
| gamma | 0.9 |
| fix standard deviation of policy's probability | False |

<img src="./img/p_gain_training_process_casestudy004.png" width="480px">

Fig.3.4.1 The proportional gains over the training process

<img src="./img/p_gain_distribution_casestudy004.png" width="480px">

Fig.3.4.2 The proportional gains over the training process



# Summary:

- Case study #1 tells us that the PID parameter tuning algorithm powered by the RL is helpful, however, it remains the question in the convergence.
