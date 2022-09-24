import time

class FaceStateMachine:
    # state machine definitions
    STATE_NO_FACE = 0
    STATE_FACE_NO_SMILE = 1
    STATE_SMILE = 2
    STATE_MANY_FACES = 3
    STATE_SCATTER = 4
    STATE_NUM_STATES = 5

    NONE_STRIKE_THRESHOLD = 6
    FACE_STRIKE_THRESHOLD = 2
    SMILE_STRIKE_THRESHOLD = 4
    NOSMILE_STRIKE_THRESHOLD = 2

    SCATTER_THRESHOLD = 15

    def __init__(self, state_function):
        self.current_state = self.STATE_NO_FACE
        self.last_state_change = time.time()
        self.last_face_detection = 0
        self.state_function = state_function
        self.face_strike = 0
        self.none_strike = 0
        self.face_detected = False
        self.smile_strike = 0
        self.nosmile_strike = 0
        self.smile_detected = False

    def process(self, input):
        assert(input >= 0 and input < self.STATE_NUM_STATES)

        new_state = self.current_state

        if input == self.STATE_NO_FACE:
            self.none_strike += 1
            self.face_strike = 0
            if self.none_strike == self.NONE_STRIKE_THRESHOLD:
                self.none_strike = 0
                self.smile_strike = 0
                self.nosmile_strike = 0
                self.face_detected = False
                self.last_face_detection = 0
                self.smile_detected = False
                new_state = self.STATE_NO_FACE

        if input == self.STATE_FACE_NO_SMILE or input == self.STATE_SMILE:
            self.none_strike = 0
            self.face_strike += 1
            if self.face_strike == self.FACE_STRIKE_THRESHOLD:
                self.face_strike = 0
                if self.face_detected == False:
                    new_state = self.STATE_FACE_NO_SMILE
                    self.last_face_detection = time.time()
                self.face_detected = True

        if self.face_detected and input == self.STATE_FACE_NO_SMILE:
            self.smile_strike = 0
            self.nosmile_strike += 1
            if self.nosmile_strike == self.NOSMILE_STRIKE_THRESHOLD:
                self.nosmile_strike = 0
                self.smile_detected = False
                new_state = self.STATE_FACE_NO_SMILE

        if self.face_detected and input == self.STATE_SMILE:
            self.nosmile_strike = 0
            self.smile_strike += 1
            if self.smile_strike == self.SMILE_STRIKE_THRESHOLD:
                self.smile_strike = 0
                self.smile_detected = True
                new_state = self.STATE_SMILE

        # check if someone got stuck in front of the camera
        if self.face_detected and \
                self.last_face_detection != 0 and \
                time.time() - self.last_face_detection > self.SCATTER_THRESHOLD:
            new_state = self.STATE_SCATTER
            self.face_detected = False
            self.last_face_detection = 0

        if new_state != self.current_state:
            self.last_state_change = time.time()
            self.current_state = new_state

        self.state_function(self.current_state, self.last_state_change)
