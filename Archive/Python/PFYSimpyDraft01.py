#!/usr/bin/env python
import numpy
import simpy


def truck(env,
          id,
          ini_cnt_id,
          end_cnt_id,
          ingate_queue_time,
          ingate_process_time,
          travel_to_pfinder_time,
          back_in_time,
          pfinder_process_time,
          pull_out_time,
          travel_to_outgate_time,
          outgate_queue_time,
          outgate_process_time
          ):
    def __init__(self):
        self.id = numpy.random.randint(1, 10)
        self.ini_cnt_id = 0
        self.end_cnt_id = 0
        self.ingate_queue_time = 0
        self.ingate_process_time = 0
        self.travel_to_pfinder_time = 0
        self.back_in_time = 0
        self.pfinder_process_time = 0
        self.pull_out_time = 0
        self.travel_to_outgate_time = 0
        self.outgate_queue_time = 0
        self.outgate_process_time = 0
    while True:
        print("Hello")
        print(ini_cnt_id)
        yield env.timeout(numpy.random.randint(1, 10))


def main():

    env = simpy.Environment()
    for i in range(200):
        env.process(truck(env))
    env.run(until=1000)


if __name__ == '__main__':
    main()

# def attendee(env, name, buffet, knowledge=0, hunger=0):
#     while True:
#         # Guest talks
#         for i in range(TALKS_PER_LESSON):
#             knowledge += randint(0, 3) / (1 + hunger)
#             hunger += randint(1, 4)
#             # print('%s time in talks: %.2f' % (name, env.now))

#             yield env.timeout(TALK_LENGTH)

#         print(
#             '''Attendee %s finished talks with knowledge %.2f \
# and hunger %.2f.''' % (name, knowledge, hunger))
#         # Go to buffet
#         start = env.now
#         print('%s entered buffet queue at %.2f.' % (name, start))
#         with buffet.request() as req:
#             yield req | env.timeout(BREAK_LENGTH - DURATION_EAT)
#             time_left = BREAK_LENGTH - (env.now - start)

#             if req.triggered:
#                 print('%s waited for %.2f.' % (name, env.now - start))

#                 food = min(
#                     randint(3, 12), time_left)  # Less time -> less food
#                 yield env.timeout(DURATION_EAT)
#                 hunger -= min(food, hunger)
#                 time_left -= DURATION_EAT
#                 print(
#                     'Attendee %s finished eating with hunger %.2f.' % (
#                         name, hunger))
#             else:
#                 hunger -= 1  # Penalty for only taking a look at all the food
#                 print(
#                     '''Attendee %s didn\'t make it to the buffet, \
# hunger is now at %.2f.''' % (name, hunger))

#         yield env.timeout(time_left)


# buffet = simpy.Resource(env, capacity=BUFFET_SLOTS)
# for i in range(10):
#     env.process(attendee(env, i, buffet))
# env.run(until=220)
# def clock(env, name, tick):
#     while True:
#         print(name, env.now)
#         yield env.timeout(tick)


# env = simpy.Environment()

# env.process(clock(env, 'fast', 0.5))
# env.process(clock(env, 'slow', 1))
# env.run(until=2)
