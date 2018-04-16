import utils
import create_sequence

states = [(x, y) for x in range(-46, 31) for y in range(-9, 46)]

model = utils.hmm(states)

print("Creating Sequences")
data = create_sequence.give_seq("spencers/2018-1-1", 100)

print("Training")
model.em(data, 10)
