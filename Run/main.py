from Schedule.proxyRefreshSchedule import run as refreshScheduler
from Schedule.proxyRefreshSchedule import main as firstRefresh
from Schedule.proxyValidSchedule import run as validScheduler
from API.ProxyApi import run as Api
from multiprocessing import Process

def run():

    refresh_process = Process(target=refreshScheduler,name="refreshProcess")
    valid_process = Process(target=validScheduler,name="validProcess")
    api_process = Process(target=Api,name="proxyApi")
    process_list = [refresh_process,valid_process,api_process]
    for process in process_list:
        process.start()
    for process in process_list:
        process.join()

if __name__ == '__main__':
    firstRefresh()
    run()