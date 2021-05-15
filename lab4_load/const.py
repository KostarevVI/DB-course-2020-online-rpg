from dbFunctions import DBFunctions


class Data:

    def __init__(self):
        self.nickname = list()
        self.battle_result = list()
        self.id_of_person = list()
        self.class_of_person = list()
        self.item_date = list()

        dbFunctions = DBFunctions()
        dbFunctions.connect_to_database()
        dbFunctions.get_data_for_request(self.nickname,
                                         self.battle_result,
                                         self.id_of_person,
                                         self.class_of_person,
                                         self.item_date)

        self.second_and_requests = dict()
        self.millisecond_and_requests = []
        self.threads_vs_time = dict()
        for d in range(1, 1000000):
            self.second_and_requests[d] = []
