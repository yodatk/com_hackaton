"""

Game Logic For the Keyboard game - this is a safe
threaded singleton implementation because this resource is
being used by a lot of threads


"""

from threading import Lock


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
        # key = name of group, tcp connection
        self.group1 = {}
        self.group2 = {}
        self.game_running = False
        self.group1_score = 0
        self.group2_score = 0

    def reset(self):
        """
        reset all params of the game
        :return:
        """
        self.group1 = {}
        self.group2 = {}
        self.game_running = False
        self.group1_score = 0
        self.group2_score = 0

    def assign_team_to_group(self, name: str, connection):
        """
        will assign the team to a certain group - randomly
        :param name: name of the team we want to assign
        :param connection: the team tcp connection
        :return: none
        """
        if name not in self.group1 and name not in self.group2:
            if len(self.group1) > len(self.group2):
                print(f"group: {name} is now added to group2")
                self.group2[name] = connection
            else:
                print(f"group: {name} is now added to group1")
                self.group1[name] = connection
        else:
            print(f"group: {name} rejected becasue it's already in a group")

    def add_score_to_group(self, team, score_to_add):
        """
        giving the score of the group that related to the team that submitted those chars
        :param team: name of the team to add the score
        :param score_to_add: number of chars to add
        :return:
        """
        print(f"adding score: {score_to_add} from team: {team}")
        if team in self.group1:
            self.group1_score += score_to_add
        elif team in self.group2:
            self.group2_score += score_to_add

    def generate_welcome_msg(self):
        """
        :return: generate welcoming string according to the teams in the groups
        """
        return 'Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n' + "".join(
            key + "\n" for key in self.group1.keys()) + "\nGroup 2:\n==\n" + "".join(
            key + "\n" for key in self.group2.keys()) + "Start pressing keys on your keyboard as fast as you can!!\n"

    def generate_end_msg(self):
        winner_group_num = "Group 1 wins!\n\n" if self.group1_score > self.group2_score else "Group 2 wins!\n\n"
        winners = "\n".join(
            [team_name for team_name in (self.group1 if self.group1_score > self.group2_score else self.group2)])
        return 'Game over!\n' + f"Group 1 typed in {self.group1_score} characters. Group 2 typed in {self.group2_score} characters.\n" + winner_group_num + "Congratulations to the winners:\n==\n" + winners


def get_instance() -> GameLogicSingleton:
    """
    safe way to get into the singleton
    :return: the singleton
    """
    singleton = GameLogicSingleton()
    return singleton
