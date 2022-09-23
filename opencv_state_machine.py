import time

class FaceStateMachine:
    # state machine definitions
    STATE_NO_FACE = 0
    STATE_FACE_NO_SMILE = 1
    STATE_SMILE = 2
    STATE_MANY_FACES = 3
    STATE_NUM_STATES = 4

    QUEUE_SIZE = 20

    def __init__(self, state_function):
        self.current_state = self.STATE_NO_FACE
        self.state_queue = [self.STATE_NO_FACE] * self.QUEUE_SIZE
        self.last_state_change = time.time()
        self.state_function = state_function

    def process(self, input):
        assert(input >= 0 and input < self.STATE_NUM_STATES)
        cnts = [0] * self.STATE_NUM_STATES
        self.state_queue = self.state_queue[1:] + [input]
        for i in range(self.QUEUE_SIZE):
            cnts[self.state_queue[i]] += 1

        new_state = self.current_state
        for i in range(self.STATE_NUM_STATES):
            if cnts[i] >= self.QUEUE_SIZE//2:
                new_state = i

        if new_state != self.current_state:
            self.last_state_change = time.time()
            self.current_state = new_state

        self.state_function(self.current_state, self.last_state_change)
