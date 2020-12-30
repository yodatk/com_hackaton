from threading import Lock, Thread


class SingletonMeta(type):
    """
    This is a thread-safe implementation of GameLogicSingleton.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the GameLogicSingleton.
    """

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        # Now, imagine that the program has just been launched. Since there'udp_socket no
        # GameLogicSingleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the GameLogicSingleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the GameLogicSingleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class GameLogicSingleton(metaclass=SingletonMeta):
    """
    We'll use this property to prove that our GameLogicSingleton really works.
    """

    def __init__(self) -> None:
        super().__init__()
        # key = name of group, value = port
        self.group1 = {}
        self.group2 = {}
        self.game_running = False
        self.group1_score = 0
        self.group2_score = 0

    def reset(self):
        self.group1 = {}
        self.group2 = {}
        self.game_running = False
        self.group1_score = 0
        self.group2_score = 0

    def assign_team_to_group(self, name: str, connection):
        if name not in self.group1 and name not in self.group2:
            if len(self.group1) > len(self.group2):
                self.group2[name] = connection
            else:
                self.group1[name] = connection

    def add_score_to_group(self, team, score_to_add):
        if team in self.group1:
            self.group1_score += score_to_add
        elif team in self.group2:
            self.group2_score += score_to_add

    def generate_welcome_msg(self):
        return 'Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n' + "".join(
            key + "\n" for key in self.group1.keys()) + "\nGroup 2:\n==\n" + "".join(
            key + "\n" for key in self.group2.keys()) + "Start pressing keys on your keyboard as fast as you can!!\n"

    def generate_end_msg(self):
        winner_group_num = "Group 1 wins!\n\n" if self.group1_score > self.group2_score else "Group 2 wins!\n\n"
        winners = "\n".join(
            [team_name for team_name in (self.group1 if self.group1_score > self.group2_score else self.group2)])
        return 'Game over!\n' + f"Group 1 typed in {self.group1_score} characters. Group 2 typed in {self.group2_score} characters.\n" + winner_group_num + "Congratulations to the winners:\n==\n" + winners

    def some_business_logic(self):
        """
        Finally, any singleton should define some business logic, which can be
        executed on its instance.
        """


def get_instance() -> GameLogicSingleton:
    singleton = GameLogicSingleton()
    return singleton
