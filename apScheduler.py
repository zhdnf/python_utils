import time 
# 阻塞
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

# 单任务阻塞
class Apscheduler(object):
    def __init__(self):
        self.sched = BlockingScheduler()
   
    # 一般方式添加job
    def add(self, func, time, id, args=()):
            self.sched.add_job(func, args=args, trigger='interval', seconds=time, id=id)
            
    def _remove(self, id):
        self.sched.remove_job(id)
        print('%s is removed'%id)
    
    # 删除job方式添加
    def add_remove(self, time, id_1, id_2):
        self.sched.add_job(self._remove, args=(id_1,), trigger='interval', seconds=time, id=id_2) 
    
    def _pause(self, id):
        self.job.pause(id)
    
    # 停止job方式添加
    def add_pause(self, time, id_1, id_2):
        self.sched.add_job(self._pause, args=(id_1,), trigger='interval',
                            seconds=time, id=id_2) 

    def _resume(self, id):
        self.job.resume(id)

    # 恢复job方式添加
    def add_resume(self, time, id_1, id_2):
        self.sched.add_job(self._resume, args=(id_1,), trigger='interval',
                            seconds=time, id=id_2) 

    # 修改job形式
    # def modify(self):

    # 显示jobs信息
    # def print(self):

    # 调度器开始
    def start(self):
        self.sched.start()

    # 关闭调度器
    def close(self):
        # 完成当前执行的任务再关闭
        self.sched.shutdown()
        # 直接关闭
        # self.sched.shutdown(wait=False)

   
    def _listener(self, event):
        if event.exception:
            print("the job crashed :( ")
        else:
            print('the job worked :) ')

    # 添加监听器
    def listener(self):
        self.sched.add_listener(self._listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    

def job():
    print("hello, world")


if __name__ == '__main__':
    timer = Apscheduler()
    timer.listener()
    timer.add(job, 2, 'hah')
    timer.add_remove(5, 'hah', 'haha')
    timer.start()
