class Activity:
    def __init__(self, id, duration, predecessors=[]):
        self.id = id
        self.duration = duration
        self.predecessors = predecessors
        self.successors = []
        self.es = None
        self.ef = None
        self.ls = None
        self.lf = None
        self.slack = None
