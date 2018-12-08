from easydata import Graph
import random
import math

# The following is an example of a graph used to implement a feedforward neural network.
# The neural network produces outputs, given inputs from a randomly-generated sample set.
# The goal is to show how the easydata library may be used to structure data for seemless
# application, not as an example of machine-learning.
#
# For this reason, the neural network does not feed back (i.e. train). However, it
# is obvious that this type of computation would fit into the framework shown below, as
# the variables required to compute errors and gradients are potentially if not readily
# accessible in the existing NN model.

def logistic(x):
    return 1 / (1 + pow(math.e, -x))

# Create graph and define neuron schema
nn=Graph()
nn.create_schema('neuron', ['bias', 'output'])

# Create neuron objects and links between layers
layers=[]
layer_sizes=(10, 5, 3)
for i in range(len(layer_sizes)):
	layer_size=layer_sizes[i]
	layers.append([])
	for j in range(layer_size):
		key=str(i)
		layers[i].append(key)
		nn.create_object('neuron', key, 0, [random.randrange(100)/100, 0])
		if len(layers) > 1:
			for k in layers[i-1]:
				nn.create_link(k, key, random.randrange(100)/100)

# Generate random samples
samples=[]
sample_size=3
for i in range(sample_size):
	sample=[random.randrange(2) for j in range(len(layers[0]))]
	samples.append(sample)

# Compute output for each sample
outputs=[]
for i in range(len(samples)):
	sample=samples[i]
	outputs.append([])

	# Set input layer neurons
	input_keys=layers[0]
	for j in range(len(input_keys)):
		key=input_keys[j]
		value=sample[j]
		nn.set_attr(key, 'output', value)

	# Compute hidden and output layer neurons
	neuron_keys=nn.get_instances('neuron')
	for j in range(len(neuron_keys)):
		key=neuron_keys[j]
		if key not in input_keys:
			source_keys=nn.get_attr(key, 'sources')
			input_total=0
			for k in source_keys:
				link_key=nn.get_key(k, key)
				input_weight=nn[link_key]
				input_value=nn[k]
				input_total+=input_value*input_weight
			bias_value=nn.get_attr(key, 'bias')
			output_value=logistic(input_total+bias_value)
			nn.set_attr(key, 'output', output_value)

	# Update all neurons
	output_keys=layers[len(layers)-1]
	for j in range(len(neuron_keys)):
		key=neuron_keys[j]
		value=nn.get_attr(key, 'output')
		nn[key]=value
		if key in output_keys:
			outputs[i].append(value)

# Display input-output pairs
for i in range(len(samples)):
	sample=samples[i]
	output=outputs[i]
	print(sample, '\t', output, sep='')
