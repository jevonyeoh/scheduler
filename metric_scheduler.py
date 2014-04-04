from nova.scheduler import filter_scheduler
import time

class MetricScheduler(filter_scheduler.FilterScheduler):
    def __init__(self, *args, **kwargs):
        super(MetricScheduler, self).__init__(*args, **kwargs)
   
    def schedule_run_instance(self, context, request_spec,
                              admin_password, injected_files,
                              requested_networks, is_first_time,
                              filter_properties, legacy_bdm_in_spec):
                        
        time1 = time.time()
        super(MetricScheduler, self).schedule_run_instance(context, request_spec,
                              admin_password, injected_files,
                              requested_networks, is_first_time,
                              filter_properties, legacy_bdm_in_spec)
        time2 = time.time()
        diff = time2 - time1
        fo = open("/home/vagrant/timing.log", 'a')
        fo.write("Log time: " + time.strftime("%c") + "\n")
        fo.write("Filter properties\n")
        fo.write(str(filter_properties) + "\n")
        fo.write("Request spec\n")
        fo.write(str(request_spec) + "\n")
        fo.write("Time taken to schedule\n")
        fo.write(str(diff) + "\n")