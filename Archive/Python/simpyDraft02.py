#!/usr/bin/env python
from random import randint
import simpy

TALKS_PER_LESSON = 3
TALK_LENGTH = 30
BREAK_LENGTH = 15
DURATION_EAT


def attendee(env, name, knowledge=0, hunger=0):
    while True:
        # Guest talks
        for i in range(TALKS_PER_LESSON):
            knowledge += randint(0, 3) / (1 + hunger)
            hunger += randint(1, 4)

            yield env.timeout(TALK_LENGTH)

        print(
            '''Attendee %s finished talks with knowledge %.2f \
and hunger %.2f.''' % (name, knowledge, hunger))
        # Go to buffet
        food = randint(3, 12)
        hunger -= min(food, hunger)

        yield env.timeout(BREAK_LENGTH)

        print(
            'Attendee %s finished eating with hunger %.2f.' % (
                name, hunger))


env = simpy.Environment()
for i in range(5):
    env.process(attendee(env, i))
env.run(until=220)
# def clock(env, name, tick):
#     while True:
#         print(name, env.now)
#         yield env.timeout(tick)


# env = simpy.Environment()

# env.process(clock(env, 'fast', 0.5))
# env.process(clock(env, 'slow', 1))
# env.run(until=2)
