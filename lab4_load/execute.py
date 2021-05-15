import threading
import time

import matplotlib.pyplot as plt
from const import Data
from dbFunctions import DBFunctions

dbFunction = DBFunctions()
dbFunction.connect_to_database()
const_and_data = Data()

use_prepare = False
threads_and_time = True
plot_x = []
plot_y = []
results_d_threads = []
unit_of_time = 20


def main():
    global plot_x
    global plot_y
    global use_prepare
    global threads_and_time
    min_req = 10
    max_req = 5000
    step = 10

    # dbFunction.drop_index_if_exists()
    # threads_and_time = False
    # threads_count = 1
    # print("Смотрим зависимость при 1 потоке")
    # x1, y1 = get_requests_and_time_dependency(min_req, max_req, step, False, threads_count)
    #
    # threads_count = 50
    # print("Смотрим зависимость при 50 потоках")
    # x2, y2 = get_requests_and_time_dependency(min_req, max_req, step, False, threads_count)
    #
    # threads_count = 92
    # print("Смотрим зависимость при 97 потоках")
    # x3, y3 = get_requests_and_time_dependency(min_req, max_req, step, False, threads_count)
    #
    # plt.title('Время/запросы без оптимизации, 20 сек, шаг 10')
    # plt.plot(x1, y1, label='1 поток')
    # plt.plot(x2, y2, label='50 потоков')
    # plt.plot(x3, y3, label='97 потоков')
    # plt.xlabel('Кол-во запросов')
    # plt.ylabel('Среднее время ответа на запрос в мс')
    # plt.legend()
    # plt.show()

    ########################

    # dbFunction.drop_index_if_exists()
    # threads_and_time = False
    # threads_count = 1
    # x1, y1 = get_requests_and_time_dependency(min_req, max_req, step, False, threads_count)
    #
    # dbFunction.add_indexes()
    # threads_count = 1
    # x2, y2 = get_requests_and_time_dependency(min_req, max_req, step, False, threads_count)
    #
    # use_prepare = True
    # threads_count = 1
    # x3, y3 = get_requests_and_time_dependency(min_req, max_req, step, False, threads_count)
    #
    # plt.title('Время/запросы, 1 потоков, 20 сек, шаг 10')
    # plt.plot(x1, y1, label='До оптимизации')
    # plt.plot(x2, y2, label='Индексы')
    # plt.plot(x3, y3, label='Индексы + Prepare')
    # plt.xlabel('Кол-во запросов')
    # plt.ylabel('Среднее время ответа на запрос в мс')
    # plt.legend()
    # plt.show()

    ########################

    dbFunction.drop_index_if_exists()
    threads_and_time = True
    threads_count = 50
    x1, y1 = get_threads_and_time_dependency(min_req, max_req, step, threads_count, False)

    dbFunction.add_indexes()
    use_prepare = True
    x2, y2 = get_threads_and_time_dependency(min_req, max_req, step, threads_count, False)

    plt.title('Время/потоки, 500 запросов, 50 потоков')
    plt.plot(x1, y1, label='До оптимизации')
    plt.plot(x2, y2, label='После оптимизации')
    plt.xlabel('Кол-во потоков')
    plt.ylabel('Среднее время ответа на запрос в мс')
    plt.legend()
    plt.show()


def get_requests_and_time_dependency(min_req, max_req, step, need_to_plot, threads_count):
    global threads_result

    threads_result = []
    for t in range(threads_count):
        qt = QueryThread(min_req, max_req, step)
        qt.start()

    while threading.activeCount() > 1:
        time.sleep(1)

    number_with_max_req_in_sec = 0
    max_req_in_sec = 0
    for i in range(1, len(threads_result)):
        values = threads_result[i - 1]
        if len(values[0]) > max_req_in_sec:
            max_req_in_sec = len(values[0])
            number_with_max_req_in_sec = i

    values = threads_result[number_with_max_req_in_sec - 1]
    print("Смотрим результаты ", str(number_with_max_req_in_sec), " потока")
    plot_x = values[0]
    plot_y = values[1]

    if need_to_plot:
        plt.plot(plot_x, plot_y, linewidth=2.0, label='Количество потоков = ' + str(threads_count), color="red")
        plt.xlabel('Количество запросов в секунду')
        plt.ylabel('Время ответа на один запрос, мс')
        plt.legend()
        plt.show()
    return plot_x, plot_y


def get_threads_and_time_dependency(min_queries, max_queries, step, num_threads, need_to_plot):
    plot_x = [k for k in range(1, num_threads + 1)]
    plot_y = []

    global cur_num_threads

    for cur_num_threads in range(1, num_threads + 1):
        results_d_threads.clear()
        cur_threads_sum = 0
        print("count time for " + str(cur_num_threads) + " threads")
        for t in range(cur_num_threads):
            dbt = QueryThread(min_queries, max_queries, step)
            dbt.start()

        while threading.activeCount() > 1:
            time.sleep(1)

        for f in range(1, len(results_d_threads)):
            cur_threads_sum += results_d_threads[f - 1]

        plot_y.append(cur_threads_sum/cur_num_threads)



    if need_to_plot:
        plt.plot(plot_x, plot_y, linewidth=2.0)
        plt.xlabel('Количество потоков')
        plt.ylabel('Время ответа на один запрос, мс')
        plt.show()
    return plot_x, plot_y


class QueryThread(threading.Thread):
    def __init__(self, min_queries, max_queries, step):

        threading.Thread.__init__(self)
        self.DBFunctions = DBFunctions()
        self.DBFunctions.connect_to_database()
        self.max_queries = max_queries
        self.min_queries = min_queries
        self.step = step

        if use_prepare:
            self.DBFunctions.prepare_queries()
            self.DBFunctions.connection.commit()

    def run(self):

        if not threads_and_time:
            thread_failed_with_time = False
            res_x = []
            res_y = []
            target_RPS = self.min_queries
            while target_RPS <= self.max_queries:
                if thread_failed_with_time:
                    break
                executed_RPS = 0
                exec_sum = 0
                start_time = time.localtime().tm_sec

                while executed_RPS < target_RPS:
                    executed_RPS += 1
                    exec_time = self.execute()
                    exec_sum += exec_time
                    run_queries_time = time.localtime().tm_sec - start_time

                    if run_queries_time >= unit_of_time or executed_RPS == target_RPS:
                        if unit_of_time - run_queries_time > 0:
                            time.sleep(unit_of_time - run_queries_time)
                        if executed_RPS < target_RPS:
                            thread_failed_with_time = True
                            break
                        else:
                            res_x.append(executed_RPS)
                            res_y.append(exec_sum / executed_RPS)

                target_RPS += self.step
            thread_res = (res_x, res_y)
            threads_result.append(thread_res)

        else:
            exec_sum = 0
            executed_req = 0
            for j in range(self.min_queries, self.max_queries + 1, self.step):
                exec_time = self.execute()
                exec_sum += exec_time
                executed_req += 1

            results_d_threads.append(exec_sum / executed_req)

    def execute(self):
        if not use_prepare:
            result = self.DBFunctions.execute_random_query_and_get_time(const_and_data)
            return result

        else:
            result = self.DBFunctions.execute_random_query_with_optimisation_and_get_time(const_and_data)
            return result


if __name__ == "__main__":
    main()
